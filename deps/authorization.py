from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException

from caching.redis_client import r
from database.models import User, Role


def is_admin(user_id: int, db: Session):
    role = r.get(f'{user_id}_role')
    if role is None:
        statement = select(User) \
            .with_only_columns(User.id) \
            .where(and_(User.role == Role.ADMIN, User.id == user_id))\
            .limit(1)
        id = db.scalars(statement=statement).first()
        if id is None:
            raise HTTPException(status_code=403, detail="unauthorized")
        r.set(name=f'{id}_role', value=Role.ADMIN.value, ex=300)
    return user_id
