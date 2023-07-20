from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from deps.authorization import is_admin
from .tables_service import add_table
from deps.auth import current_user
from routers.tables.tables_schemas import AddTableSchema

router = APIRouter(prefix='/tables', tags=['tables'])


@router.post('/', status_code=201)
def add_table_to_restaurant(table: AddTableSchema,
                            current=Depends(current_user),db: Session = Depends(get_db)):
    # throw if not admin
    is_admin(user_id=current.get('sub'), db=db)

    table = add_table(table=table, restaurant_id=current.get('restaurant_id'), db=db)
    return table


@router.get('/')
def get_tables_page(limit: int = 10, offset: int = 0):
    print(limit, offset)

