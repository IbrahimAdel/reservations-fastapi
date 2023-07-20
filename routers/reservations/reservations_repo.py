from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import delete, and_, select, asc, func, or_, between
from sqlalchemy.sql.functions import count

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
        .where(and_(Reservation.start <= end, Reservation.end >= start, Reservation.restaurant_id == restaurant_id))\
        .order_by(asc(Reservation.start))
    return paginate(query=statement, limit=limit, offset=offset, db=db)


def is_reservation_conflicts(restaurant_id: int, table_id: int, start: datetime, end: datetime, db: Session):
    statement = select(Reservation.id)\
        .where(and_(
            or_(between(expr=Reservation.start, lower_bound=start, upper_bound=end),
                between(expr=Reservation.end, lower_bound=start, upper_bound=end)),
            Reservation.restaurant_id == restaurant_id,
            Reservation.table_id == table_id
        ))
    c = db.scalars(statement=statement).first()
    return c is not None


def get_reservation_by_id(reservation_id: int, restaurant_id: int, db: Session):
    statement = select(Reservation)\
        .where(and_(Reservation.id == reservation_id, Reservation.restaurant_id == restaurant_id))
    return db.scalars(statement=statement).first()
