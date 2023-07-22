from typing import Any

from pydantic import BaseModel, Field, NaiveDatetime, EmailStr


class AddUserSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    number: str = Field(..., max_length=4, pattern="^[0-9]+$")


class UserModelResponse(BaseModel):
    number: str
    id: int
    created_at: NaiveDatetime
    restaurant_id: int
    email: EmailStr
    name: str
    role: Any
    updated_at: NaiveDatetime
