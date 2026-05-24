"""
Dummy payments router -- no Stripe, no webhooks.
Provides simple demo endpoints to simulate payment confirmation and failure.
"""
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import get_current_user
from app.models.booking import BookingStatus
from app.routers._helpers import serialize_doc

router = APIRouter(prefix="/payments", tags=["Payments (Demo)"])


@router.post("/pay/{booking_id}", summary="Simulate successful payment")
async def simulate_payment_success(
    booking_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    """
    Demo endpoint: marks a pending booking as **confirmed**.
    Call this after booking to simulate a successful payment.
    """
    doc = await db["bookings"].find_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]}
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if doc["status"] != BookingStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Booking is already {doc['status']} — only pending bookings can be paid",
        )

    updated = await db["bookings"].find_one_and_update(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": BookingStatus.confirmed, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    return {
        "message": "Payment successful. Booking confirmed.",
        "booking": serialize_doc(updated),
    }


@router.post("/fail/{booking_id}", summary="Simulate failed payment")
async def simulate_payment_failure(
    booking_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    """
    Demo endpoint: marks a pending booking as **cancelled**.
    Simulates a declined / failed payment.
    """
    doc = await db["bookings"].find_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]}
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if doc["status"] != BookingStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Booking is already {doc['status']} — only pending bookings can fail",
        )

    updated = await db["bookings"].find_one_and_update(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": BookingStatus.cancelled, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    return {
        "message": "Payment failed. Booking cancelled.",
        "booking": serialize_doc(updated),
    }


@router.post("/complete/{booking_id}", summary="Mark booking as completed")
async def mark_completed(
    booking_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    """
    Demo endpoint: marks a confirmed booking as **completed**
    (i.e. the service was delivered).
    """
    doc = await db["bookings"].find_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]}
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if doc["status"] != BookingStatus.confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only confirmed bookings can be marked complete (current: {doc['status']})",
        )

    updated = await db["bookings"].find_one_and_update(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": BookingStatus.completed, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    return {
        "message": "Booking marked as completed.",
        "booking": serialize_doc(updated),
    }
