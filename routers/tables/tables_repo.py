from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from database.models import Table
from .tables_schemas import AddTableSchema


def create_table(table: AddTableSchema, restaurant_id: int, db: Session):
    t = Table(capacity=table.capacity, number=table.number, restaurant_id=restaurant_id)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def is_table_number_taken(number: int, restaurant_id: int, db: Session):
    statement = select(Table)\
        .with_only_columns(Table.id)\
        .where(and_(Table.number == number, Table.restaurant_id == restaurant_id))\
        .limit(1)
    table_id = db.scalars(statement=statement).first()
    return table_id is not None
