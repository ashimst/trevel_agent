from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FlightModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    origin: str
    destination: str
    departure_dt: datetime
    airline: str
    seat_class: str          # economy / business / first
    available_seats: int
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
