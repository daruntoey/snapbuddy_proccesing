"""Photographer repository."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.photographer import Photographer

class PhotographerRepository:
    async def get_by_id(self, db: AsyncSession, photographer_id: int) -> Optional[Photographer]:
        result = await db.execute(select(Photographer).where(Photographer.id == photographer_id))
        return result.scalar_one_or_none()

    async def list_photographers(
        self, db: AsyncSession, skip: int = 0, limit: int = 20, style: Optional[str] = None
    ) -> List[Photographer]:
        query = select(Photographer).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

photographer_repo = PhotographerRepository()
