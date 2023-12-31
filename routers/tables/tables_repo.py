from sqlalchemy.orm import Session
from sqlalchemy import select, and_, delete, asc, func

from database.models import Table
from utils.query_utilities import paginate
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


def is_table_in_restaurant(table_id: int, restaurant_id: int, db: Session):
    statement = select(Table)\
        .with_only_columns(Table.id)\
        .where(and_(Table.id == table_id, Table.restaurant_id == restaurant_id))\
        .limit(1)
    table_id = db.scalars(statement=statement).first()
    return table_id is not None


def get_table_id_and_capacity(table_id: int, restaurant_id: int, db: Session):
    statement = select(Table.id, Table.capacity)\
        .select_from(Table)\
        .where(and_(Table.id == table_id, Table.restaurant_id == restaurant_id))\
        .limit(1)
    result = db.execute(statement=statement).first()
    if result is None:
        return result
    return dict(zip(["id", "capacity"], result))


def get_tables_page(limit: int, offset: int, restaurant_id, db: Session):
    statement = select(Table).where(Table.restaurant_id == restaurant_id)
    return paginate(query=statement, limit=limit, offset=offset, db=db)


def delete_table(table_id: int, restaurant_id: int, db: Session):
    statement = delete(Table).where(and_(Table.id == table_id, Table.restaurant_id == restaurant_id))
    result = db.execute(statement=statement)
    db.commit()
    return result

def get_min_capacity(capacity: int, restaurant_id: int, db: Session):
    statement = select(func.min(Table.capacity))\
        .where(and_(Table.restaurant_id == restaurant_id, Table.capacity >= capacity))
    return db.scalar(statement)


def get_table_ids_with_min_capacity(min_capacity: int, restaurant_id: int, db: Session):
    statement = select(Table)\
        .where(and_(Table.capacity == min_capacity, Table.restaurant_id == restaurant_id))
    return [table.id for table in db.scalars(statement)]
