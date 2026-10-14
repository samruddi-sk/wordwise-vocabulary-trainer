from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=200)
    definition: str = Field(min_length=1, max_length=2000)
    language: str = Field(min_length=1, max_length=80)

    @field_validator("word", "definition", "language")
    @classmethod
    def trim_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank")
        return value

class WordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    word: str
    definition: str
    language: str
    created_at: datetime

class ReviewCreate(BaseModel):
    score: int = Field(ge=0, le=5)

class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    word_id: int
    review_date: datetime
    score: int
    interval: int
    easiness_factor: float
    repetition: int
    next_review: datetime

class WordProgress(WordOut):
    last_score: int | None = None
    interval: int = 0
    easiness_factor: float = 2.5
    repetition: int = 0
    next_review: datetime | None = None
    is_due: bool = True

class HistoryOut(BaseModel):
    total_words: int
    total_reviews: int
    accuracy_percent: float
    streak_days: int
    schedule: list[WordProgress]
    difficult_words: list[WordProgress]
    recent_reviews: list[ReviewOut]
