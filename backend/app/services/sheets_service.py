"""Google Sheets service for data storage."""
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
from loguru import logger
import json
import os

class GoogleSheetsService:
    """Service for interacting with Google Sheets."""
    
    def __init__(self):
        """Initialize Google Sheets client."""
        try:
            # Load credentials from environment variable
            creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if creds_json:
                creds_dict = json.loads(creds_json)
                credentials = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive.readonly'
                    ]
                )
                self.client = gspread.authorize(credentials)
                logger.info("✅ Google Sheets client initialized")
            else:
                self.client = None
                logger.warning("⚠️ No Google credentials found")
                
            self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets: {e}")
            self.client = None
    
    def get_sheet(self, sheet_name: str):
        """Get worksheet by name."""
        if not self.client or not self.sheet_id:
            return None
        try:
            spreadsheet = self.client.open_by_key(self.sheet_id)
            return spreadsheet.worksheet(sheet_name)
        except Exception as e:
            logger.error(f"Failed to open sheet {sheet_name}: {e}")
            return None
    
    async def get_photographers(
        self, 
        style: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rate: Optional[int] = None
    ) -> List[Dict]:
        """Get photographers from Google Sheets with filters."""
        try:
            worksheet = self.get_sheet('Photographers')
            if not worksheet:
                return self._get_mock_photographers()
            
            # Get all records
            records = worksheet.get_all_records()
            
            # Apply filters
            filtered = []
            for record in records:
                # Filter by style
                if style and style.lower() not in record.get('styles', '').lower():
                    continue
                
                # Filter by rating
                if min_rating and record.get('rating', 0) < min_rating:
                    continue
                
                # Filter by hourly rate
                if max_rate and record.get('hourly_rate', 0) > max_rate:
                    continue
                
                filtered.append(record)
            
            logger.info(f"Found {len(filtered)} photographers")
            return filtered
            
        except Exception as e:
            logger.error(f"Failed to get photographers: {e}")
            return self._get_mock_photographers()
    
    async def get_photographer_by_id(self, photographer_id: int) -> Optional[Dict]:
        """Get single photographer by ID."""
        try:
            photographers = await self.get_photographers()
            for p in photographers:
                if p.get('photographer_id') == photographer_id:
                    return p
            return None
        except Exception as e:
            logger.error(f"Failed to get photographer {photographer_id}: {e}")
            return None
    
    async def add_booking(self, booking_data: Dict) -> Dict:
        """Add new booking to Bookings sheet."""
        try:
            worksheet = self.get_sheet('Bookings')
            if not worksheet:
                return {"booking_id": 1, **booking_data, "status": "confirmed"}
            
            # Generate new booking ID
            records = worksheet.get_all_records()
            new_id = max([r.get('booking_id', 0) for r in records], default=0) + 1
            
            # Prepare row data
            row = [
                new_id,
                booking_data.get('user_email'),
                booking_data.get('photographer_id'),
                booking_data.get('booking_date'),
                booking_data.get('duration'),
                booking_data.get('location'),
                'pending'
            ]
            
            # Append row
            worksheet.append_row(row)
            logger.info(f"✅ Booking {new_id} created")
            
            return {"booking_id": new_id, **booking_data, "status": "pending"}
            
        except Exception as e:
            logger.error(f"Failed to create booking: {e}")
            return {"booking_id": 1, **booking_data, "status": "confirmed"}
    
    def _get_mock_photographers(self) -> List[Dict]:
        """Return mock photographers data."""
        return [
            {
                "photographer_id": 1,
                "business_name": "Bangkok Studio Photography",
                "bio": "Specializing in Korean cafe aesthetic",
                "location": "Bangkok",
                "hourly_rate": 2000,
                "styles": "Korean cafe, natural light, cozy",
                "rating": 4.8,
                "phone": "081-234-5678",
                "email": "bangkok@studio.com"
            },
            {
                "photographer_id": 2,
                "business_name": "Urban Light Photography",
                "bio": "Bright and airy minimalist photography",
                "location": "Bangkok",
                "hourly_rate": 2500,
                "styles": "Minimalist, bright, editorial",
                "rating": 4.7,
                "phone": "082-345-6789",
                "email": "urban@light.com"
            },
            {
                "photographer_id": 3,
                "business_name": "Candid Moments Studio",
                "bio": "Natural and warm lifestyle photography",
                "location": "Bangkok",
                "hourly_rate": 1800,
                "styles": "Natural, warm, lifestyle, candid",
                "rating": 4.9,
                "phone": "083-456-7890",
                "email": "candid@moments.com"
            }
        ]

# Global instance
sheets_service = GoogleSheetsService()
