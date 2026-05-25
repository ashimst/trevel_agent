from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.flight import FlightCreate, FlightResponse, FlightBookRequest
from app.schemas.booking import BookingResponse
from app.services.booking_service import create_booking
from app.models.booking import ServiceType
from app.routers._helpers import serialize_doc, list_collection, get_one

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.get("/", response_model=List[FlightResponse])
async def list_flights(
    skip: int = 0, limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return await list_collection(db, "flights", skip, limit)


@router.get("/{flight_id}", response_model=FlightResponse)
async def get_flight(flight_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await get_one(db, "flights", flight_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    return doc


@router.post("/", response_model=FlightResponse, status_code=201)
async def create_flight(
    payload: FlightCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    doc = payload.model_dump()
    from datetime import datetime, timezone
    doc["created_at"] = datetime.now(timezone.utc)
    result = await db["flights"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/{flight_id}/book", response_model=BookingResponse, status_code=201)
async def book_flight(
    flight_id: str,
    payload: FlightBookRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    flight = await get_one(db, "flights", flight_id)
    if not flight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    if flight.get("available_seats", 0) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No seats available")

    booking = await create_booking(
        db=db,
        user_id=current_user["_id"],
        service_type=ServiceType.flight,
        service_id=flight_id,
        amount=flight["price"],
        notes=payload.notes,
    )
    # Decrement seat count
    await db["flights"].update_one(
        {"_id": ObjectId(flight_id)}, {"$inc": {"available_seats": -1}}
    )
    return booking
