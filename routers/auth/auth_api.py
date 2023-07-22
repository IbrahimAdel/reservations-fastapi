from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from .schemas import UserRegisterSchema, UserLoginSchema, UserRegisterResponse, LoginResponse, RefreshTokensSchema, \
    RefreshTokensResponse
from . import auth_service

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', status_code=201)
async def register(user: UserRegisterSchema, db: Session = Depends(get_db)) -> UserRegisterResponse:
    await auth_service.register_user(user, db)
    return user


@router.post('/login')
async def login(credentials: UserLoginSchema, db: Session = Depends(get_db)) -> LoginResponse:
    result = await auth_service.login_user(credentials, db)
    return result


@router.post('/refresh_tokens')
def refresh(body: RefreshTokensSchema) -> RefreshTokensResponse:
    return auth_service.refresh_tokens(body.refresh_token)
