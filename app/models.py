from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    word: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
    reviews: Mapped[list["Review"]] = relationship(back_populates="word", cascade="all, delete-orphan", passive_deletes=True)

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("score BETWEEN 0 AND 5", name="ck_reviews_score_range"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    review_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    interval: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    easiness_factor: Mapped[float] = mapped_column(Float, nullable=False, default=2.5)
    repetition: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    next_review: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    word: Mapped[Word] = relationship(back_populates="reviews")
