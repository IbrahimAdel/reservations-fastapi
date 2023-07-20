from fastapi import APIRouter, Depends

from internals.auth import is_logged_in
from routers.users.users_schemas import AddUserSchema

router = APIRouter(prefix='/users', tags=['users'])

PROTECTED = Depends(is_logged_in)


@router.post('/', dependencies=[PROTECTED])
def add_user(user: AddUserSchema):
    print(user)
    return user

@router.get('/me', dependencies=[PROTECTED])
def me():
    return {"me": "hi"}
