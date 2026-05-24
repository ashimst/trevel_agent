from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.bus import BusCreate, BusResponse, BusBookRequest
from app.schemas.booking import BookingResponse
from app.services.booking_service import create_booking
from app.models.booking import ServiceType
from app.routers._helpers import serialize_doc, list_collection, get_one

router = APIRouter(prefix="/buses", tags=["Buses"])


@router.get("/", response_model=List[BusResponse])
async def list_buses(
    skip: int = 0, limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return await list_collection(db, "buses", skip, limit)


@router.get("/{bus_id}", response_model=BusResponse)
async def get_bus(bus_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await get_one(db, "buses", bus_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    return doc


@router.post("/", response_model=BusResponse, status_code=201)
async def create_bus(
    payload: BusCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    doc = payload.model_dump()
    from datetime import datetime
    doc["created_at"] = datetime.utcnow()
    result = await db["buses"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/{bus_id}/book", response_model=BookingResponse, status_code=201)
async def book_bus(
    bus_id: str,
    payload: BusBookRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    bus = await get_one(db, "buses", bus_id)
    if not bus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    if bus.get("available_seats", 0) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No seats available")

    booking = await create_booking(
        db=db,
        user_id=current_user["_id"],
        service_type=ServiceType.bus,
        service_id=bus_id,
        amount=bus["price"],
        notes=payload.notes,
    )
    await db["buses"].update_one(
        {"_id": ObjectId(bus_id)}, {"$inc": {"available_seats": -1}}
    )
    return booking
