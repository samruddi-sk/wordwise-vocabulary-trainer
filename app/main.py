from datetime import date, datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db
from .spaced_repetition import calculate_schedule


app = FastAPI(
    title="Spaced Repetition Vocabulary Trainer API",
    description="A vocabulary trainer API that schedules reviews using an SM-2-inspired algorithm.",
    version="1.0.0",
)

# Allow the React frontend to communicate with the FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def latest_review(db: Session, word_id: int):
    """Return the most recent review for a vocabulary word."""
    return db.scalars(
        select(models.Review)
        .where(models.Review.word_id == word_id)
        .order_by(
            models.Review.review_date.desc(),
            models.Review.id.desc(),
        )
        .limit(1)
    ).first()


def progress_for_word(
    db: Session,
    word: models.Word,
) -> schemas.WordProgress:
    """Build progress information and determine whether a word is due."""
    latest = latest_review(db, word.id)
    today = date.today()

    if latest is None:
        return schemas.WordProgress.model_validate(
            word,
            from_attributes=True,
        ).model_copy(update={"is_due": True})

    due_date = latest.next_review.date()

    return schemas.WordProgress(
        id=word.id,
        word=word.word,
        definition=word.definition,
        language=word.language,
        created_at=word.created_at,
        last_score=latest.score,
        interval=latest.interval,
        easiness_factor=latest.easiness_factor,
        repetition=latest.repetition,
        next_review=latest.next_review,
        is_due=due_date <= today,
    )


@app.get("/", tags=["health"])
def root():
    """Return basic API information."""
    return {
        "message": "Spaced Repetition Vocabulary Trainer API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.post(
    "/words/",
    response_model=schemas.WordOut,
    status_code=status.HTTP_201_CREATED,
    tags=["words"],
)
def create_word(
    payload: schemas.WordCreate,
    db: Session = Depends(get_db),
):
    """Create a vocabulary word."""
    word = models.Word(
        word=payload.word,
        definition=payload.definition,
        language=payload.language,
    )

    db.add(word)
    db.commit()
    db.refresh(word)

    return word


@app.get(
    "/words/due/",
    response_model=list[schemas.WordProgress],
    tags=["words"],
)
def get_due_words(db: Session = Depends(get_db)):
    """Return words due today, including words never reviewed."""
    words = db.scalars(
        select(models.Word).order_by(
            models.Word.created_at.desc(),
            models.Word.id.desc(),
        )
    ).all()

    return [
        progress
        for word in words
        if (progress := progress_for_word(db, word)).is_due
    ]


@app.post(
    "/words/{word_id}/review/",
    response_model=schemas.ReviewOut,
    status_code=status.HTTP_201_CREATED,
    tags=["reviews"],
)
def review_word(
    word_id: int,
    payload: schemas.ReviewCreate,
    db: Session = Depends(get_db),
):
    """Submit a review score and calculate the next review date."""
    word = db.get(models.Word, word_id)

    if word is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found",
        )

    previous = latest_review(db, word_id)

    schedule = calculate_schedule(
        score=payload.score,
        previous_interval=previous.interval if previous else 0,
        easiness_factor=(
            previous.easiness_factor if previous else 2.5
        ),
        repetition=previous.repetition if previous else 0,
    )

    review = models.Review(
        word_id=word_id,
        score=payload.score,
        interval=schedule.interval,
        easiness_factor=schedule.easiness_factor,
        repetition=schedule.repetition,
        next_review=schedule.next_review,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


@app.get(
    "/words/history/",
    response_model=schemas.HistoryOut,
    tags=["reviews"],
)
def get_history(
    db: Session = Depends(get_db),
    limit: int = Query(default=100, ge=1, le=500),
):
    """Return learning history, progress metrics, and review schedules."""
    words = db.scalars(
        select(models.Word).order_by(models.Word.word.asc())
    ).all()

    reviews = db.scalars(
        select(models.Review)
        .order_by(
            models.Review.review_date.desc(),
            models.Review.id.desc(),
        )
        .limit(limit)
    ).all()

    all_reviews = db.scalars(
        select(models.Review).order_by(
            models.Review.review_date.desc(),
            models.Review.id.desc(),
        )
    ).all()

    progress = [
        progress_for_word(db, word)
        for word in words
    ]

    reviewed_count = len(all_reviews)
    successful_count = sum(
        1 for item in all_reviews if item.score >= 3
    )

    review_dates = {
        item.review_date.date()
        for item in all_reviews
    }

    today = date.today()
    anchor = (
        today
        if today in review_dates
        else today - timedelta(days=1)
    )

    streak = 0

    while anchor in review_dates:
        streak += 1
        anchor -= timedelta(days=1)

    difficult = sorted(
        (
            item
            for item in progress
            if item.last_score is not None
        ),
        key=lambda item: (item.last_score, item.word),
    )[:5]

    schedule = sorted(
        (
            item
            for item in progress
            if item.next_review is not None
        ),
        key=lambda item: (item.next_review, item.word),
    )

    return schemas.HistoryOut(
        total_words=len(words),
        total_reviews=reviewed_count,
        accuracy_percent=(
            round((successful_count / reviewed_count) * 100, 1)
            if reviewed_count
            else 0.0
        ),
        streak_days=streak,
        schedule=schedule,
        difficult_words=difficult,
        recent_reviews=reviews,
    )


@app.delete(
    "/words/{word_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["words"],
)
def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
):
    """Delete a vocabulary word."""
    word = db.get(models.Word, word_id)

    if word is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found",
        )

    db.delete(word)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)