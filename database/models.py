import enum

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, func, Enum, UniqueConstraint
from sqlalchemy.orm import relationship, deferred

from .db import Base


class Role(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    users = relationship("User", backref="restaurant")
    tables = relationship("Table", backref="restaurant")
    reservations = relationship("Reservation", backref="restaurant")

    def __repr__(self):
        return 'RestaurantModel(name=%s)' % self.name


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(55), nullable=False)
    name = Column(String(80), nullable=False)
    hashed_password = deferred(Column(String(255), nullable=False))
    number = Column(String(4), default="0000")
    role = Column(Enum(Role))
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", onupdate="cascade", ondelete="cascade"), index=True)

    __table_args__ = (UniqueConstraint("number", "restaurant_id", name="restaurant_user_uc1"),)

    def __repr__(self):
        return 'UserModel(name=%s)' % self.name


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False, default=1)
    capacity = Column(Integer, default=4)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", onupdate="cascade", ondelete="cascade"), index=True)
    reservations = relationship("Reservation", backref="table")

    __table_args__ = (UniqueConstraint("number", "restaurant_id", name="restaurant_table_uc1"),)

    def __repr__(self):
        return 'TableModel(id=%s)' % self.id


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(TIMESTAMP(timezone=False), nullable=False, index=True)
    end = Column(TIMESTAMP(timezone=False), nullable=False, index=True)
    capacity_needed = Column(Integer, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id", onupdate="cascade", ondelete="SET NULL"), index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", onupdate="cascade", ondelete="cascade"), index=True)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return 'ReservationModel(id=%s)' % self.id
