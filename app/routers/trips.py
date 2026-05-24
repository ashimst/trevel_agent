from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.trip import TripCreate, TripAddBooking, TripResponse
from app.services import trip_service

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/", response_model=TripResponse, status_code=201)
async def create_trip(
    payload: TripCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    return await trip_service.create_trip(
        db=db,
        user_id=current_user["_id"],
        name=payload.name,
        description=payload.description,
    )


@router.get("/me", response_model=List[TripResponse])
async def my_trips(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    return await trip_service.get_user_trips(db=db, user_id=current_user["_id"])


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    return await trip_service.get_trip(db=db, trip_id=trip_id, user_id=current_user["_id"])


@router.post("/{trip_id}/bookings", response_model=TripResponse)
async def add_booking(
    trip_id: str,
    payload: TripAddBooking,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    return await trip_service.add_booking_to_trip(
        db=db,
        trip_id=trip_id,
        booking_id=payload.booking_id,
        user_id=current_user["_id"],
    )


@router.delete("/{trip_id}/bookings/{booking_id}", response_model=TripResponse)
async def remove_booking(
    trip_id: str,
    booking_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    return await trip_service.remove_booking_from_trip(
        db=db,
        trip_id=trip_id,
        booking_id=booking_id,
        user_id=current_user["_id"],
    )


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(
    trip_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    await trip_service.delete_trip(db=db, trip_id=trip_id, user_id=current_user["_id"])
