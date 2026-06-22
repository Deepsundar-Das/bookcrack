from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime, date, UTC, timezone
from enum import Enum

class GenderEnum(str, Enum):
    male="male"
    female = "female"
    other = "other"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    #initially make it nullable but when user will try to book something make it mandatory to provide ph no
    phone: str | None = None
    # use tolower() to store gender
    gender: GenderEnum | None = None
    DOB: date | None = None
    # store hashed password
    password: str = Field(exclude=True, nullable=False)
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    last_login: datetime = Field(default_factory = lambda: datetime.now(timezone.utc).replace(tzinfo=None))
