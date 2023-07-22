from typing import List

from pydantic import BaseModel, PositiveInt, ConfigDict
from datetime import datetime


class AddTableSchema(BaseModel):
    number: PositiveInt
    capacity: PositiveInt


class TableModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    capacity: int
    created_at: datetime
    updated_at: datetime
    restaurant_id: int


class TablePageResponse(BaseModel):
    count: int
    items: List[TableModelResponse]


class DeleteTableResponse(BaseModel):
    success: bool
