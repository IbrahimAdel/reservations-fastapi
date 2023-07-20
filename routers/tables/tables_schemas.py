from pydantic import BaseModel


class AddTableSchema(BaseModel):
    number: int
    capacity: int
