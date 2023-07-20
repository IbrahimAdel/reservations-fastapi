from fastapi import HTTPException
from sqlalchemy.orm import Session

from deps.auth import encode_token, verify_password, get_password_hash
from routers.auth.schemas import UserRegisterSchema, UserLoginSchema
from routers.auth.auth_repo import is_email_name_taken, is_restaurant_name_taken, create_admin, get_user_for_login


async def register_user(user: UserRegisterSchema, db: Session):
    email_taken = is_email_name_taken(user.email, db)
    if email_taken:
        raise HTTPException(status_code=400, detail='email is taken')
    restaurant_exists = is_restaurant_name_taken(name=user.restaurant_name, db=db)
    if restaurant_exists:
        raise HTTPException(status_code=400, detail="restaurant name is taken")

    hashed_password = get_password_hash(password=user.password)
    create_admin(user=user, hashed_pass=hashed_password, db=db)


async def login_user(credentials: UserLoginSchema, db: Session):
    user = await get_user_for_login(email=credentials.email.lower(), db=db)
    if (user is None) or (not verify_password(plain_password=credentials.password,
                                              hashed_password=user.hashed_password)):
        raise HTTPException(status_code=401, detail='Invalid username or password')

    token = encode_token(user.id, user.restaurant_id)
    return {"access_token": token}