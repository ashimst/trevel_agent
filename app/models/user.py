"""
Pydantic v2 models — these mirror MongoDB documents exactly.
ObjectId is stored as a plain str (_id field).
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PyObjectId(str):
    """Lightweight wrapper so we can annotate _id fields."""
    pass


class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: str
    full_name: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
