from transformers import pipeline
from .config import settings


class MLService:
    """Service for ML models (sentiment analysis and fake news detection)"""

    def __init__(self):
        # Initialize sentiment analysis model
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", model=settings.SENTIMENT_MODEL
        )

        # Initialize fake news detection model
        self.fake_news_detector = pipeline(
            "text-classification", model=settings.FAKE_NEWS_MODEL
        )

    def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of given text"""
        result = self.sentiment_analyzer(text)[0]
        return {"score": float(result["score"]), "label": result["label"]}

    def detect_fake_news(self, text: str) -> dict:
        """Detect if news might be fake"""
        result = self.fake_news_detector(
            text, candidate_labels=["reliable", "unreliable"]
        )
        return {"probability": float(result["scores"][0]), "label": result["labels"][0]}

    def analyze_article(self, title: str, content: str) -> dict:
        """Analyze both sentiment and fake news probability"""
        # Combine title and content for better analysis
        full_text = f"{title} {content}"

        sentiment = self.analyze_sentiment(full_text)
        fake_news = self.detect_fake_news(full_text)

        return {"sentiment": sentiment, "fake_news": fake_news}


# Create singleton instance
ml_service = MLService()
