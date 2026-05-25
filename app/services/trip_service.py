"""
Trip service: create, retrieve, and manage booking attachments.
"""
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    doc["booking_ids"] = [str(b) for b in doc.get("booking_ids", [])]
    return doc


async def create_trip(*, db: AsyncIOMotorDatabase, user_id: str, name: str, description: str | None) -> dict:
    now = datetime.now(timezone.utc)
    trip_id = ObjectId()
    doc = {
        "_id": trip_id,
        "user_id": user_id,
        "name": name,
        "description": description,
        "booking_ids": [],
        "created_at": now,
        "updated_at": now,
    }
    await db["trips"].insert_one(doc)
    return _serialize(doc)


async def get_user_trips(*, db: AsyncIOMotorDatabase, user_id: str) -> list[dict]:
    cursor = db["trips"].find({"user_id": user_id})
    return [_serialize(d) async for d in cursor]


async def get_trip(*, db: AsyncIOMotorDatabase, trip_id: str, user_id: str) -> dict:
    doc = await db["trips"].find_one({"_id": ObjectId(trip_id), "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return _serialize(doc)


async def add_booking_to_trip(
    *, db: AsyncIOMotorDatabase, trip_id: str, booking_id: str, user_id: str
) -> dict:
    booking = await db["bookings"].find_one({"_id": ObjectId(booking_id), "user_id": user_id})
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found or not yours")

    result = await db["trips"].find_one_and_update(
        {"_id": ObjectId(trip_id), "user_id": user_id},
        {
            "$addToSet": {"booking_ids": ObjectId(booking_id)},
            "$set": {"updated_at": datetime.now(timezone.utc)},
        },
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return _serialize(result)


async def remove_booking_from_trip(
    *, db: AsyncIOMotorDatabase, trip_id: str, booking_id: str, user_id: str
) -> dict:
    result = await db["trips"].find_one_and_update(
        {"_id": ObjectId(trip_id), "user_id": user_id},
        {
            "$pull": {"booking_ids": ObjectId(booking_id)},
            "$set": {"updated_at": datetime.now(timezone.utc)},
        },
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return _serialize(result)


async def delete_trip(*, db: AsyncIOMotorDatabase, trip_id: str, user_id: str) -> None:
    result = await db["trips"].delete_one({"_id": ObjectId(trip_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
