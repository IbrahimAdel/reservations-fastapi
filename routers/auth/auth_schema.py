from pydantic import BaseModel, EmailStr


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


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokensResponse(BaseModel):
    access_token: str
    refresh_token: str

