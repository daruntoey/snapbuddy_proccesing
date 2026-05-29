"""AI matching — keyword fallback + NLP when available."""
from typing import List, Dict, Optional
import numpy as np
from loguru import logger

from app.services.sheets_service import sheets_service
from app.ai.gemini_service import gemini_service
from app.ai.nlp_service import nlp_service


class AIMatchingService:

    async def match_buddies(
        self,
        user_description: str,
        budget_max: Optional[int] = None,
        city: Optional[str] = None,
        min_rating: Optional[float] = None,
        top_k: int = 10,
    ) -> List[Dict]:
        logger.info(f"match_buddies start: '{user_description[:60]}'")

        # 1. Get buddies
        buddies = await sheets_service.get_buddies(min_rating=min_rating, city=city)
        logger.info(f"Buddies from Sheets: {len(buddies)}")

        if not buddies:
            logger.warning("No buddies returned")
            return []

        # 2. Try NLP embedding (optional)
        user_emb = None
        try:
            user_emb = await nlp_service.extract_text_embedding(user_description)
            logger.info("NLP embedding ready")
        except Exception as e:
            logger.warning(f"NLP unavailable: {e}")

        # 3. Score each buddy
        user_words = set(user_description.lower().replace(",", " ").split())
        scored = []

        for buddy in buddies:
            try:
                buddy_text = (
                    buddy.get("top_styles", "") + " "
                    + buddy.get("bio", "") + " "
                    + buddy.get("city", "")
                ).lower()
                buddy_words = set(buddy_text.replace(",", " ").split())

                # Keyword similarity (always works)
                common = user_words & buddy_words
                keyword_sim = len(common) / max(len(user_words), 1)

                # NLP similarity (if available)
                nlp_sim = keyword_sim
                if user_emb is not None:
                    try:
                        buddy_emb = await nlp_service.extract_text_embedding(buddy_text)
                        if buddy_emb is not None:
                            nlp_sim = self._cosine(user_emb, buddy_emb)
                    except Exception:
                        pass

                similarity = (nlp_sim * 0.6) + (keyword_sim * 0.4)

                rating = float(buddy.get("average_rating", 0) or 0)
                exp = min(int(buddy.get("experience_year", 0) or 0), 10)
                portfolio = min(int(buddy.get("portfolio_count", 0) or 0), 200)

                score = round(
                    similarity * 70
                    + (rating / 5.0) * 15
                    + (exp / 10.0) * 10
                    + (portfolio / 200.0) * 5,
                    1,
                )

                scored.append({
                    **buddy,
                    "match_score": score,
                    "similarity": round(float(similarity), 4),
                    "explanation": "",
                    "portfolio": [],
                })
            except Exception as e:
                logger.warning(f"Score failed {buddy.get('buddy_id')}: {e}")

        # 4. Sort
        scored.sort(key=lambda x: x["match_score"], reverse=True)
        top = scored[:top_k]
        logger.info(f"Top {len(top)} matches, best score={top[0]['match_score'] if top else 0}")

        # 5. Enrich top 5
        for buddy in top[:5]:
            try:
                buddy["portfolio"] = await sheets_service.get_portfolio(buddy["buddy_id"])
            except Exception:
                buddy["portfolio"] = []
            buddy["explanation"] = await self._explain(user_description, buddy)

        return top

    def _cosine(self, a, b) -> float:
        a, b = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0:
            return 0.0
        return float(np.dot(a / na, b / nb))

    async def _explain(self, user_desc: str, buddy: Dict) -> str:
        try:
            prompt = (
                "สรุป 1 ประโยคว่าทำไม buddy นี้ถึงเหมาะกับผู้ใช้ (ภาษาไทย):\n"
                "ผู้ใช้ต้องการ: " + user_desc + "\n"
                "Buddy: " + buddy.get("nickname", "") + " | "
                + buddy.get("top_styles", "") + " | "
                + "rating " + str(buddy.get("average_rating", 0))
            )
            result = await gemini_service.generate_content(prompt)
            if "mock" not in result:
                return result.strip()
        except Exception as e:
            logger.warning(f"Explain failed: {e}")
        return "เหมาะสมกับสไตล์ที่ต้องการ"


ai_matching_service = AIMatchingService()
