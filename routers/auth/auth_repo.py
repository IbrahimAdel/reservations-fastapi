from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from database.models import User, Role, Restaurant
from .schemas import UserRegisterSchema


async def create_admin(user: UserRegisterSchema, hashed_pass: str, db: Session):
    user_to_create = User(email=user.email.lower(), hashed_password=hashed_pass, name=user.name, role=Role.ADMIN,
                          restaurant=Restaurant(name=user.restaurant_name))
    db.add(user_to_create)
    db.commit()
    db.refresh(user_to_create)
    return user_to_create


async def is_restaurant_name_taken(name: str, db: Session):
    statement = select(Restaurant)\
        .with_only_columns(Restaurant.name)\
        .where(and_(Restaurant.name == name))\
        .limit(1)
    result = db.execute(statement).first()

    if result is None:
        return False
    return True


async def is_email_name_taken(email: str, db: Session):
    statement = select(User) \
        .with_only_columns(User.email) \
        .where(and_(User.email == email.lower()))\
        .limit(1)
    result = db.execute(statement).first()
    if result is None:
        return False
    return True


async def get_user_email_and_pass(email: str, db: Session):
    statement = select(User)\
        .with_only_columns(User.email, User.hashed_password) \
        .where(and_(User.email == email))\
        .limit(1)
    user = db.execute(statement).first()
    return user
