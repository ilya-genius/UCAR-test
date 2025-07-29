import enum
import re
from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./reviews.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class Sentiment(enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(Enum(Sentiment), nullable=False)
    created_at = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ReviewCreate(BaseModel):
    text: str

class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: Sentiment
    created_at: str

def analyze_sentiment(text: str) -> Sentiment:
    lowered = text.lower()
    words = re.findall(r'\w+', lowered)

    positive_parts = ["хорош", "люблю", "отлич", "нрав", "прекрас", "супер", "класс", "рекоменд", "шикар", "удивит"]
    negative_parts = ["плохо", "ненавиж", "ужас", "отврат", "кошмар", "разочар", "бесполез", "дерьм", "слаб", "глуп"]

    positive_count = sum(
        1 for word in words for part in positive_parts if part in word
    )
    negative_count = sum(
        1 for word in words for part in negative_parts if part in word
    )

    if positive_count > negative_count:
        return Sentiment.positive
    elif negative_count > positive_count:
        return Sentiment.negative
    else:
        return Sentiment.neutral

@app.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate):
    db = SessionLocal()
    try:
        sentiment = analyze_sentiment(review.text)
        created_at = datetime.utcnow().isoformat()
        db_review = Review(text=review.text, sentiment=sentiment, created_at=created_at)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    finally:
        db.close()

@app.get("/reviews", response_model=list[ReviewResponse])
def get_reviews(sentiment: Sentiment = Query(None)):
    db = SessionLocal()
    try:
        query = db.query(Review)
        if sentiment:
            query = query.filter(Review.sentiment == sentiment)
        return query.all()
    finally:
        db.close()
