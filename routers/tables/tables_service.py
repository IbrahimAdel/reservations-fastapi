from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import tables_repo
from ..reservations import reservations_repo
from .tables_schemas import AddTableSchema


def add_table(table: AddTableSchema, restaurant_id: int, db: Session):
    is_number_taken = tables_repo.is_table_number_taken(number=table.number, restaurant_id=restaurant_id, db=db)
    if is_number_taken:
        raise HTTPException(status_code=400, detail=f"table with number {table.number} already exists")
    return tables_repo.create_table(table=table, restaurant_id=restaurant_id, db=db)


def get_tables_page(limit: int, offset: int, restaurant_id: int, db: Session):
    return tables_repo.get_tables_page(limit=limit, offset=offset, restaurant_id=restaurant_id, db=db)


def delete_table(table_id: int, restaurant_id: int, db: Session):
    if not tables_repo.is_table_in_restaurant(table_id=table_id, restaurant_id=restaurant_id, db=db):
        raise HTTPException(status_code=404, detail="table not found")
    if reservations_repo.is_there_future_reservation_for_table(table_id, db):
        raise HTTPException(status_code=400, detail="table has future reservations")

    tables_repo.delete_table(table_id=table_id, restaurant_id=restaurant_id, db=db)
    return {"success": True}
