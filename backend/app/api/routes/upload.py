"""File upload routes."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.upload_service import upload_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/reference-images")
async def upload_reference_images(files: List[UploadFile] = File(...)):
    # ✅ ไม่มี current_user parameter
    
    """Upload reference images (no AI processing needed)."""
    if len(files) > 5:
        raise HTTPException(400, "Maximum 5 images allowed")
    
    results = []
    
    for file in files:
        # Validate file
        if not file.content_type.startswith('image/'):
            continue
        
        # Read file
        content = await file.read()
        
        # Create temporary URL (base64)
        import base64
        b64_data = base64.b64encode(content).decode('utf-8')
        data_url = f"data:{file.content_type};base64,{b64_data}"
        
        results.append({
            "filename": file.filename,
            "url": data_url,
            "content_type": file.content_type,
            "size": len(content)
        })
    
    return {"images": results}
