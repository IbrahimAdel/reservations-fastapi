from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from pydantic import NaiveDatetime

from database.db import get_db
from deps.authentication import current_user
from .reservations_schemas import AddReservationSchema, UpdateReservationSchema, ReservationModelResponse, \
    AvailableSlot, DeleteReservationResponse, ReservationPageResponse
from . import reservations_service

router = APIRouter(prefix='/reservations', tags=['reservations'])


@router.post('', status_code=201)
def add_reservation(reservation: AddReservationSchema, current=Depends(current_user),
                    db: Session = Depends(get_db)) -> ReservationModelResponse:
    restaurant_id = current.get('restaurant_id')
    return reservations_service.add_reservation(reservation=reservation, restaurant_id=restaurant_id, db=db)


@router.delete('/{reservation_id}')
def delete_reservation(reservation_id: int, current=Depends(current_user),
                       db: Session = Depends(get_db)) -> DeleteReservationResponse:
    restaurant_id = current.get('restaurant_id')
    reservations_service.delete_reservation(reservation_id=reservation_id, restaurant_id=restaurant_id, db=db)
    return {"success": True}


@router.get('/today')
def reservations_today(offset: int = 0, limit: int = 10, current=Depends(current_user),
                       db: Session = Depends(get_db)) -> ReservationPageResponse:
    restaurant_id = current.get('restaurant_id')
    return reservations_service.get_today_reservation(restaurant_id=restaurant_id, db=db, limit=limit, offset=offset)


@router.get('/available')
def available_slots(from_time: NaiveDatetime, to_time: NaiveDatetime, min_capacity: int,
                    current=Depends(current_user), db: Session = Depends(get_db)) -> List[AvailableSlot]:
    restaurant_id = current.get('restaurant_id')
    return reservations_service.get_available_slots(from_time=from_time, to_time=to_time, needed_capacity=min_capacity,
                                                    restaurant_id=restaurant_id, db=db)


@router.get('/{reservation_id}')
def reservations_today(reservation_id: int, current=Depends(current_user),
                       db: Session = Depends(get_db)) -> ReservationModelResponse:
    restaurant_id = current.get('restaurant_id')
    return reservations_service.get_reservation_by_id(restaurant_id=restaurant_id, db=db, reservation_id=reservation_id)


@router.put('/{reservation_id}')
def update_reservation(reservation_id: int, update: UpdateReservationSchema,
                       current=Depends(current_user), db: Session = Depends(get_db)) -> ReservationModelResponse:
    restaurant_id = current.get('restaurant_id')
    return reservations_service.update_reservation_by_id(restaurant_id=restaurant_id, update=update,
                                                         db=db, reservation_id=reservation_id)
