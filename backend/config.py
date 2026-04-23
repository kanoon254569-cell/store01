"""Configuration Management"""
import os
from pydantic_settings import BaseSettings
from pydantic import field_validator


def _coerce_debug(value) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on", "debug", "dev", "development"}:
        return True
    if normalized in {"0", "false", "no", "off", "release", "prod", "production"}:
        return False
    return True

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "ecommerce_db"
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = 60
    PURCHASE_LIMIT_PER_MINUTE: int = 5  # ป้องกัน double purchase
    
    # Server
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        return _coerce_debug(value)
    
    class Config:
        env_file = ".env"

settings = Settings()
