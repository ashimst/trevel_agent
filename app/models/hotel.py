from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HotelModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    property_name: str
    location: str
    check_in: datetime
    check_out: datetime
    room_type: str           # standard / deluxe / suite
    available_rooms: int
    price_per_night: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
