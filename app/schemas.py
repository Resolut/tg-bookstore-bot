from typing import Optional

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class UserBase(BaseModel):
    telegram_id: int
    username: str = Field(..., min_length=1, max_length=32)


class UserCreate(UserBase):
    role: str = 'client'
