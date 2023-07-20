from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import delete, and_, select

from database.models import Reservation
from utils.query_utilities import paginate
from .reservations_schemas import AddReservationSchema


def add_reservation(reservation: AddReservationSchema, restaurant_id: int, db: Session):
    r = Reservation(restaurant_id=restaurant_id, start=reservation.start,
                    end=reservation.end, table_id=reservation.table_id)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def delete_reservation(reservation_id: int, restaurant_id: int, db: Session):
    statement = delete(Reservation)\
        .where(and_(Reservation.restaurant_id == restaurant_id, Reservation.id == reservation_id))
    db.execute(statement=statement)
    db.commit()

def reservation_exists(reservation_id: int, restaurant_id: int, db: Session):
    statement = select(Reservation)\
        .where(and_(Reservation.id == reservation_id, Reservation.restaurant_id == restaurant_id))\
        .with_only_columns(Reservation.id)
    return db.scalars(statement=statement).first() is not None


def get_today_reservation(limit: int, offset: int, restaurant_id: int, db: Session):
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1) - timedelta(milliseconds=1)
    statement = select(Reservation)\
        .where(and_(Reservation.start <= end, Reservation.end >= start, Reservation.restaurant_id == restaurant_id))
    return paginate(query=statement, limit=limit, offset=offset, db=db)
