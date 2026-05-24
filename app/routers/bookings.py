from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.booking import BookingResponse
from app.models.booking import BookingStatus
from app.routers._helpers import serialize_doc

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/me", response_model=List[BookingResponse])
async def my_bookings(
    skip: int = 0,
    limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    cursor = db["bookings"].find({"user_id": current_user["_id"]}).skip(skip).limit(limit)
    return [serialize_doc(d) async for d in cursor]


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    doc = await db["bookings"].find_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]}
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return serialize_doc(doc)


@router.delete("/{booking_id}", status_code=204)
async def cancel_booking(
    booking_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    doc = await db["bookings"].find_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]}
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if doc["status"] in (BookingStatus.completed, BookingStatus.cancelled):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel a {doc['status']} booking",
        )
    await db["bookings"].update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": BookingStatus.cancelled, "updated_at": datetime.utcnow()}},
    )
