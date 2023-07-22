from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from . import users_service
from deps.authentication import current_user
from .users_schemas import AddUserSchema, UserModelResponse

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=201)
async def add_user(user: AddUserSchema, current=Depends(current_user),
                   db: Session = Depends(get_db)) -> UserModelResponse:
    created_user = users_service.add_user(user, current.get('restaurant_id'), db)
    return created_user

@router.get('/me')
async def me(current=Depends(current_user), db: Session = Depends(get_db)) -> UserModelResponse:
    user = users_service.get_current_user(int(current.get('sub')), db)
    return user
