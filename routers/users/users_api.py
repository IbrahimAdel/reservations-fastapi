from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from . import users_service as UsersService
from deps.auth import current_user
from routers.users.users_schemas import AddUserSchema

router = APIRouter(prefix='/users', tags=['users'])

PROTECTED = Depends(current_user)


@router.post('/', status_code=201)
async def add_user(user: AddUserSchema, current=Depends(current_user), db: Session = Depends(get_db)):
    created_user = UsersService.add_user(user, current.get('restaurant_id'), db)
    return created_user

@router.get('/me')
async def me(current=Depends(current_user), db: Session = Depends(get_db)):
    user = UsersService.get_current_user(int(current.get('sub')), db)
    return user
