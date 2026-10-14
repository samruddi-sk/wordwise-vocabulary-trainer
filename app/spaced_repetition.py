from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
import math

@dataclass(frozen=True)
class Schedule:
    interval: int
    easiness_factor: float
    repetition: int
    next_review: datetime

def calculate_schedule(score: int, previous_interval: int = 0, easiness_factor: float = 2.5, repetition: int = 0, today: date | None = None) -> Schedule:
    """Calculate a practical SM-2-inspired schedule following the challenge's explicit rules.

    The brief's example requires a first score of 5 to schedule the next review in 5 days;
    scores 0-2 always schedule the next review for tomorrow.
    """
    if not 0 <= score <= 5:
        raise ValueError("score must be between 0 and 5")
    today = today or date.today()
    ef = easiness_factor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
    ef = max(1.3, round(ef, 2))

    if score <= 2:
        interval = 1
        repetitions = 0
    elif score == 3:
        interval = max(2, math.ceil(max(previous_interval, 1) * 1.2))
        repetitions = repetition + 1
    elif score == 4:
        interval = max(2, previous_interval + 1) if repetition == 0 else max(previous_interval + 1, round(previous_interval * ef))
        repetitions = repetition + 1
    else:  # score == 5
        if repetition == 0:
            interval = 5
        elif repetition == 1:
            interval = 10
        else:
            interval = max(previous_interval + 1, round(previous_interval * ef))
        repetitions = repetition + 1

    next_review = datetime.combine(today + timedelta(days=interval), time.min)
    return Schedule(interval=interval, easiness_factor=ef, repetition=repetitions, next_review=next_review)
