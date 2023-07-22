from typing import List

from pydantic import BaseModel, PositiveInt

from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from database.models import Table


class AddTableSchema(BaseModel):
    number: PositiveInt
    capacity: PositiveInt


TableModelResponse = sqlalchemy_to_pydantic(Table)


class TablePageResponse(BaseModel):
    count: int
    items: List[TableModelResponse]


class DeleteTableResponse(BaseModel):
    success: bool
