from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .database import get_db, NewsArticle
from .news_service import news_service
from .ml_service import ml_service
from .config import settings

app = FastAPI(title=settings.PROJECT_NAME)

class ArticleBase(BaseModel):
    title: str
    content: str
    source: str
    url: str

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    published_at: datetime
    sentiment_score: float
    sentiment_label: str
    fake_news_probability: float
    created_at: datetime

    class Config:
        from_attributes = True

@app.post("/analyze", response_model=ArticleResponse)
async def analyze_article(article: ArticleCreate, db: Session = Depends(get_db)):
    """Analyze a single article"""
    analysis = ml_service.analyze_article(article.title, article.content)
    
    db_article = NewsArticle(
        **article.dict(),
        published_at=datetime.utcnow(),
        sentiment_score=analysis['sentiment']['score'],
        sentiment_label=analysis['sentiment']['label'],
        fake_news_probability=analysis['fake_news']['probability']
    )
    
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article

@app.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get analyzed articles"""
    articles = db.query(NewsArticle)\
        .order_by(NewsArticle.published_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return articles

@app.post("/fetch-news")
async def fetch_news(
    query: Optional[str] = None,
    days: int = 1,
    db: Session = Depends(get_db)
):
    """Fetch and analyze new articles"""
    try:
        articles = news_service.fetch_and_process_news(db, query, days)
        return {"message": f"Processed {len(articles)} articles"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))