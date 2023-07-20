from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db
from deps.auth import current_user
from .reservations_schemas import AddReservationSchema
from . import reservations_service

router = APIRouter(prefix='/reservations', tags=['reservations'])


@router.post('')
def add_reservation(reservation: AddReservationSchema, current=Depends(current_user), db: Session = Depends(get_db)):
    restaurant_id = current.get('restaurant_id')
    return reservations_service.add_reservation(reservation=reservation, restaurant_id=restaurant_id, db=db)


@router.delete('/{reservation_id}')
def delete_reservation(reservation_id: int, current=Depends(current_user), db: Session = Depends(get_db)):
    restaurant_id = current.get('restaurant_id')
    reservations_service.delete_reservation(reservation_id=reservation_id, restaurant_id=restaurant_id, db=db)
    return {"success": True}


@router.get('/today')
def reservations_today(offset: int = 0, limit: int = 10, current=Depends(current_user), db: Session = Depends(get_db)):
    restaurant_id = current.get('restaurant_id')
    return reservations_service.get_today_reservation(restaurant_id=restaurant_id, db=db, limit=limit, offset=offset)


@router.get('/{reservation_id}')
def reservations_today(reservation_id: int, current=Depends(current_user), db: Session = Depends(get_db)):
    restaurant_id = current.get('restaurant_id')
    return reservations_service.get_reservation_by_id(restaurant_id=restaurant_id, db=db, reservation_id=reservation_id)

