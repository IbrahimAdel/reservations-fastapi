from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from deps.authorization import is_admin
from utils.error_schemas import UnauthorizedResponse
from . import tables_service
from deps.authentication import current_user
from routers.tables.tables_schemas import AddTableSchema, TableModelResponse, TablePageResponse, DeleteTableResponse

router = APIRouter(prefix='/tables', tags=['tables'])


@router.post('/', status_code=201, responses={403:{"model": UnauthorizedResponse}})
def add_table_to_restaurant(table: AddTableSchema, current=Depends(current_user),
                            db: Session = Depends(get_db)) -> TableModelResponse:
    # throw if not admin
    is_admin(user_id=current.get('sub'), db=db)

    table = tables_service.add_table(table=table, restaurant_id=current.get('restaurant_id'), db=db)
    return table


@router.get('/')
def get_tables_page(limit: int = 10, offset: int = 0, current=Depends(current_user),
                    db: Session = Depends(get_db)) -> TablePageResponse:
    restaurant_id = current.get('restaurant_id')
    page = tables_service.get_tables_page(limit=limit, offset=offset, restaurant_id=restaurant_id, db=db)
    return page


@router.delete('/{table_id}')
def delete_table(table_id: int, current=Depends(current_user),
                 db: Session = Depends(get_db)) -> DeleteTableResponse:
    restaurant_id = current.get('restaurant_id')
    is_admin(user_id=current.get('sub'), db=db)
    return tables_service.delete_table(table_id=table_id, restaurant_id=restaurant_id, db=db)
