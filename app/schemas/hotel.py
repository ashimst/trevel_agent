from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HotelCreate(BaseModel):
    property_name: str
    location: str
    check_in: datetime
    check_out: datetime
    room_type: str
    available_rooms: int
    price_per_night: float


class HotelResponse(BaseModel):
    id: str
    property_name: str
    location: str
    check_in: datetime
    check_out: datetime
    room_type: str
    available_rooms: int
    price_per_night: float
    created_at: datetime


class HotelBookRequest(BaseModel):
    notes: Optional[str] = None
