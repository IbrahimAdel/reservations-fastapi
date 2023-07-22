from pydantic import BaseModel, EmailStr
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from database.models import User


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    restaurant_name: str
    name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshTokensSchema(BaseModel):
    refresh_token: str


UserRegisterResponse = sqlalchemy_to_pydantic(User)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokensResponse(BaseModel):
    access_token: str
    refresh_token: str

