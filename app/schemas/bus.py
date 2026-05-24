from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BusCreate(BaseModel):
    origin: str
    destination: str
    departure_dt: datetime
    operator: str
    seat_number: str
    available_seats: int
    price: float


class BusResponse(BaseModel):
    id: str
    origin: str
    destination: str
    departure_dt: datetime
    operator: str
    seat_number: str
    available_seats: int
    price: float
    created_at: datetime


class BusBookRequest(BaseModel):
    notes: Optional[str] = None
