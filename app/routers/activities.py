from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityBookRequest
from app.schemas.booking import BookingResponse
from app.services.booking_service import create_booking
from app.models.booking import ServiceType
from app.routers._helpers import list_collection, get_one

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("/", response_model=List[ActivityResponse])
async def list_activities(
    skip: int = 0, limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return await list_collection(db, "activities", skip, limit)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await get_one(db, "activities", activity_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return doc


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    payload: ActivityCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    doc = payload.model_dump()
    from datetime import datetime
    doc["created_at"] = datetime.utcnow()
    result = await db["activities"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/{activity_id}/book", response_model=BookingResponse, status_code=201)
async def book_activity(
    activity_id: str,
    payload: ActivityBookRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    activity = await get_one(db, "activities", activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    if activity.get("max_participants", 0) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activity is fully booked")

    booking = await create_booking(
        db=db,
        user_id=current_user["_id"],
        service_type=ServiceType.activity,
        service_id=activity_id,
        amount=activity["price"],
        notes=payload.notes,
    )
    from bson import ObjectId
    await db["activities"].update_one(
        {"_id": ObjectId(activity_id)}, {"$inc": {"max_participants": -1}}
    )
    return booking
