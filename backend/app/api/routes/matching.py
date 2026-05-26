"""AI Matching routes using Google Sheets data."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger
import json

router = APIRouter()


class MatchRequest(BaseModel):
    description: str
    budget_max: int = 10000
    location: Optional[str] = "Bangkok"


@router.post("/match")
async def match_photographers(request: MatchRequest):
    """Match photographers using AI + Google Sheets data."""
    try:
        logger.info(f"🔍 Matching photographers for: {request.description}")
        
        # Return mock matches (Google Sheets integration pending)
        mock_matches = [
            {
                "photographer_id": 1,
                "business_name": "Bangkok Studio Photography",
                "bio": "Specializing in Korean cafe aesthetic",
                "location": "Bangkok",
                "hourly_rate": 2000,
                "styles": "Korean cafe, natural light, cozy, warm tones",
                "rating": 4.8,
                "phone": "081-234-5678",
                "email": "bangkok@studio.com",
                "match_score": 95.5,
                "explanation": "Perfect match for Korean cafe aesthetic with experience in natural lighting and cozy compositions."
            },
            {
                "photographer_id": 2,
                "business_name": "Urban Light Photography",
                "bio": "Bright and airy minimalist photography",
                "location": "Bangkok",
                "hourly_rate": 2500,
                "styles": "Minimalist, bright, editorial, clean lines",
                "rating": 4.7,
                "phone": "082-345-6789",
                "email": "urban@light.com",
                "match_score": 88.2,
                "explanation": "Strong match for clean, modern aesthetic with excellent editorial experience and professional lighting."
            },
            {
                "photographer_id": 3,
                "business_name": "Candid Moments Studio",
                "bio": "Natural and warm lifestyle photography",
                "location": "Bangkok",
                "hourly_rate": 1800,
                "styles": "Natural, warm, lifestyle, candid, emotional",
                "rating": 4.9,
                "phone": "083-456-7890",
                "email": "candid@moments.com",
                "match_score": 82.7,
                "explanation": "Great for authentic, emotional shots with warm tones and natural aesthetic. Highest rating among matches."
            }
        ]
        
        # Sort by match score
        mock_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        logger.info(f"✅ Found {len(mock_matches)} photographers")
        
        return {
            "matches": mock_matches,
            "total": len(mock_matches),
            "query": request.description,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"❌ Matching failed: {e}", exc_info=True)
        raise HTTPException(500, f"Matching failed: {str(e)}")


@router.get("/photographers")
async def get_photographers(
    skip: int = 0,
    limit: int = 10,
    style: Optional[str] = None,
):
    """Get photographers from Google Sheets (mock data for now)."""
    try:
        mock_photographers = [
            {
                "photographer_id": 1,
                "business_name": "Bangkok Studio Photography",
                "styles": "Korean cafe, natural light, cozy",
                "location": "Bangkok",
                "hourly_rate": 2000,
                "rating": 4.8,
                "email": "bangkok@studio.com"
            },
            {
                "photographer_id": 2,
                "business_name": "Urban Light Photography",
                "styles": "Minimalist, bright, editorial",
                "location": "Bangkok",
                "hourly_rate": 2500,
                "rating": 4.7,
                "email": "urban@light.com"
            },
            {
                "photographer_id": 3,
                "business_name": "Candid Moments Studio",
                "styles": "Natural, warm, lifestyle",
                "location": "Bangkok",
                "hourly_rate": 1800,
                "rating": 4.9,
                "email": "candid@moments.com"
            }
        ]
        
        return {
            "photographers": mock_photographers[skip:skip + limit],
            "total": len(mock_photographers)
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get photographers: {e}")
        raise HTTPException(500, f"Error: {str(e)}")
