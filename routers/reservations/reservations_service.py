from datetime import datetime
from typing import List, Any, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .reservations_schemas import AddReservationSchema, UpdateReservationSchema
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


def update_reservation_by_id(reservation_id: int, update: UpdateReservationSchema, restaurant_id: int, db: Session):
    reservation = reservations_repo.get_reservation_by_id(reservation_id=reservation_id,
                                                          restaurant_id=restaurant_id, db=db)
    if reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")
    print(reservation.start)
    print(datetime.now())
    print(reservation.start > datetime.now())
    if reservation.start < datetime.now():
        raise HTTPException(status_code=400, detail="can not edit past reservations")
    reservations_repo.update_reservation(reservation_id, restaurant_id, reservation_update=update, db=db)
    db.refresh(reservation)
    return reservation


def get_available_slots(restaurant_id: int, needed_capacity: int, from_time: datetime, to_time: datetime, db: Session):
    min_capacity = tables_repo.get_min_capacity(needed_capacity, restaurant_id, db)
    tables_ids = tables_repo.get_table_ids_with_min_capacity(min_capacity, restaurant_id, db=db)
    reservations = reservations_repo.get_reservations_for_tables(from_time, to_time, tables_ids, db=db)

    intersections = find_reservation_intersections(reservations, table_count=len(tables_ids))
    # inverting the intersections to get available reservation slots
    slots = []
    slot = {
        "start": from_time
    }
    for i in intersections:
        if i.get("start") > slot.get("start"):
            slot.update({"end": i.get("start")})
            if slot.get("end") > slot.get("start"):
                slots.append(slot)
        slot = {"start": i.get("end")}

    slot.update({"end": to_time})
    if slot.get("start") != slot.get("end"):
        slots.append(slot)

    return slots


def find_reservation_intersections(reservations: list, table_count: int):
    intersections: List[Dict[str, Any]] = []
    if len(reservations) == 0:
        return intersections

    for idx, current in enumerate(reservations):
        if idx == 0:
            intersections.append({
                "start": current.start,
                "end": current.end,
                "table_ids": {current.table_id}
            })
        else:
            last = intersections[len(intersections) - 1]
            max_start = max([last.get('start', None), current.start])
            min_end = min([last.get('end', None), current.end])
            if max_start < min_end:
                last.update({
                    "start": max_start,
                    "end": min_end,
                    "table_ids": {current.table_id}
                })
            else:
                intersections.append({
                    "start": current.start,
                    "end": current.end,
                    "table_ids": {current.table_id}
                })

    return list(filter(lambda x: len(x.get("table_ids")) == table_count, intersections))
