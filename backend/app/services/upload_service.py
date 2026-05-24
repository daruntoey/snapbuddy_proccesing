"""File upload service."""
from typing import List
from fastapi import UploadFile
from google.cloud import storage
import uuid

from app.config import settings

class UploadService:
    def __init__(self):
        # Initialize GCS client
        self.bucket_name = settings.GCS_BUCKET_NAME

    async def upload_reference_images(self, files: List[UploadFile], user_id: int, db):
        """Upload images to GCS."""
        uploaded_urls = []
        
        for file in files:
            # Generate unique filename
            file_ext = file.filename.split('.')[-1]
            unique_filename = f"users/{user_id}/references/{uuid.uuid4()}.{file_ext}"
            
            # For now, return mock URLs
            # In production, upload to GCS
            mock_url = f"https://storage.googleapis.com/{self.bucket_name}/{unique_filename}"
            uploaded_urls.append(mock_url)
        
        return uploaded_urls

upload_service = UploadService()
