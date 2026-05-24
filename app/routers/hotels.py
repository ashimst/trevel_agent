from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.hotel import HotelCreate, HotelResponse, HotelBookRequest
from app.schemas.booking import BookingResponse
from app.services.booking_service import create_booking
from app.models.booking import ServiceType
from app.routers._helpers import list_collection, get_one

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", response_model=List[HotelResponse])
async def list_hotels(
    skip: int = 0, limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return await list_collection(db, "hotels", skip, limit)


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(hotel_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await get_one(db, "hotels", hotel_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return doc


@router.post("/", response_model=HotelResponse, status_code=201)
async def create_hotel(
    payload: HotelCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    doc = payload.model_dump()
    from datetime import datetime
    doc["created_at"] = datetime.utcnow()
    result = await db["hotels"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/{hotel_id}/book", response_model=BookingResponse, status_code=201)
async def book_hotel(
    hotel_id: str,
    payload: HotelBookRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    hotel = await get_one(db, "hotels", hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    if hotel.get("available_rooms", 0) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No rooms available")

    # Compute total: price_per_night × nights
    from datetime import datetime
    nights = max(
        1,
        (hotel["check_out"] - hotel["check_in"]).days
        if not isinstance(hotel["check_out"], str)
        else 1,
    )
    amount = hotel["price_per_night"] * nights

    booking = await create_booking(
        db=db,
        user_id=current_user["_id"],
        service_type=ServiceType.hotel,
        service_id=hotel_id,
        amount=amount,
        notes=payload.notes,
    )
    await db["hotels"].update_one(
        {"_id": ObjectId(hotel_id)}, {"$inc": {"available_rooms": -1}}
    )
    return booking
