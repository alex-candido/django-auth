# django_app/config.py

from typing import List
from pydantic_settings import BaseSettings
import dj_database_url

class ConfigService(BaseSettings):
    # Django Core Settings
    DEBUG: bool = True
    SECRET_KEY: str = "default_secret_key" 
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
    JWT_SECRET_KEY: str = "default_jwt_secret_key"
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES: int = 5
    JWT_REFRESH_TOKEN_LIFETIME_DAYS: int = 1
    JWT_ALGORITHM: str = "HS256"
    
    # CORS Settings
    CORS_ALLOW_ALL_ORIGINS: bool = True
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Email Settings - Configuração para Brevo (sem hardcode de credenciais)
    EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST: str = "smtp-relay.brevo.com"  # Servidor SMTP do Brevo
    EMAIL_PORT: int = 587  # Porta para TLS
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""  # A variável será lida do arquivo .env
    EMAIL_HOST_PASSWORD: str = ""  # A chave de API do Brevo será lida do arquivo .env
    DEFAULT_FROM_EMAIL: str = "alex.candido.tec@gmail.com"
    
    # Frontend URL (para links em emails)
    FRONTEND_URL: str = "http://localhost:3000"
    
    class Config:
        env_file = "envs/.env"  # Caminho para o arquivo de variáveis de ambiente
        case_sensitive = True

