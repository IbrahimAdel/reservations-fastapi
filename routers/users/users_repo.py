from sqlalchemy.orm import Session, defer
from sqlalchemy import select, and_

from database.models import User, Role
from routers.users.users_schemas import AddUserSchema


def create_user(user: AddUserSchema, hashed_pass: str, restaurant_id: int, db: Session):
    user_to_create = User(email=user.email.lower(), hashed_password=hashed_pass, name=user.name, role=Role.USER,
                          restaurant_id=restaurant_id, number=user.number.rjust(4, '0'))
    db.add(user_to_create)
    db.commit()
    db.refresh(user_to_create)
    return user_to_create


def get_user_by_id(user_id: int, db: Session):
    statement = select(User)\
        .where(and_(User.id == user_id))\
        .limit(1)
    result = db.scalars(statement).first()
    return result
