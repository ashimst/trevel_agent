"""
Generic booking creation used by every service router.
Creates the booking document and a dummy PaymentIntent in one step.
"""
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.booking import BookingStatus, ServiceType
from app.services.stripe_service import create_payment_intent


async def create_booking(
    *,
    db: AsyncIOMotorDatabase,
    user_id: str,
    service_type: ServiceType,
    service_id: str,
    amount: float,
    notes: str | None = None,
) -> dict:
    """
    1. Verify the service document exists.
    2. Generate a dummy PaymentIntent (no external call).
    3. Insert booking document with status=pending.
    4. Return the booking doc.
    """
    collection_map = {
        ServiceType.flight: "flights",
        ServiceType.bus: "buses",
        ServiceType.hotel: "hotels",
        ServiceType.activity: "activities",
        ServiceType.guide: "guides",
        ServiceType.car_rental: "car_rentals",
    }
    collection = collection_map[service_type]

    service_doc = await db[collection].find_one({"_id": ObjectId(service_id)})
    if not service_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{service_type} not found")

    # Dummy payment intent -- synchronous, no external dependency
    intent = create_payment_intent(
        amount,
        metadata={"user_id": user_id, "service_type": service_type, "service_id": service_id},
    )
    payment_intent_id: str = intent["id"]

    now = datetime.now(timezone.utc)
    booking_id = ObjectId()
    doc = {
        "_id": booking_id,
        "user_id": user_id,
        "service_type": service_type,
        "service_id": service_id,
        "status": BookingStatus.pending,
        "payment_intent_id": payment_intent_id,
        "amount": amount,
        "notes": notes,
        "created_at": now,
        "updated_at": now,
    }
    await db["bookings"].insert_one(doc)
    doc["id"] = str(booking_id)
    doc["_id"] = str(booking_id)
    doc["service_id"] = str(service_id)
    return doc
