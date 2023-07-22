from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    detail: str


class BadRequestResponse(BaseModel):
    detail: str


class UnauthorizedResponse(BaseModel):
    detail: str
