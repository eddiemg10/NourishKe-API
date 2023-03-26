from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., example="john@example.com")

    class Config:
        orm_mode = True

class UserIn(UserBase):
    password: str = Field(..., example="secret_password")


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, example="new_secret_password")


class UserOut(UserBase):
    id: str = Field(..., alias="_id")


class User(UserBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
