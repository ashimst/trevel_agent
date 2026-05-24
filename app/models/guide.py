from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class GuideModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    languages: List[str]
    speciality: str
    daily_rate: float
    available_from: datetime
    available_to: datetime
    bio: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
