from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from .auth_schema import UserRegisterSchema, UserLoginSchema, LoginResponse, RefreshTokensSchema, RefreshTokensResponse
from . import auth_service
from ..users.users_schemas import UserModelResponse

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', status_code=201)
def register(user: UserRegisterSchema, db: Session = Depends(get_db)) -> UserModelResponse:
    user = auth_service.register_user(user, db)
    return user


@router.post('/login')
def login(credentials: UserLoginSchema, db: Session = Depends(get_db)) -> LoginResponse:
    result = auth_service.login_user(credentials, db)
    return result


@router.post('/refresh_tokens')
def refresh(body: RefreshTokensSchema) -> RefreshTokensResponse:
    return auth_service.refresh_tokens(body.refresh_token)
