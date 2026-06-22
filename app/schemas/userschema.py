from pydantic import BaseModel, EmailStr, Field


only_letter_patters=r"[a-zA-Z\s]+$"

class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
    first_name: str = Field(max_length=20, pattern=only_letter_patters)
    last_name: str = Field(max_length=20, pattern=only_letter_patters)


class LoginUser(BaseModel):
    email: EmailStr
    password: str
