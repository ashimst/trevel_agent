import json
from typing import Any, Dict, List
from bson import ObjectId
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from app.core.database import get_database
from app.models.booking import ServiceType, BookingStatus
from app.services.booking_service import create_booking

def _get_collection_for_service(service_type: str) -> str:
    collection_map = {
        "flight": "flights",
        "bus": "buses",
        "hotel": "hotels",
        "activity": "activities",
        "guide": "guides",
        "car_rental": "car_rentals",
    }
    if service_type not in collection_map:
        raise ValueError(f"Invalid service type: {service_type}")
    return collection_map[service_type]

async def _get_service_price(db, service_type: str, service_id: str) -> float:
    collection = _get_collection_for_service(service_type)
    doc = await db[collection].find_one({"_id": ObjectId(service_id)})
    if not doc:
        raise ValueError(f"Service not found: {service_id}")
    
    # Extract price based on type
    if service_type in ("flight", "bus", "activity"):
        return doc.get("price", 0.0)
    elif service_type == "hotel":
        return doc.get("price_per_night", 0.0)
    elif service_type == "guide":
        return doc.get("daily_rate", 0.0)
    elif service_type == "car_rental":
        return doc.get("price_per_day", 0.0)
    return 0.0

@tool
async def book_service(service_type: str, service_id: str, config: RunnableConfig) -> str:
    """
    Book a travel service for the user. This creates the actual booking in the system.
    Pass the service_type (flight, bus, hotel, activity, guide, car_rental) and the service_id.
    """
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated. Please log in to book."

    try:
        db = get_database()
        collection = _get_collection_for_service(service_type)
        doc = await db[collection].find_one({"_id": ObjectId(service_id)})
        if not doc:
            return f"Error: {service_type} not found in our system."
            
        price = await _get_service_price(db, service_type, service_id)
        
        # Actually create the booking in the database
        booking = await create_booking(
            db=db,
            user_id=user_id,
            service_type=ServiceType(service_type),
            service_id=service_id,
            amount=price
        )
        
        # Clean up the service doc for presentation
        doc["_id"] = str(doc["_id"])
        for k, v in doc.items():
            if hasattr(v, "isoformat"):
                doc[k] = v.isoformat()
                
        return f"Booking created successfully! Service details: {json.dumps(doc)}. Amount charged: ${price:.2f}. Booking status: pending payment."
    except Exception as e:
        return f"Error creating booking: {str(e)}"

@tool
async def confirm_booking(service_type: str, service_id: str, config: RunnableConfig) -> str:
    """
    Confirm a previously created booking. Use this after showing booking details to the user 
    and they have explicitly agreed.
    """
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."

    try:
        db = get_database()
        price = await _get_service_price(db, service_type, service_id)
        
        # Create the booking
        booking = await create_booking(
            db=db,
            user_id=user_id,
            service_type=ServiceType(service_type),
            service_id=service_id,
            amount=price
        )
        return f"Booking confirmed! Amount: ${booking['amount']:.2f}. Status: pending payment."
    except Exception as e:
        return f"Error confirming booking: {str(e)}"

@tool
async def cancel_booking(booking_id: str, config: RunnableConfig) -> str:
    """Cancel a pending booking."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        result = await db.bookings.update_one(
            {"_id": ObjectId(booking_id), "user_id": user_id, "status": BookingStatus.pending},
            {"$set": {"status": BookingStatus.cancelled.value}}
        )
        if result.modified_count == 1:
            return "Booking cancelled successfully."
        return "Could not cancel this booking. It may not exist, belong to another user, or is no longer in pending status."
    except Exception as e:
        return f"Error cancelling booking: {str(e)}"

@tool
async def get_my_bookings(config: RunnableConfig) -> str:
    """Get all bookings for the current user."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        cursor = db.bookings.find({"user_id": user_id})
        results = await cursor.to_list(length=50)
        if not results:
            return "You have no bookings yet."
        for r in results:
            r["_id"] = str(r["_id"])
            if "created_at" in r:
                r["created_at"] = r["created_at"].isoformat()
            if "updated_at" in r:
                r["updated_at"] = r["updated_at"].isoformat()
            # Convert enums to strings
            if "service_type" in r and hasattr(r["service_type"], "value"):
                r["service_type"] = r["service_type"].value
            if "status" in r and hasattr(r["status"], "value"):
                r["status"] = r["status"].value
        return json.dumps(results)
    except Exception as e:
        return f"Error fetching bookings: {str(e)}"

@tool
async def get_booking_detail(booking_id: str, config: RunnableConfig) -> str:
    """Get details of a specific booking."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        doc = await db.bookings.find_one({"_id": ObjectId(booking_id), "user_id": user_id})
        if not doc:
            return "Booking not found."
            
        doc["_id"] = str(doc["_id"])
        if "created_at" in doc:
            doc["created_at"] = doc["created_at"].isoformat()
        if "updated_at" in doc:
            doc["updated_at"] = doc["updated_at"].isoformat()
        if "service_type" in doc and hasattr(doc["service_type"], "value"):
            doc["service_type"] = doc["service_type"].value
        if "status" in doc and hasattr(doc["status"], "value"):
            doc["status"] = doc["status"].value
        return json.dumps(doc)
    except Exception as e:
        return f"Error fetching booking: {str(e)}"
