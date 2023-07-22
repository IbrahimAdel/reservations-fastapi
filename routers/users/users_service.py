from fastapi import HTTPException
from sqlalchemy.orm import Session

from .users_schemas import AddUserSchema
from deps import authentication as AuthHandler
from routers.auth.auth_repo import is_email_name_taken
from . import users_repo as UsersRepo


def add_user(user: AddUserSchema, restaurant_id: int, db: Session):
    email_taken = is_email_name_taken(user.email, db)
    if email_taken:
        raise HTTPException(status_code=400, detail='email is taken')
    hashed_password = AuthHandler.get_password_hash(user.password)
    created_user = UsersRepo.create_user(user, hashed_password, restaurant_id, db)
    return created_user


def get_current_user(user_id: int, db: Session):
    user = UsersRepo.get_user_by_id(user_id, db)
    return user
