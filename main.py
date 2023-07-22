from fastapi import FastAPI
from pydantic import BaseModel

from database import models, db
from routers.auth import auth_api
from routers.reservations import reservations_api
from routers.tables import tables_api
from routers.users import users_api
from utils.error_schemas import NotFoundResponse, BadRequestResponse

app = FastAPI(title="Restaurant management", version='1.0',
              responses={404: {"model": NotFoundResponse}, 400: {"model": BadRequestResponse}})

app.include_router(router=auth_api.router)
app.include_router(router=users_api.router)
app.include_router(router=tables_api.router)
app.include_router(router=reservations_api.router)

# TODO. only for dev, use migrations for production.
models.Base.metadata.create_all(bind=db.engine)


class HealthCheckResponse(BaseModel):
    healthy: bool


@app.get("/")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(healthy=True)
