from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CarRentalModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    vehicle_type: str        # sedan / SUV / van / motorcycle
    vehicle_name: str
    pickup_location: str
    pickup_dt: datetime
    dropoff_dt: datetime
    price_per_day: float
    available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
