"""Photographers routes using Google Sheets."""
from fastapi import APIRouter, Query
from typing import Optional

from app.services.sheets_service import sheets_service

router = APIRouter()


@router.get("")
async def get_photographers(
    style: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None),
    max_rate: Optional[int] = Query(None),
):
    """Get photographers from Google Sheets."""
    photographers = await sheets_service.get_photographers(
        style=style,
        min_rating=min_rating,
        max_rate=max_rate
    )
    return {"photographers": photographers, "total": len(photographers)}


@router.get("/{photographer_id}")
async def get_photographer(photographer_id: int):
    """Get photographer by ID."""
    photographer = await sheets_service.get_photographer_by_id(photographer_id)
    if not photographer:
        return {"error": "Photographer not found"}, 404
    return photographer
