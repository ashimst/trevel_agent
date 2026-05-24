from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    flight = "flight"
    bus = "bus"
    hotel = "hotel"
    activity = "activity"
    guide = "guide"
    car_rental = "car_rental"


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class BookingModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    service_type: ServiceType
    service_id: str
    status: BookingStatus = BookingStatus.pending
    payment_intent_id: Optional[str] = None
    amount: float
    # Optional extra details snapshot
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
