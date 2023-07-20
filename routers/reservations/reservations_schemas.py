from pydantic import BaseModel, FutureDatetime


class AddReservationSchema(BaseModel):
    start: FutureDatetime
    end: FutureDatetime
    table_id: int
