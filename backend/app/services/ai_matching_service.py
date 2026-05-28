"""AI-powered matching service using buddyProfile + buddyPortfolio from Google Sheets."""
from typing import List, Dict, Optional
import numpy as np
from loguru import logger

from app.services.sheets_service import sheets_service
from app.ai.gemini_service import gemini_service
from app.ai.nlp_service import nlp_service


class AIMatchingService:
    """
    Match buddies to a user's request using:
    1. NLP cosine-similarity on combined profile+portfolio text
    2. Rating bonus
    3. Gemini explanation for top-5 results
    """

    async def match_buddies(
        self,
        user_description: str,
        budget_max: Optional[int] = None,
        city: Optional[str] = None,
        min_rating: Optional[float] = None,
        top_k: int = 10,
    ) -> List[Dict]:
        """
        Main entry point.

        Returns up to `top_k` ranked buddy dicts with added fields:
          match_score  – 0-100
          similarity   – cosine similarity 0-1
          explanation  – Gemini-generated reason (top 5 only)
          portfolio    – list of portfolio items for this buddy
        """
        # 1. Fetch buddies from Sheets (pre-filtered)
        buddies = await sheets_service.get_buddies(
            min_rating=min_rating,
            city=city,
        )
        if not buddies:
            logger.warning("No buddies returned from Sheets")
            return []

        # 2. Embed the user's request
        user_emb = await nlp_service.extract_text_embedding(user_description)
        if user_emb is None:
            logger.error("Could not compute user embedding")
            return []

        # 3. Score each buddy
        scored: List[Dict] = []
        for buddy in buddies:
            try:
                buddy_text = await sheets_service.get_buddy_embedding_text(buddy)
                buddy_emb = await nlp_service.extract_text_embedding(buddy_text)
                if buddy_emb is None:
                    continue

                similarity = self._cosine_similarity(user_emb, buddy_emb)

                # Base score from similarity (0-100)
                base = similarity * 100

                # Rating bonus: up to +10 pts
                rating = buddy.get("average_rating", 0) or 0
                rating_bonus = (rating / 5.0) * 10

                # Experience bonus: up to +5 pts
                exp = min(buddy.get("experience_year", 0) or 0, 10)
                exp_bonus = (exp / 10.0) * 5

                # Portfolio depth bonus: up to +5 pts
                portfolio_count = buddy.get("portfolio_count", 0) or 0
                portfolio_bonus = min(portfolio_count / 200.0, 1.0) * 5

                final_score = round(base + rating_bonus + exp_bonus + portfolio_bonus, 1)

                scored.append({
                    **buddy,
                    "match_score": final_score,
                    "similarity": round(float(similarity), 4),
                    "explanation": "",   # filled below for top-5
                    "portfolio": [],     # filled below for top-5
                })
            except Exception as e:
                logger.warning(f"Scoring failed for {buddy.get('buddy_id')}: {e}")

        # 4. Sort descending by match score
        scored.sort(key=lambda x: x["match_score"], reverse=True)
        top = scored[:top_k]

        # 5. Enrich top-5 with portfolio items + Gemini explanation
        for buddy in top[:5]:
            # Portfolio
            try:
                buddy["portfolio"] = await sheets_service.get_portfolio(buddy["buddy_id"])
            except Exception:
                buddy["portfolio"] = []

            # Gemini explanation
            buddy["explanation"] = await self._explain_match(user_description, buddy)

        logger.info(f"✅ Matched {len(top)} buddies for query: '{user_description[:60]}'")
        return top

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        a = np.array(a, dtype=np.float32)
        b = np.array(b, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a / norm_a, b / norm_b))

    async def _explain_match(self, user_description: str, buddy: Dict) -> str:
        try:
            portfolio_summary = ""
            for p in buddy.get("portfolio", [])[:3]:
                portfolio_summary += (
                    f"  - {p.get('category','')}: mood={p.get('mood_tag','')}, "
                    f"light={p.get('lighting_tag','')}, edit={p.get('edit_style','')}\n"
                )

            prompt = f"""คุณเป็นผู้ช่วย SnapBuddy อธิบายให้ผู้ใช้เข้าใจว่าทำไม buddy คนนี้ถึง match กับที่ต้องการ (1-2 ประโยค ภาษาไทย):

ผู้ใช้ต้องการ: {user_description}

Buddy:
- ชื่อ/ชื่อเล่น: {buddy.get('nickname') or buddy.get('name', '')}
- Bio: {buddy.get('bio', '')}
- สไตล์หลัก: {buddy.get('top_styles', '')}
- ประสบการณ์: {buddy.get('experience_year', 0)} ปี
- Rating: {buddy.get('average_rating', 0)}/5
- Portfolio ตัวอย่าง:
{portfolio_summary or '  (ไม่มีข้อมูล)'}

ตอบสั้น กระชับ ตรงประเด็น ไม่ต้องขึ้นต้นด้วย "Buddy" หรือชื่อ"""

            result = await gemini_service.generate_content(prompt)
            return result.strip() if result else "เหมาะสมกับสไตล์ที่ต้องการ"
        except Exception as e:
            logger.warning(f"Gemini explanation failed: {e}")
            return "เหมาะสมกับสไตล์ที่ต้องการ"


# Global singleton
ai_matching_service = AIMatchingService()
