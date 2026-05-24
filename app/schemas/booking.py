from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.booking import ServiceType, BookingStatus


class BookingResponse(BaseModel):
    id: str
    user_id: str
    service_type: ServiceType
    service_id: str
    status: BookingStatus
    payment_intent_id: Optional[str]
    amount: float
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class BookingCreateInternal(BaseModel):
    """Used internally by service layer."""
    user_id: str
    service_type: ServiceType
    service_id: str
    amount: float
    notes: Optional[str] = None
