from newsapi import NewsApiClient
from datetime import datetime, timedelta
from .config import settings
from .database import NewsArticle
from .ml_service import ml_service
from sqlalchemy.orm import Session

class NewsService:
    """Service for fetching and processing news"""
    
    def __init__(self):
        self.api = NewsApiClient(api_key=settings.NEWS_API_KEY)
    
    def fetch_latest_news(self, query: str = None, days: int = 1) -> list:
        """Fetch latest news articles"""
        from_date = datetime.now() - timedelta(days=days)
        
        response = self.api.get_everything(
            q=query,
            from_param=from_date.strftime('%Y-%m-%d'),
            language=settings.NEWS_LANGUAGE,
            sort_by=settings.NEWS_SORT_BY
        )
        
        return response['articles']
    
    def process_article(self, article: dict, db: Session) -> NewsArticle:
        """Process a single article with ML analysis and save to database"""
        # Analyze article
        analysis = ml_service.analyze_article(
            article['title'],
            article['content'] or article['description']
        )
        
        # Create database entry
        db_article = NewsArticle(
            title=article['title'],
            content=article['content'] or article['description'],
            source=article['source']['name'],
            url=article['url'],
            published_at=datetime.strptime(
                article['publishedAt'],
                '%Y-%m-%dT%H:%M:%SZ'
            ),
            sentiment_score=analysis['sentiment']['score'],
            sentiment_label=analysis['sentiment']['label'],
            fake_news_probability=analysis['fake_news']['probability']
        )
        
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        
        return db_article
    
    def fetch_and_process_news(self, db: Session, query: str = None, days: int = 1) -> list:
        """Fetch latest news and process all articles"""
        articles = self.fetch_latest_news(query, days)
        processed_articles = []
        
        for article in articles:
            try:
                processed = self.process_article(article, db)
                processed_articles.append(processed)
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
        
        return processed_articles

# Create singleton instance
news_service = NewsService()