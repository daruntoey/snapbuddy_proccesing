"""File upload routes."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.upload_service import upload_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/reference-images")
async def upload_reference_images(
    files: List[UploadFile] = File(...),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload reference images for aesthetic analysis."""
    if len(files) > 5:
        raise HTTPException(400, "Maximum 5 images allowed")
    
    results = await upload_service.upload_reference_images(files, current_user.id, db)
    return {"images": results}
