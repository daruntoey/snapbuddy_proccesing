"""Google Sheets service — reads buddyProfile and buddyPortfolio sheets."""
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
from loguru import logger
import json
import os


class GoogleSheetsService:
    """Service for interacting with Google Sheets."""

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    def __init__(self):
        self.client = None
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        self._spreadsheet = None
        self._init_client()

    def _init_client(self):
        creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if not creds_json:
            logger.warning("⚠️  GOOGLE_APPLICATION_CREDENTIALS_JSON not set — using mock data")
            return
        try:
            creds_dict = json.loads(creds_json)
            credentials = Credentials.from_service_account_info(creds_dict, scopes=self.SCOPES)
            self.client = gspread.authorize(credentials)
            logger.info("✅ Google Sheets client initialised")
        except Exception as e:
            logger.error(f"Failed to init Google Sheets client: {e}")

    def _get_spreadsheet(self):
        if self._spreadsheet:
            return self._spreadsheet
        if not self.client or not self.sheet_id:
            return None
        try:
            self._spreadsheet = self.client.open_by_key(self.sheet_id)
            return self._spreadsheet
        except Exception as e:
            logger.error(f"Cannot open spreadsheet: {e}")
            return None

    def _get_worksheet(self, name: str):
        ss = self._get_spreadsheet()
        if not ss:
            return None
        try:
            return ss.worksheet(name)
        except Exception as e:
            logger.error(f"Cannot open worksheet '{name}': {e}")
            return None

    # ------------------------------------------------------------------
    # buddyProfile
    # ------------------------------------------------------------------
    async def get_buddies(
        self,
        style: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rate: Optional[int] = None,
        city: Optional[str] = None,
    ) -> List[Dict]:
        """
        Fetch buddies from the 'buddyProfile' sheet.

        Columns: buddy_id, user_id, name, nickname, profile_image,
                 phone, email, birth_date, gender, city, bio,
                 experience_year, language, account_status,
                 verification_level, created_at, average_rating,
                 top_styles, portfolio_count
        """
        ws = self._get_worksheet("buddyProfile")
        if not ws:
            logger.warning("buddyProfile sheet unavailable — using mock data")
            return self._mock_buddies()

        try:
            records = ws.get_all_records()
        except Exception as e:
            logger.error(f"Failed to read buddyProfile: {e}")
            return self._mock_buddies()

        results = []
        for r in records:
            # Skip inactive / empty rows
            if r.get("account_status", "").lower() not in ("active", ""):
                continue

            # Rating filter
            try:
                rating = float(r.get("average_rating", 0) or 0)
            except (ValueError, TypeError):
                rating = 0.0
            if min_rating and rating < min_rating:
                continue

            # Style filter (checks top_styles + bio)
            if style:
                haystack = (
                    str(r.get("top_styles", "")).lower()
                    + " "
                    + str(r.get("bio", "")).lower()
                )
                if style.lower() not in haystack:
                    continue

            # City filter
            if city and city.lower() not in str(r.get("city", "")).lower():
                continue

            results.append({
                "buddy_id":        str(r.get("buddy_id", "")),
                "user_id":         str(r.get("user_id", "")),
                "name":            str(r.get("name", "")),
                "nickname":        str(r.get("nickname", "")),
                "profile_image":   str(r.get("profile_image", "")),
                "phone":           str(r.get("phone", "")),
                "email":           str(r.get("email", "")),
                "city":            str(r.get("city", "")),
                "bio":             str(r.get("bio", "")),
                "experience_year": int(r.get("experience_year", 0) or 0),
                "language":        str(r.get("language", "Thai, English")),
                "account_status":  str(r.get("account_status", "Active")),
                "average_rating":  rating,
                "top_styles":      str(r.get("top_styles", "")),
                "portfolio_count": int(r.get("portfolio_count", 0) or 0),
            })

        logger.info(f"buddyProfile → {len(results)} buddies (filtered)")
        return results

    async def get_buddy_by_id(self, buddy_id: str) -> Optional[Dict]:
        buddies = await self.get_buddies()
        for b in buddies:
            if b["buddy_id"] == str(buddy_id):
                return b
        return None

    # ------------------------------------------------------------------
    # buddyPortfolio
    # ------------------------------------------------------------------
    async def get_portfolio(self, buddy_id: Optional[str] = None) -> List[Dict]:
        """
        Fetch rows from the 'buddyPortfolio' sheet.

        Columns: portfolio_id, buddy_id, image_url, category,
                 mood_tag, lighting_tag, pose_style, location_type,
                 edit_style, camera_type, upload_date,
                 engagement_score, hero_shot
        """
        ws = self._get_worksheet("buddyPortfolio")
        if not ws:
            return self._mock_portfolio(buddy_id)

        try:
            records = ws.get_all_records()
        except Exception as e:
            logger.error(f"Failed to read buddyPortfolio: {e}")
            return self._mock_portfolio(buddy_id)

        results = []
        for r in records:
            if buddy_id and str(r.get("buddy_id", "")) != str(buddy_id):
                continue
            results.append({
                "portfolio_id":    str(r.get("portfolio_id", "")),
                "buddy_id":        str(r.get("buddy_id", "")),
                "image_url":       str(r.get("image_url", "")),
                "category":        str(r.get("category", "")),
                "mood_tag":        str(r.get("mood_tag", "")),
                "lighting_tag":    str(r.get("lighting_tag", "")),
                "pose_style":      str(r.get("pose_style", "")),
                "location_type":   str(r.get("location_type", "")),
                "edit_style":      str(r.get("edit_style", "")),
                "camera_type":     str(r.get("camera_type", "")),
                "upload_date":     str(r.get("upload_date", "")),
                "engagement_score": int(r.get("engagement_score", 0) or 0),
                "hero_shot":       str(r.get("hero_shot", "")).upper() == "TRUE",
            })

        return results

    # ------------------------------------------------------------------
    # Build a rich text description of a buddy (for NLP embedding)
    # ------------------------------------------------------------------
    async def get_buddy_embedding_text(self, buddy: Dict) -> str:
        """
        Combine profile + portfolio tags into one descriptive text
        for embedding/similarity purposes.
        """
        portfolio = await self.get_portfolio(buddy["buddy_id"])

        # Collect all unique style signals from portfolio
        mood_tags     = list({p["mood_tag"]     for p in portfolio if p["mood_tag"]})
        lighting_tags = list({p["lighting_tag"] for p in portfolio if p["lighting_tag"]})
        edit_styles   = list({p["edit_style"]   for p in portfolio if p["edit_style"]})
        location_types = list({p["location_type"] for p in portfolio if p["location_type"]})
        categories    = list({p["category"]     for p in portfolio if p["category"]})

        parts = [
            f"ชื่อ: {buddy.get('nickname') or buddy.get('name', '')}",
            f"Bio: {buddy.get('bio', '')}",
            f"สไตล์หลัก: {buddy.get('top_styles', '')}",
            f"ประสบการณ์: {buddy.get('experience_year', 0)} ปี",
            f"เมือง: {buddy.get('city', '')}",
        ]
        if mood_tags:
            parts.append(f"Mood: {', '.join(mood_tags)}")
        if lighting_tags:
            parts.append(f"แสง: {', '.join(lighting_tags)}")
        if edit_styles:
            parts.append(f"สไตล์ตกแต่งภาพ: {', '.join(edit_styles)}")
        if location_types:
            parts.append(f"สถานที่: {', '.join(location_types)}")
        if categories:
            parts.append(f"ประเภทงาน: {', '.join(categories)}")

        return ". ".join(parts)

    # ------------------------------------------------------------------
    # Bookings (write)
    # ------------------------------------------------------------------
    async def add_booking(self, booking_data: Dict) -> Dict:
        """Append a new booking to the Bookings sheet."""
        ws = self._get_worksheet("Bookings")
        if not ws:
            return {"booking_id": "BOOK_MOCK", **booking_data, "status": "confirmed"}

        try:
            records = ws.get_all_records()
            new_id = f"BOOK{len(records) + 1001}"
            row = [
                new_id,
                booking_data.get("seeker_id", ""),
                booking_data.get("buddy_id", ""),
                booking_data.get("booking_date", ""),
                booking_data.get("booking_time", ""),
                booking_data.get("location_name", ""),
                booking_data.get("total_price", 0),
                "pending",
            ]
            ws.append_row(row)
            logger.info(f"✅ Booking {new_id} created")
            return {"booking_id": new_id, **booking_data, "status": "pending"}
        except Exception as e:
            logger.error(f"Failed to create booking: {e}")
            return {"booking_id": "BOOK_MOCK", **booking_data, "status": "confirmed"}

    # ------------------------------------------------------------------
    # Mock data (fallback when Sheets is unavailable)
    # ------------------------------------------------------------------
    def _mock_buddies(self) -> List[Dict]:
        return [
            {
                "buddy_id": "BUD001",
                "user_id": "user01",
                "name": "Thanya K.",
                "nickname": "# T H A N Y A #",
                "profile_image": "/avatar.jpg",
                "phone": "081-234-5678",
                "email": "nat@snapbuddy.com",
                "city": "Bangkok",
                "bio": "ช่างภาพสายคาเฟ่ แสงธรรมชาติ และโทนเกาหลีนุ่ม ๆ เน้นเก็บรอยยิ้มที่เป็นธรรมชาติที่สุด",
                "experience_year": 4,
                "language": "Thai, English",
                "account_status": "Active",
                "average_rating": 4.9,
                "top_styles": "Korean Soft, Candid, Sun-kissed Cafe",
                "portfolio_count": 142,
            },
            {
                "buddy_id": "BUD002",
                "user_id": "user05",
                "name": "ทินประภา",
                "nickname": "thinprapa",
                "profile_image": "",
                "phone": "081-234-5682",
                "email": "",
                "city": "Bangkok",
                "bio": "รับจ้างเพื่อนถ่ายรูปดิจิตอล/ไอโฟน ถ่ายงานรับปริญญา คาเฟ่ ร้านอาหาร สถานที่ท่องเที่ยว หน้าคอนเสิร์ต",
                "experience_year": 2,
                "language": "Thai, English",
                "account_status": "Active",
                "average_rating": 4.8,
                "top_styles": "Cafe, Digital Camera, Graduation, Lifestyle, Travel",
                "portfolio_count": 57,
            },
            {
                "buddy_id": "BUD003",
                "user_id": "user06",
                "name": "Iam",
                "nickname": "sudarat.sy",
                "profile_image": "",
                "phone": "081-234-5683",
                "email": "",
                "city": "สมุทรปราการ",
                "bio": "เช่าเพื่อนถ่ายรูป/คาเฟ่/แหล่งท่องเที่ยว",
                "experience_year": 3,
                "language": "Thai, English",
                "account_status": "Active",
                "average_rating": 4.9,
                "top_styles": "Cafe, Lifestyle, Travel",
                "portfolio_count": 28,
            },
        ]

    def _mock_portfolio(self, buddy_id: Optional[str] = None) -> List[Dict]:
        items = [
            {
                "portfolio_id": "PORT001",
                "buddy_id": "BUD001",
                "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
                "category": "Cafe Portrait",
                "mood_tag": "Korean Soft",
                "lighting_tag": "Morning Light",
                "pose_style": "Candid",
                "location_type": "Cafe",
                "edit_style": "Warm Pastel",
                "camera_type": "Sony A7IV",
                "upload_date": "2026-05-01",
                "engagement_score": 95,
                "hero_shot": True,
            },
            {
                "portfolio_id": "PORT005",
                "buddy_id": "BUD001",
                "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb",
                "category": "Close-up Portrait",
                "mood_tag": "Candid",
                "lighting_tag": "Natural Light",
                "pose_style": "Candid",
                "location_type": "Outdoor",
                "edit_style": "Film Tone",
                "camera_type": "Canon R6",
                "upload_date": "2026-05-15",
                "engagement_score": 98,
                "hero_shot": True,
            },
        ]
        if buddy_id:
            return [p for p in items if p["buddy_id"] == buddy_id]
        return items


# Global singleton
sheets_service = GoogleSheetsService()
