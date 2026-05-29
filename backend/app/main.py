"""SnapBuddy FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
import time

from app.config import settings
from app.database import init_db, close_db
from app.api.routes import auth, upload, analysis, matching, photographers, bookings, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting SnapBuddy API...")
    settings.validate_critical()
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield

    logger.info("Shutting down...")
    try:
        await close_db()
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")


app = FastAPI(
    title="SnapBuddy API",
    description="AI-Powered Aesthetic Photography Matching Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow all Vercel preview URLs + configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["AI Analysis"])
app.include_router(matching.router, prefix="/api/matching", tags=["Matching"])
app.include_router(photographers.router, prefix="/api/photographers", tags=["Photographers"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def root():
    return {"message": "SnapBuddy API", "version": "1.0.0", "docs": "/docs", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT, "api_version": "1.0.0"}


@app.get("/debug/gemini")
async def debug_gemini():
    """Test Gemini connection directly."""
    from app.ai.gemini_service import gemini_service
    start = time.time()
    result = await gemini_service.generate_content(
        'Reply ONLY with this JSON: {"status":"ok","model":"working"}'
    )
    elapsed = round(time.time() - start, 2)
    return {
        "elapsed_seconds": elapsed,
        "raw_response": result[:200],
        "is_mock": '"mock"' in result,
        "api_key_length": len(gemini_service.api_key),
        "working_url": gemini_service.working_url,
    }

@app.get("/debug/gemini-models")
async def debug_gemini_models():
    """List available Gemini models for this API key."""
    import requests
    from app.ai.gemini_service import gemini_service
    
    resp = requests.get(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_service.api_key}",
        timeout=10
    )
    if resp.status_code == 200:
        data = resp.json()
        models = [m["name"] for m in data.get("models", []) 
                  if "generateContent" in m.get("supportedGenerationMethods", [])]
        return {"status": "ok", "available_models": models}
    return {"status": "error", "code": resp.status_code, "body": resp.text[:300]}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
