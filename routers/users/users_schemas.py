from pydantic import BaseModel, Field


class AddUserSchema(BaseModel):
    email: str
    password: str
    name: str
    number: str = Field(..., max_length=4, pattern="^[0-9]+$")
