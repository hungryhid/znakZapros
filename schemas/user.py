from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)