"""Buddy/Photographer routes — reads from buddyProfile + buddyPortfolio sheets."""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.services.sheets_service import sheets_service

router = APIRouter()


@router.get("")
async def list_buddies(
    style: Optional[str] = Query(None, description="กรองตามสไตล์ เช่น 'Korean Soft'"),
    min_rating: Optional[float] = Query(None, description="คะแนน minimum เช่น 4.5"),
    city: Optional[str] = Query(None, description="เมือง เช่น 'Bangkok'"),
):
    """List all buddies from the buddyProfile sheet with optional filters."""
    buddies = await sheets_service.get_buddies(
        style=style,
        min_rating=min_rating,
        city=city,
    )
    return {"buddies": buddies, "total": len(buddies)}


@router.get("/{buddy_id}")
async def get_buddy(buddy_id: str):
    """Get a single buddy profile + portfolio by buddy_id."""
    buddy = await sheets_service.get_buddy_by_id(buddy_id)
    if not buddy:
        raise HTTPException(status_code=404, detail=f"Buddy '{buddy_id}' not found")

    portfolio = await sheets_service.get_portfolio(buddy_id)
    return {**buddy, "portfolio": portfolio}
