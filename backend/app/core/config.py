from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "PlacementPilot"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(
        default="dev_secret_key_change_in_production_min32chars_placementpilot",
        description="Secret key for JWT generation and cryptographic operations"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ALGORITHM: str = "HS256"
    
    # Rate Limiting (Brute-force protection on auth endpoints)
    RATE_LIMIT_LOGIN_ATTEMPTS: int = 5
    RATE_LIMIT_WINDOW_SECONDS: int = 300  # 5 minutes lockout window
    
    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    
    @property
    def cors_origins(self) -> List[str]:
        origins = [self.FRONTEND_ORIGIN.strip()]
        if "http://localhost:3000" not in origins:
            origins.append("http://localhost:3000")
        if "http://127.0.0.1:5173" not in origins:
            origins.append("http://127.0.0.1:5173")
        return origins

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/placementpilot_db",
        description="PostgreSQL connection string"
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Storage
    STORAGE_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "storage")
    MAX_UPLOAD_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

    # AI Configuration
    AI_PROVIDER: str = "mock"  # gemini, openai, anthropic, mock
    AI_API_KEY: str = ""
    AI_MODEL: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
