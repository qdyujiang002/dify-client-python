try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum
from typing import Optional

from pydantic import BaseModel


class Rating(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class FeedbackRequest(BaseModel):
    rating: Optional[Rating] = None
    user: Optional[str] = None


class FeedbackResponse(BaseModel):
    result: Optional[str] = None  # success
