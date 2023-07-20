from fastapi import HTTPException
from sqlalchemy.orm import Session

from internals import auth as auth_handler
from .schemas import UserRegisterSchema, UserLoginSchema
from . import auth_repo as AuthRepo

users = []

async def register_user(user: UserRegisterSchema, db: Session):
    email_taken = await AuthRepo.is_email_name_taken(user.email, db)
    if email_taken:
        raise HTTPException(status_code=400, detail='email is taken')
    restaurant_exists = await AuthRepo.is_restaurant_name_taken(user.restaurant_name, db)
    if restaurant_exists:
        raise HTTPException(status_code=400, detail="restaurant name is taken")

    hashed_password = auth_handler.get_password_hash(user.password)
    await AuthRepo.create_admin(user, hashed_password, db)


async def login_user(credentials: UserLoginSchema, db: Session):
    user = await AuthRepo.get_user_email_and_pass(credentials.email.lower(), db)
    if (user is None) or (not auth_handler.verify_password(credentials.password, user.hashed_password)):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    token = auth_handler.encode_token(user.email)
    return {"access_token": token}
