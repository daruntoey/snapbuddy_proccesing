"""Photographer routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.schemas.photographer import PhotographerResponse

router = APIRouter()

@router.get("/{photographer_id}", response_model=PhotographerResponse)
async def get_photographer(
    photographer_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get photographer profile."""
    from app.repositories.photographer_repository import photographer_repo
    photographer = await photographer_repo.get_by_id(db, photographer_id)
    if not photographer:
        raise HTTPException(404, "Photographer not found")
    return photographer

@router.get("/")
async def list_photographers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    style: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List photographers with optional filtering."""
    from app.repositories.photographer_repository import photographer_repo
    photographers = await photographer_repo.list_photographers(db, skip, limit, style)
    return {"photographers": photographers, "total": len(photographers)}
