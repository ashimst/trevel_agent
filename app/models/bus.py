from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BusModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    origin: str
    destination: str
    departure_dt: datetime
    operator: str
    seat_number: str
    available_seats: int
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
