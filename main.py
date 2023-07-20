from fastapi import FastAPI

from database import models, db
from routers.auth import auth_api
from routers.reservations import reservations_api
from routers.tables import tables_api
from routers.users import users_api

app = FastAPI()

app.include_router(router=auth_api.router)
app.include_router(router=users_api.router)
app.include_router(router=tables_api.router)
app.include_router(router=reservations_api.router)

models.Base.metadata.create_all(bind=db.engine)


@app.get("/")
def health_check():
    return {"healthy": True}