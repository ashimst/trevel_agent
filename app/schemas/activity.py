from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ActivityCreate(BaseModel):
    name: str
    location: str
    date: datetime
    duration_hours: float
    max_participants: int
    price: float


class ActivityResponse(BaseModel):
    id: str
    name: str
    location: str
    date: datetime
    duration_hours: float
    max_participants: int
    price: float
    created_at: datetime


class ActivityBookRequest(BaseModel):
    notes: Optional[str] = None
