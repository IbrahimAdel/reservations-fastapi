from typing import List
from datetime import datetime

from pydantic import BaseModel, FutureDatetime, NaiveDatetime, ConfigDict

from database.models import Reservation


class AddReservationSchema(BaseModel):
    start: FutureDatetime
    end: FutureDatetime
    table_id: int
    capacity_needed: int


class UpdateReservationSchema(BaseModel):
    start: FutureDatetime
    end: FutureDatetime


class ReservationModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start: datetime
    end: datetime
    capacity_needed: int
    table_id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime


class AvailableSlot(BaseModel):
    start: NaiveDatetime
    end: NaiveDatetime


class DeleteReservationResponse(BaseModel):
    success: bool


class ReservationPageResponse(BaseModel):
    count: int
    items: List[ReservationModelResponse]
