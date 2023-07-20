from sqlalchemy import Select, select, func
from sqlalchemy.orm import Session


def paginate(query: Select, limit: int, offset: int, db: Session) -> dict:
    return {
        'count': db.scalar(select(func.count()).select_from(query.subquery())),
        'items': [todo for todo in db.scalars(query.limit(limit).offset(offset))]
    }