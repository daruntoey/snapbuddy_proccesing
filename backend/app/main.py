"""SnapBuddy FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger

from app.config import settings
from app.database import init_db, close_db
from app.api.routes import auth, upload, analysis, matching, photographers, bookings, users

# Lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting SnapBuddy API...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Cleanup
    logger.info("Shutting down...")
    await close_db()

# Create FastAPI app
app = FastAPI(
    title="SnapBuddy API",
    description="AI-Powered Aesthetic Photography Matching Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["AI Analysis"])
app.include_router(matching.router, prefix="/api/matching", tags=["Matching"])
app.include_router(photographers.router, prefix="/api/photographers", tags=["Photographers"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SnapBuddy API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
