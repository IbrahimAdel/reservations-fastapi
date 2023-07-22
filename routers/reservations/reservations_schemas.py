from typing import List

from pydantic import BaseModel, FutureDatetime, NaiveDatetime
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from database.models import Reservation


class AddReservationSchema(BaseModel):
    start: FutureDatetime
    end: FutureDatetime
    table_id: int
    capacity_needed: int


class UpdateReservationSchema(BaseModel):
    start: FutureDatetime
    end: FutureDatetime


ReservationModelResponse = sqlalchemy_to_pydantic(Reservation)


class AvailableSlot(BaseModel):
    start: NaiveDatetime
    end: NaiveDatetime


class DeleteReservationResponse(BaseModel):
    success: bool


class ReservationPageResponse(BaseModel):
    count: int
    items: List[ReservationModelResponse]
