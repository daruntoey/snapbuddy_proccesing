"""Matching routes."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/match")
async def match_photographers(request: dict):
    """Match photographers - mock data."""
    
    matches = [
        {
            "photographer_id": 1,
            "business_name": "Bangkok Studio Photography",
            "hourly_rate": 2000,
            "rating": 4.8,
            "styles": "Korean cafe, natural light",
            "match_score": 95.5,
            "explanation": "Perfect for Korean cafe aesthetic"
        },
        {
            "photographer_id": 2,
            "business_name": "Urban Light Photography",
            "hourly_rate": 2500,
            "rating": 4.7,
            "styles": "Minimalist, bright",
            "match_score": 88.2,
            "explanation": "Great for clean aesthetic"
        },
        {
            "photographer_id": 3,
            "business_name": "Candid Moments Studio",
            "hourly_rate": 1800,
            "rating": 4.9,
            "styles": "Natural, warm",
            "match_score": 82.7,
            "explanation": "Best for authentic shots"
        }
    ]
    
    return {
        "matches": matches,
        "total": 3,
        "status": "success"
    }


@router.get("/photographers")
async def get_photographers():
    """Get all photographers."""
    
    photographers = [
        {
            "photographer_id": 1,
            "business_name": "Bangkok Studio Photography",
            "hourly_rate": 2000,
            "rating": 4.8
        },
        {
            "photographer_id": 2,
            "business_name": "Urban Light Photography",
            "hourly_rate": 2500,
            "rating": 4.7
        },
        {
            "photographer_id": 3,
            "business_name": "Candid Moments Studio",
            "hourly_rate": 1800,
            "rating": 4.9
        }
    ]
    
    return {
        "photographers": photographers,
        "total": 3
    }
