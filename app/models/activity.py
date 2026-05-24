from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ActivityModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    location: str
    date: datetime
    duration_hours: float
    max_participants: int
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
