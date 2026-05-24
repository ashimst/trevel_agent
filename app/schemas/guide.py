from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class GuideCreate(BaseModel):
    name: str
    languages: List[str]
    speciality: str
    daily_rate: float
    available_from: datetime
    available_to: datetime
    bio: str = ""


class GuideResponse(BaseModel):
    id: str
    name: str
    languages: List[str]
    speciality: str
    daily_rate: float
    available_from: datetime
    available_to: datetime
    bio: str
    created_at: datetime


class GuideBookRequest(BaseModel):
    booking_from: datetime
    booking_to: datetime
    notes: Optional[str] = None
