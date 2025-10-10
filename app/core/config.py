from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    """Application settings."""
    
    # Database
    database_url: str = "sqlite:///./data.db"
    
    # API
    api_title: str = "JSON Storage API"
    api_description: str = "A FastAPI application for storing and managing JSON data with update limits"
    api_version: str = "1.0.0"
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    
    # CORS
    cors_origins: list = ["*"]
    cors_credentials: bool = True
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    # Update limits
    default_max_updates: int = 50
    min_max_updates: int = 1
    max_max_updates: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
