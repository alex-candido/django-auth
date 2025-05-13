# django_app/__shared/config.py

from typing import List
from pydantic_settings import BaseSettings
import dj_database_url

class ConfigService(BaseSettings):
    # Django Core Settings
    DEBUG: bool = True
    SECRET_KEY: str = ""
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Environment Settings
    ENVIRONMENT: str = "development"
    
    # Database Settings
    DATABASE_URL: str = ""
    
    @property
    def DATABASE_CONFIG(self) -> dict:
        if self.ENVIRONMENT.lower() == "development":
            return dj_database_url.parse("sqlite:///db.sqlite3")
        if self.ENVIRONMENT.lower() == "production" and self.DATABASE_URL:
            return dj_database_url.parse(self.DATABASE_URL)
        raise ValueError("DATABASE_URL must be set for production environment.")

    
    # JWT Settings
    JWT_SECRET_KEY: str = ""
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES: int = 5
    JWT_REFRESH_TOKEN_LIFETIME_DAYS: int = 1
    JWT_ALGORITHM: str = "HS256"
    
    # CORS Settings
    CORS_ALLOW_ALL_ORIGINS: bool = True
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000"
    ]
    
    # Email Settings
    EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST: str = "smtp-relay.sendinblue.com"
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = "alex.candido.tec@gmail.com"
    
        # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"  # URL of the frontend (for redirects, etc.)
    
    # Allauth Settings
    ACCOUNT_EMAIL_VERIFICATION: str = 'mandatory'  # Email verification is mandatory
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION: bool = False  # Do not log in automatically after email confirmation
    ACCOUNT_UNIQUE_EMAIL: bool = True  # Enforce unique email addresses for accounts
    ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS: bool = True  # Redirect after login for authenticated users
    ACCOUNT_AUTHENTICATED_REMEMBER: bool = True  # Remember login for authenticated users
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS: int = 3  # Email confirmation link expiration time in days
    ACCOUNT_EMAIL_SUBJECT_PREFIX: str = '[MyProject] '  # Prefix for all outgoing emails
    ACCOUNT_PASSWORD_MIN_LENGTH: int = 8  # Minimum password length for users
    ACCOUNT_CONFIRM_EMAIL_ON_GET: bool = True  # Confirm email when accessed via GET request
    ACCOUNT_DEFAULT_HTTP_PROTOCOL: str = 'https'  # Default HTTP protocol (use 'https' in production)
    
    # Allauth Sign-up Fields
    ACCOUNT_SIGNUP_FIELDS: List[str] = ['email*', 'username*', 'password1*', 'password2*']  # Required fields for sign-up

    # Email Confirmation Redirects
    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL: str = f"{FRONTEND_URL}/auth/sign-in"  # Redirect for unauthenticated users after email confirmation
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL: str = f"{FRONTEND_URL}/app"  # Redirect for authenticated users after email confirmation
    
    # Login/Logout Redirect URLs
    LOGIN_REDIRECT_URL: str = f"{FRONTEND_URL}/app"  # URL to redirect after login
    LOGOUT_REDIRECT_URL: str = f"{FRONTEND_URL}/auth/sign-in"  # URL to redirect after logout
    LOGIN_URL: str = f"{FRONTEND_URL}/auth/sign-in"  # URL to redirect users for login
    PASSWORD_RESET_USE_SITES_DOMAIN: bool = False
    RESET_PASSWORD_REDIRECT_URL: str = f"{FRONTEND_URL}/auth/reset-password"

    class Config:
        env_file = "envs/.env"  # Path to the environment variables file
        case_sensitive = True
