from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CarRentalCreate(BaseModel):
    vehicle_type: str
    vehicle_name: str
    pickup_location: str
    pickup_dt: datetime
    dropoff_dt: datetime
    price_per_day: float
    available: bool = True


class CarRentalResponse(BaseModel):
    id: str
    vehicle_type: str
    vehicle_name: str
    pickup_location: str
    pickup_dt: datetime
    dropoff_dt: datetime
    price_per_day: float
    available: bool
    created_at: datetime


class CarRentalBookRequest(BaseModel):
    notes: Optional[str] = None
