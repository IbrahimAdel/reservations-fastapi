from pydantic import BaseModel


class AddUserSchema(BaseModel):
    email: str
    password: str
    name: str
    number: int
