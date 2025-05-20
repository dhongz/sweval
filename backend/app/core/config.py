from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import secrets
import os
from typing import Dict
from pydantic import BaseModel

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class StripePlans(BaseModel):
    basic: str = ""
    pro: str = ""

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sweval API"
    # API_V1_STR: str = "/api/v1"

    # CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS")
    
    # # Security settings
    # SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    # ALGORITHM: str = "HS256"  # Updated for JWE
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    
    # # JWT Cookie settings
    # AUTHJWT_SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    # AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    # AUTHJWT_COOKIE_SECURE: bool = True
    # AUTHJWT_COOKIE_CSRF_PROTECT: bool = True
    # AUTHJWT_COOKIE_SAMESITE: str = "lax"
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    # LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    # LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT")
    # LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT")
    # LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false") == "true"
    
    # # Database and Services
    # DATABASE_URL: str = os.getenv("DATABASE_URL")
    # GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

    # REDIS_URL: str = os.getenv("REDIS_URL")
    # DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY")

    # RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    # RESEND_FROM_EMAIL: str = os.getenv("RESEND_FROM_EMAIL")

    # AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    # AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    # AWS_REGION: str = os.getenv("AWS_REGION")
    # S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")

    # GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    # GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    # GOOGLE_PUBSUB_TOPIC: str = os.getenv("GOOGLE_PUBSUB_TOPIC")
    
    # FRONTEND_URL: str = os.getenv("FRONTEND_URL")
    # BACKEND_URL: str = os.getenv("BACKEND_URL")

    # # Stripe
    # STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    # STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    # STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")

    # @property
    # def STRIPE_PLAN_IDS(self) -> Dict[str, str]:
    #     return {
    #         "basic": os.getenv("STRIPE_BASIC_PLAN_ID", ""),
    #         "pro": os.getenv("STRIPE_PRO_PLAN_ID", "")
    #     }

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # This tells Pydantic to ignore extra fields

settings = Settings()