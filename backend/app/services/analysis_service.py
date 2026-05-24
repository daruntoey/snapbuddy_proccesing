"""AI analysis service."""
from typing import List
from app.schemas.analysis import MoodAnalysisRequest, MoodAnalysisResponse
from app.ai.gemini_service import gemini_service
from app.ai.nlp_service import nlp_service
from app.ai.cv_service import cv_service
from app.ai.aesthetic_engine import aesthetic_engine
from app.models.mood_spec import MoodSpec

class AnalysisService:
    async def analyze_user_mood(self, request: MoodAnalysisRequest, user_id: int, db):
        """Analyze user's aesthetic preferences."""
        
        # Extract text features
        mood_analysis = {}
        if request.text_description:
            mood_analysis = await gemini_service.analyze_mood_from_text(request.text_description)
            text_embedding = await nlp_service.extract_text_embedding(request.text_description)
        else:
            text_embedding = None
        
        # Extract image features
        image_embeddings = []
        # For now, skip actual image processing
        
        # Create combined embedding
        if image_embeddings or text_embedding is not None:
            combined_embedding = await aesthetic_engine.merge_embeddings(
                image_embeddings, text_embedding
            )
        else:
            combined_embedding = None
        
        # Generate summary
        aesthetic_summary = await gemini_service.generate_aesthetic_summary({
            "mood_tags": mood_analysis.get("mood_tags", []),
            "style_tags": mood_analysis.get("style_tags", []),
            "text_description": request.text_description,
            "budget_min": request.budget_min,
            "budget_max": request.budget_max,
        })
        
        # Save mood spec
        mood_spec = MoodSpec(
            user_id=user_id,
            text_description=request.text_description,
            mood_tags=mood_analysis.get("mood_tags", []),
            style_tags=mood_analysis.get("style_tags", []),
            budget_min=request.budget_min,
            budget_max=request.budget_max,
            preferred_location=request.location,
        )
        db.add(mood_spec)
        await db.commit()
        await db.refresh(mood_spec)
        
        return MoodAnalysisResponse(
            mood_spec_id=mood_spec.id,
            mood_tags=mood_analysis.get("mood_tags", []),
            style_tags=mood_analysis.get("style_tags", []),
            detected_intent=mood_analysis.get("detected_intent", ""),
            aesthetic_summary=aesthetic_summary,
        )

    async def extract_embeddings(self, image_urls: List[str]):
        """Extract embeddings from images."""
        # Implement image embedding extraction
        return {"embeddings": []}

analysis_service = AnalysisService()
