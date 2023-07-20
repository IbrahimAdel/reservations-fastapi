from fastapi import HTTPException
from sqlalchemy.orm import Session

from .reservations_schemas import AddReservationSchema
from ..tables import tables_repo
from . import reservations_repo


def add_reservation(reservation: AddReservationSchema, restaurant_id: int, db: Session):
    # TODO validate that the start and end do not intersect with another reservation
    table_exists = tables_repo.is_table_in_restaurant(table_id=reservation.table_id, restaurant_id=restaurant_id, db=db)
    if not table_exists:
        raise HTTPException(status_code=404, detail="table not found")

    return reservations_repo.add_reservation(reservation=reservation, restaurant_id=restaurant_id, db=db)


def delete_reservation(reservation_id: int, restaurant_id: int, db: Session):
    if not reservations_repo.reservation_exists(reservation_id=reservation_id, restaurant_id=restaurant_id, db=db):
        raise HTTPException(status_code=404, detail="reservation not found")

    reservations_repo.delete_reservation(reservation_id=reservation_id, restaurant_id=restaurant_id, db=db)
