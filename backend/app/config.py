"""Application configuration management."""
import json
import os
from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "SnapBuddy"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str
    GCS_BUCKET_NAME: str
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS_JSON: Optional[str] = None

    # Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_MAX_RETRIES: int = 3
    GEMINI_TIMEOUT: int = 30

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "photographer_embeddings"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google Maps
    GOOGLE_MAPS_API_KEY: str

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png,webp"

    # AI Models
    CLIP_MODEL_NAME: str = "openai/clip-vit-large-patch14"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Matching Algorithm
    STYLE_WEIGHT: float = 0.40
    PERFORMANCE_WEIGHT: float = 0.25
    BUDGET_WEIGHT: float = 0.15
    AVAILABILITY_WEIGHT: float = 0.10
    DISTANCE_WEIGHT: float = 0.10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions into list."""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]

    def get_google_credentials(self) -> Optional[dict]:
        """Get Google credentials as dict."""
        if self.GOOGLE_APPLICATION_CREDENTIALS_JSON:
            try:
                return json.loads(self.GOOGLE_APPLICATION_CREDENTIALS_JSON)
            except json.JSONDecodeError:
                pass
        return None

    @property
    def qdrant_connection_url(self) -> str:
        """Get Qdrant connection URL."""
        if self.QDRANT_URL:
            return self.QDRANT_URL
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
