from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.car_rental import CarRentalCreate, CarRentalResponse, CarRentalBookRequest
from app.schemas.booking import BookingResponse
from app.services.booking_service import create_booking
from app.models.booking import ServiceType
from app.routers._helpers import list_collection, get_one

router = APIRouter(prefix="/car-rentals", tags=["Car Rentals"])


@router.get("/", response_model=List[CarRentalResponse])
async def list_car_rentals(
    skip: int = 0, limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return await list_collection(db, "car_rentals", skip, limit)


@router.get("/{rental_id}", response_model=CarRentalResponse)
async def get_car_rental(rental_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await get_one(db, "car_rentals", rental_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car rental not found")
    return doc


@router.post("/", response_model=CarRentalResponse, status_code=201)
async def create_car_rental(
    payload: CarRentalCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    doc = payload.model_dump()
    from datetime import datetime
    doc["created_at"] = datetime.utcnow()
    result = await db["car_rentals"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/{rental_id}/book", response_model=BookingResponse, status_code=201)
async def book_car_rental(
    rental_id: str,
    payload: CarRentalBookRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    rental = await get_one(db, "car_rentals", rental_id)
    if not rental:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car rental not found")
    if not rental.get("available", True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle not available")

    def _as_dt(v):
        if isinstance(v, str):
            from datetime import datetime
            return datetime.fromisoformat(v)
        return v

    days = max(1, (_as_dt(rental["dropoff_dt"]) - _as_dt(rental["pickup_dt"])).days)
    amount = rental["price_per_day"] * days

    booking = await create_booking(
        db=db,
        user_id=current_user["_id"],
        service_type=ServiceType.car_rental,
        service_id=rental_id,
        amount=amount,
        notes=payload.notes,
    )
    await db["car_rentals"].update_one(
        {"_id": ObjectId(rental_id)}, {"$set": {"available": False}}
    )
    return booking
