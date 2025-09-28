from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserInDB(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    settings: dict = {}
    created_at: datetime = datetime.utcnow()


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr