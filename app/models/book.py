from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(nullable=False, primary_key=True, default_factory=uuid.uuid4)
    title: str
    author: str
    description: str
    no_of_pages: int
    rating: float | None = None
    published_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )


def __repr__(self):
    return f"<Book is {self.title}>"
