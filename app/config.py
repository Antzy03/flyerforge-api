"""Configuration settings for FlyerForge API."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Info
    app_name: str = "FlyerForge API"
    app_version: str = "1.0.0"
    
    # Pollinations API Key (required)
    pollinations_api_key: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
