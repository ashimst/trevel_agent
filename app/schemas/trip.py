from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TripCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TripAddBooking(BaseModel):
    booking_id: str


class TripResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str]
    booking_ids: List[str]
    created_at: datetime
    updated_at: datetime
