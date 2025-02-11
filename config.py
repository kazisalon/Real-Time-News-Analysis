from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news.db")
    MODEL_PATH = "ml_models/saved_models"
    API_PREFIX = "/api/v1"
