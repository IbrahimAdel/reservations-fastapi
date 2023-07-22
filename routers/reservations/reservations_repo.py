from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import delete, and_, select, asc, or_, between, column, update

from database.models import Reservation
from utils.query_utilities import paginate
from .reservations_schemas import AddReservationSchema, UpdateReservationSchema


def add_reservation(reservation: AddReservationSchema, restaurant_id: int, db: Session):
    r = Reservation(restaurant_id=restaurant_id, start=reservation.start, capacity_needed=reservation.capacity_needed,
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


def is_reservation_conflicts(restaurant_id: int, table_id: int, current_reservation_id: int | None,
                             start: datetime, end: datetime, db: Session):
    statement = select(Reservation.id)\
        .where(and_(
            or_(between(expr=Reservation.start, lower_bound=start, upper_bound=end),
                between(expr=Reservation.end, lower_bound=start, upper_bound=end),
                and_(Reservation.start < start, Reservation.end > end)),
            Reservation.restaurant_id == restaurant_id,
            Reservation.table_id == table_id,
            Reservation.id != current_reservation_id
        ))
    c = db.scalars(statement=statement).first()
    return c is not None


def get_reservation_by_id(reservation_id: int, restaurant_id: int, db: Session):
    statement = select(Reservation)\
        .where(and_(Reservation.id == reservation_id, Reservation.restaurant_id == restaurant_id))
    return db.scalars(statement=statement).first()


def update_reservation(reservation_id: int, restaurant_id: int,
                       reservation_update: UpdateReservationSchema, db: Session):
    statement = update(Reservation)\
        .where(and_(Reservation.id == reservation_id, Reservation.restaurant_id == restaurant_id))\
        .values(start=reservation_update.start, end=reservation_update.end)
    db.execute(statement)
    db.commit()
    return


def get_reservations_for_tables(from_time: datetime, to_time: datetime, table_ids: List[int], db: Session):
    statement = select(Reservation)\
        .where(and_(
            or_(between(expr=Reservation.start, lower_bound=from_time, upper_bound=to_time),
                between(expr=Reservation.end, lower_bound=from_time, upper_bound=to_time),
                and_(Reservation.start < from_time, Reservation.end > to_time)),
            column('table_id').in_(table_ids)
    )).order_by(asc(Reservation.start))
    return [reservation for reservation in db.scalars(statement=statement).all()]


def is_there_future_reservation_for_table(table_id: int, db: Session):
    now = datetime.utcnow()
    statement = select(Reservation.id)\
        .select_from(Reservation).limit(1)\
        .where(and_(Reservation.start > now, Reservation.table_id == table_id))
    result = db.execute(statement).mappings().all()
    return len(result) > 0
