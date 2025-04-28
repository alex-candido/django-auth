# django_app/config.py

from typing import List
from pydantic_settings import BaseSettings
import dj_database_url

class ConfigService(BaseSettings):
    # Django Core Settings
    DEBUG: bool = True
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Environment Settings
    ENVIRONMENT: str = "development"
    
    # Database Settings
    DATABASE_URL: str = ""
    
    @property
    def DATABASE_CONFIG(self) -> dict:
        if self.ENVIRONMENT.lower() == "development":
            return dj_database_url.parse("sqlite:///db.sqlite3")
        return dj_database_url.parse(self.DATABASE_URL)
    
    # JWT Settings
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES: int = 5
    JWT_REFRESH_TOKEN_LIFETIME_DAYS: int = 1
    JWT_ALGORITHM: str = "HS256"
    
    # CORS Settings
    CORS_ALLOW_ALL_ORIGINS: bool = True
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    class Config:
        env_file = "envs/.env"
        case_sensitive = True
