from sqlalchemy.orm import Session
from sqlalchemy import select, and_, insert

from database.models import User, Role
from routers.users.users_schemas import AddUserSchema


def create_user(user: AddUserSchema, hashed_pass: str, restaurant_id: int, db: Session):
    statement = insert(User)\
        .values(email=user.email.lower(), hashed_password=hashed_pass, name=user.name, role=Role.USER,
                restaurant_id=restaurant_id, number=user.number.rjust(4, '0'))\
        .returning(User.id, User.email, User.name, User.role, User.restaurant_id,
                   User.number, User.created_at, User.updated_at)
    result = db.execute(statement=statement).mappings().first()
    db.commit()
    print(result)
    return result


def is_number_name_taken(number: str, restaurant_id, db: Session):
    statement = select(User) \
        .with_only_columns(User.email) \
        .where(and_(User.number == number.rjust(4, '0'), User.restaurant_id == restaurant_id))\
        .limit(1)
    result = db.execute(statement).mappings().first()
    return result is not None

def get_user_by_id(user_id: int, db: Session):
    statement = select(User)\
        .where(and_(User.id == user_id))\
        .limit(1)
    result = db.scalars(statement).first()
    return result
