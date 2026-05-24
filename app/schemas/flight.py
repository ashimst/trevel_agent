from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FlightCreate(BaseModel):
    origin: str
    destination: str
    departure_dt: datetime
    airline: str
    seat_class: str
    available_seats: int
    price: float


class FlightResponse(BaseModel):
    id: str
    origin: str
    destination: str
    departure_dt: datetime
    airline: str
    seat_class: str
    available_seats: int
    price: float
    created_at: datetime


class FlightBookRequest(BaseModel):
    notes: Optional[str] = None
