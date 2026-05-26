"""AI-powered matching service using data from Google Sheets."""
from typing import List, Dict
import numpy as np
from loguru import logger

from app.services.sheets_service import sheets_service
from app.ai.gemini_service import gemini_service
from app.ai.nlp_service import nlp_service


class AIMatchingService:
    """Match photographers using AI analysis."""
    
    async def match_photographers(
        self,
        user_description: str,
        budget_max: int = 10000,
        location: str = "Bangkok"
    ) -> List[Dict]:
        """
        Match photographers based on user description using AI.
        
        Steps:
        1. Get all photographers from Google Sheets
        2. Extract user preferences embedding (NLP)
        3. Calculate similarity scores
        4. Use Gemini to explain matches
        5. Return ranked results
        """
        try:
            # 1. Get photographers from Sheets
            photographers = await sheets_service.get_photographers(
                max_rate=budget_max
            )
            
            if not photographers:
                logger.warning("No photographers found")
                return []
            
            # 2. Get user preferences embedding
            user_embedding = await nlp_service.extract_text_embedding(
                user_description
            )
            
            # 3. Calculate match scores
            matches = []
            for photographer in photographers:
                # Get photographer styles embedding
                styles_text = photographer.get('styles', '')
                photographer_embedding = await nlp_service.extract_text_embedding(
                    styles_text
                )
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(
                    user_embedding,
                    photographer_embedding
                )
                
                # Calculate final score (0-100)
                base_score = similarity * 100
                
                # Bonus for rating
                rating_bonus = photographer.get('rating', 0) * 2
                
                # Penalty for price
                price_factor = 1.0
                if photographer.get('hourly_rate', 0) > budget_max * 0.8:
                    price_factor = 0.9
                
                final_score = (base_score + rating_bonus) * price_factor
                
                matches.append({
                    **photographer,
                    "match_score": round(final_score, 1),
                    "similarity": round(similarity, 3)
                })
            
            # 4. Sort by score
            matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            # 5. Add AI explanations for top matches
            top_matches = matches[:5]
            for match in top_matches:
                explanation = await self._generate_explanation(
                    user_description,
                    match
                )
                match['explanation'] = explanation
            
            logger.info(f"✅ Found {len(top_matches)} matches")
            return top_matches
            
        except Exception as e:
            logger.error(f"Matching failed: {e}")
            return []
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        return float(np.dot(vec1_norm, vec2_norm))
    
    async def _generate_explanation(
        self,
        user_description: str,
        photographer: Dict
    ) -> str:
        """Generate AI explanation for why this photographer matches."""
        try:
            prompt = f"""
            Explain in 1-2 sentences why this photographer matches the user's request:
            
            User wants: {user_description}
            
            Photographer:
            - Name: {photographer['business_name']}
            - Styles: {photographer['styles']}
            - Rating: {photographer.get('rating', 0)}/5
            - Rate: ${photographer.get('hourly_rate', 0)}/hr
            
            Be specific and concise.
            """
            
            explanation = await gemini_service.generate_content(prompt)
            return explanation.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")
            return "Great match based on style and expertise"


# Global instance
ai_matching_service = AIMatchingService()
