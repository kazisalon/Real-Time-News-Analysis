from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./news.db")

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "News Analyzer"

    # ML Model Settings
    SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    FAKE_NEWS_MODEL: str = "facebook/bart-large-mnli"

    # News API Settings
    NEWS_LANGUAGE: str = "en"
    NEWS_SORT_BY: str = "publishedAt"

    class Config:
        case_sensitive = True


settings = Settings()
