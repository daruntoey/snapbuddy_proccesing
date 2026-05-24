# SnapBuddy API Documentation

Complete REST API reference for SnapBuddy platform.

**Base URL**: `https://snapbuddy-backend.onrender.com` (Production)  
**Base URL**: `http://localhost:8000` (Development)

**API Version**: 1.0.0  
**Authentication**: Bearer Token (JWT)

## Interactive Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Register

Create a new user account.

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Login

Authenticate and receive access token.

**Endpoint**: `POST /api/auth/login`

**Request Body** (Form Data):
```
username=user@example.com
password=SecurePassword123!
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## Upload

### Upload Reference Images

Upload aesthetic reference images for analysis.

**Endpoint**: `POST /api/upload/reference-images`  
**Authentication**: Required

**Request**: `multipart/form-data`
```
files: [File, File, ...] (max 5 images)
```

**Response**: `200 OK`
```json
{
  "images": [
    {
      "url": "https://storage.googleapis.com/snapbuddy-uploads/...",
      "thumbnail": "https://storage.googleapis.com/...",
      "size": 1024000
    }
  ]
}
```

**Limits**:
- Maximum 5 images per request
- Maximum 10MB per image
- Supported formats: JPG, JPEG, PNG, WEBP

## AI Analysis

### Analyze Mood

Extract aesthetic preferences from text and images.

**Endpoint**: `POST /api/analysis/mood`  
**Authentication**: Required

**Request Body**:
```json
{
  "text_description": "I want a cozy Korean cafe aesthetic with warm natural lighting and minimal poses",
  "image_urls": [
    "https://storage.googleapis.com/snapbuddy-uploads/ref1.jpg",
    "https://storage.googleapis.com/snapbuddy-uploads/ref2.jpg"
  ],
  "budget_min": 100,
  "budget_max": 300,
  "location": "Seoul, South Korea"
}
```

**Response**: `200 OK`
```json
{
  "mood_spec_id": 123,
  "mood_tags": ["cozy", "minimal", "warm", "relaxed"],
  "style_tags": ["Korean cafe aesthetic", "natural light photography"],
  "lighting_preferences": ["natural light", "warm tones", "soft"],
  "location_styles": ["indoor", "cafe", "minimalist"],
  "pose_styles": ["candid", "lifestyle", "relaxed"],
  "color_preferences": ["warm tones", "earth tones", "cream"],
  "detected_intent": "Looking for a professional photographer who specializes in cozy, minimalist cafe photography with warm natural lighting",
  "aesthetic_summary": "Cozy Korean cafe vibe with warm, natural lighting and minimal styling",
  "suggested_poses": [
    "Sitting by window with coffee",
    "Reading at a table",
    "Walking through cafe"
  ],
  "suggested_locations": [
    "Minimalist cafe with large windows",
    "Vintage bookshop cafe",
    "Modern Korean cafe"
  ]
}
```

### Extract Embeddings

Extract CLIP embeddings from images.

**Endpoint**: `POST /api/analysis/extract-embedding`  
**Authentication**: Required

**Request Body**:
```json
{
  "image_urls": [
    "https://storage.googleapis.com/snapbuddy-uploads/image1.jpg"
  ]
}
```

**Response**: `200 OK`
```json
{
  "embeddings": [
    {
      "url": "https://...",
      "embedding": [0.123, -0.456, ...],  // 512-dim vector
      "style_scores": {
        "Korean cafe aesthetic": 0.92,
        "minimal photography": 0.85,
        "natural light": 0.88
      },
      "lighting_type": "natural light",
      "color_palette": ["#F5F5DC", "#8B7355", "#D2B48C"]
    }
  ]
}
```

## Matching

### Match Photographers

Find photographers matching aesthetic preferences.

**Endpoint**: `POST /api/matching/match-photographers`  
**Authentication**: Required

**Request Body**:
```json
{
  "mood_spec_id": 123,
  "limit": 10,
  "filters": {
    "budget_max": 300,
    "max_distance_km": 50,
    "min_rating": 4.0,
    "available_dates": ["2026-06-01", "2026-06-02"]
  }
}
```

**Response**: `200 OK`
```json
{
  "matches": [
    {
      "photographer_id": 456,
      "business_name": "Seoul Moments Studio",
      "match_score": 95.5,
      "style_similarity_score": 98.0,
      "performance_score": 92.5,
      "budget_fit_score": 95.0,
      "availability_score": 100.0,
      "distance_score": 90.0,
      "explanation": "Perfect match for Korean cafe aesthetic. This photographer specializes in warm, natural light portraits and has extensive experience shooting in minimalist cafe settings. Their portfolio shows strong alignment with your desired cozy, intimate vibe.",
      "satisfaction_probability": 0.94,
      "booking_probability": 0.78,
      "profile_image": "https://...",
      "hourly_rate": 150,
      "average_rating": 4.9,
      "total_reviews": 87,
      "location": "Gangnam, Seoul",
      "distance_km": 5.2,
      "portfolio_highlights": [
        {
          "image_url": "https://...",
          "similarity_score": 0.96,
          "description": "Cafe lifestyle shoot"
        }
      ],
      "available_dates": ["2026-06-01", "2026-06-03"],
      "response_time_hours": 2.5
    }
  ],
  "total": 15,
  "filters_applied": {
    "budget_max": 300,
    "max_distance": 50,
    "min_rating": 4.0
  }
}
```

**Matching Algorithm**:
```
Final Score = (0.40 × Style Similarity) + 
              (0.25 × Historical Performance) + 
              (0.15 × Budget Fit) + 
              (0.10 × Availability) + 
              (0.10 × Distance Match)
```

### Get Recommendations

Retrieve saved recommendations for a mood specification.

**Endpoint**: `GET /api/matching/recommendations/{mood_spec_id}`  
**Authentication**: Required

**Response**: `200 OK`
```json
{
  "mood_spec_id": 123,
  "recommendations": [...],  // Same as matches array above
  "created_at": "2026-05-24T10:00:00Z",
  "expires_at": "2026-05-31T10:00:00Z"
}
```

## Photographers

### Get Photographer Profile

Get detailed photographer profile.

**Endpoint**: `GET /api/photographers/{photographer_id}`

**Response**: `200 OK`
```json
{
  "id": 456,
  "business_name": "Seoul Moments Studio",
  "bio": "Specializing in lifestyle and portrait photography with a focus on natural light and authentic moments.",
  "profile_image": "https://...",
  "cover_image": "https://...",
  "location": "Gangnam, Seoul",
  "latitude": 37.4979,
  "longitude": 127.0276,
  "service_radius_km": 50,
  "hourly_rate": 150,
  "package_rates": {
    "basic": 200,
    "standard": 350,
    "premium": 500
  },
  "primary_styles": ["Korean cafe aesthetic", "natural light", "lifestyle"],
  "expertise_tags": ["portrait", "couple", "fashion", "editorial"],
  "equipment": {
    "camera": "Canon EOS R5",
    "lenses": ["24-70mm f/2.8", "85mm f/1.4"]
  },
  "average_rating": 4.9,
  "total_reviews": 87,
  "total_bookings": 142,
  "completed_bookings": 138,
  "response_rate": 0.98,
  "response_time_hours": 2.5,
  "is_verified": true,
  "is_featured": true,
  "portfolio": [
    {
      "id": 789,
      "image_url": "https://...",
      "thumbnail_url": "https://...",
      "title": "Cafe Lifestyle Session",
      "style_tags": ["cafe", "natural light", "minimal"],
      "lighting_type": "natural light",
      "color_palette": ["#F5F5DC", "#8B7355"]
    }
  ],
  "recent_reviews": [
    {
      "id": 101,
      "user_name": "Sarah K.",
      "overall_rating": 5.0,
      "style_match_rating": 5.0,
      "review_text": "Amazing experience! The photos captured exactly the aesthetic I wanted.",
      "created_at": "2026-05-20T14:30:00Z"
    }
  ],
  "available_days": ["monday", "tuesday", "wednesday", "friday"],
  "next_available_date": "2026-06-01"
}
```

### List Photographers

Browse all photographers with filtering.

**Endpoint**: `GET /api/photographers`

**Query Parameters**:
- `skip`: Pagination offset (default: 0)
- `limit`: Results per page (default: 20, max: 100)
- `style`: Filter by style tag
- `location`: Filter by location
- `min_rating`: Minimum rating (0-5)
- `max_rate`: Maximum hourly rate

**Example**:
```
GET /api/photographers?style=Korean cafe aesthetic&min_rating=4.5&limit=10
```

**Response**: `200 OK`
```json
{
  "photographers": [...],  // Array of photographer objects
  "total": 42,
  "skip": 0,
  "limit": 10
}
```

## Bookings

### Create Booking

Book a photographer for a photoshoot.

**Endpoint**: `POST /api/bookings`  
**Authentication**: Required

**Request Body**:
```json
{
  "photographer_id": 456,
  "booking_date": "2026-06-01T14:00:00Z",
  "booking_duration_hours": 2,
  "location": "Cafe Onion Anguk, Seoul",
  "latitude": 37.5665,
  "longitude": 126.9780,
  "mood_spec_id": 123,
  "reference_images": [
    "https://storage.googleapis.com/..."
  ],
  "special_requests": "Please bring reflector for window shots"
}
```

**Response**: `201 Created`
```json
{
  "id": 789,
  "photographer_id": 456,
  "booking_date": "2026-06-01T14:00:00Z",
  "booking_duration_hours": 2,
  "location": "Cafe Onion Anguk, Seoul",
  "status": "pending",
  "quoted_price": 300,
  "deposit_amount": 100,
  "created_at": "2026-05-24T10:00:00Z"
}
```

### List User Bookings

Get all bookings for current user.

**Endpoint**: `GET /api/bookings`  
**Authentication**: Required

**Query Parameters**:
- `status`: Filter by status (pending, confirmed, completed, cancelled)

**Response**: `200 OK`
```json
{
  "bookings": [
    {
      "id": 789,
      "photographer": {
        "id": 456,
        "business_name": "Seoul Moments Studio",
        "profile_image": "https://..."
      },
      "booking_date": "2026-06-01T14:00:00Z",
      "status": "confirmed",
      "quoted_price": 300
    }
  ],
  "total": 5
}
```

### Get Booking Details

Get detailed booking information.

**Endpoint**: `GET /api/bookings/{booking_id}`  
**Authentication**: Required

**Response**: `200 OK`
```json
{
  "id": 789,
  "photographer": {...},
  "booking_date": "2026-06-01T14:00:00Z",
  "status": "confirmed",
  "location": "Cafe Onion Anguk, Seoul",
  "quoted_price": 300,
  "mood_spec": {...},
  "reference_images": [...],
  "messages": [
    {
      "from": "photographer",
      "message": "Looking forward to the shoot!",
      "timestamp": "2026-05-24T11:00:00Z"
    }
  ]
}
```

## Users

### Get Current User Profile

Get authenticated user profile.

**Endpoint**: `GET /api/users/me`  
**Authentication**: Required

**Response**: `200 OK`
```json
{
  "id": 123,
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+82-10-1234-5678",
  "profile_image": "https://...",
  "is_photographer": false,
  "is_verified": true,
  "preferred_location": "Seoul",
  "budget_range_min": 100,
  "budget_range_max": 300,
  "preferred_styles": ["cafe aesthetic", "natural light"],
  "created_at": "2026-01-15T08:00:00Z",
  "total_bookings": 3
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request format or parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API requests are rate-limited:
- **Authenticated users**: 1000 requests/hour
- **Anonymous users**: 100 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1622505600
```

## Pagination

List endpoints support pagination:

**Query Parameters**:
- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 20, max: 100)

**Response includes**:
```json
{
  "items": [...],
  "total": 100,
  "skip": 20,
  "limit": 20
}
```

## Webhooks

Configure webhooks to receive real-time updates:

**Events**:
- `booking.created`
- `booking.confirmed`
- `booking.completed`
- `booking.cancelled`
- `review.created`

**Webhook Payload**:
```json
{
  "event": "booking.confirmed",
  "timestamp": "2026-05-24T10:00:00Z",
  "data": {
    "booking_id": 789,
    "photographer_id": 456,
    "user_id": 123
  }
}
```

---

**API Version**: 1.0.0  
**Last Updated**: May 2026  
**Support**: api@snapbuddy.com
