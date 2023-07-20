from fastapi import HTTPException
from sqlalchemy.orm import Session

from .reservations_schemas import AddReservationSchema
from ..tables import tables_repo
from . import reservations_repo


def add_reservation(reservation: AddReservationSchema, restaurant_id: int, db: Session):
    table_exists = tables_repo.is_table_in_restaurant(table_id=reservation.table_id, restaurant_id=restaurant_id, db=db)
    if not table_exists:
        raise HTTPException(status_code=404, detail="table not found")
    reservation_conflict = reservations_repo.is_reservation_conflicts(
        restaurant_id=restaurant_id, table_id=reservation.table_id, start=reservation.start, end=reservation.end, db=db
    )
    if reservation_conflict:
        raise HTTPException(status_code=400, detail="conflict with other reservation")

    return reservations_repo.add_reservation(reservation=reservation, restaurant_id=restaurant_id, db=db)


def delete_reservation(reservation_id: int, restaurant_id: int, db: Session):
    if not reservations_repo.reservation_exists(reservation_id=reservation_id, restaurant_id=restaurant_id, db=db):
        raise HTTPException(status_code=404, detail="reservation not found")

    reservations_repo.delete_reservation(reservation_id=reservation_id, restaurant_id=restaurant_id, db=db)

def get_today_reservation(limit: int, offset: int, restaurant_id: int, db: Session):
    return reservations_repo.get_today_reservation(restaurant_id=restaurant_id, db=db, limit=limit, offset=offset)


def get_reservation_by_id(reservation_id: int, restaurant_id: int, db: Session):
    reservation = reservations_repo.get_reservation_by_id(reservation_id=reservation_id,
                                                          restaurant_id=restaurant_id, db=db)
    if reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")
    return reservation
