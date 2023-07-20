from fastapi import HTTPException
from sqlalchemy.orm import Session

from .tables_repo import create_table, is_table_number_taken
from .tables_schemas import AddTableSchema


def add_table(table: AddTableSchema, restaurant_id: int, db: Session):
    is_number_taken = is_table_number_taken(number=table.number, restaurant_id=restaurant_id, db=db)
    if is_number_taken:
        raise HTTPException(status_code=400, detail=f"table with number {table.number} already exists")
    return create_table(table=table, restaurant_id=restaurant_id, db=db)
