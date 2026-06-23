from pydantic import BaseModel
from datetime import datetime
import uuid


class BookModel(BaseModel):
    title: str
    author: str
    description: str
    no_of_pages: int
    rating: float
    published_date: datetime


class UpdateBookModel(BaseModel):
    id: uuid.UUID
    title: str | None = None
    author: str | None = None
    description: str | None = None
    no_of_pages: int | None = None
    rating: float | None = None
    published_date: datetime | None = None
