import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List
from bson import ObjectId
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from app.core.database import get_database
from app.models.booking import ServiceType, BookingStatus
from app.services.booking_service import create_booking

logger = logging.getLogger(__name__)

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

async def _get_service_summary(db, service_type: str, service_id: str) -> str:
    """Helper to fetch and format service details for a booking."""
    try:
        collection = _get_collection_for_service(service_type)
        doc = await db[collection].find_one({"_id": ObjectId(service_id)})
        if not doc:
            return "Details unavailable"
            
        if service_type == "flight":
            return f"Flight: {doc.get('airline', 'N/A')} from {doc.get('origin', 'N/A')} to {doc.get('destination', 'N/A')}"
        elif service_type == "bus":
            return f"Bus: {doc.get('operator', 'N/A')} from {doc.get('origin', 'N/A')} to {doc.get('destination', 'N/A')}"
        elif service_type == "hotel":
            return f"Hotel: {doc.get('property_name', 'N/A')} in {doc.get('location', 'N/A')} ({doc.get('room_type', 'N/A')})"
        elif service_type == "activity":
            return f"Activity: {doc.get('activity_name', 'N/A')} in {doc.get('location', 'N/A')}"
        elif service_type == "guide":
            return f"Guide: {doc.get('guide_name', 'N/A')} (Specialities: {', '.join(doc.get('specialities', []))})"
        elif service_type == "car_rental":
            return f"Car Rental: {doc.get('company', 'N/A')} in {doc.get('location', 'N/A')} ({doc.get('vehicle_type', 'N/A')})"
    except Exception as e:
        logger.error(f"Error getting service summary: {e}")
    return "Details unavailable"

@tool
async def book_service(service_type: str, service_id: str, config: RunnableConfig) -> str:
    """
    Book a travel service for the user. This creates the initial booking in PENDING status.
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
        
        service_summary = await _get_service_summary(db, service_type, service_id)
        return (
            f"Successfully created a pending booking!\n"
            f"- **Booking ID**: {str(booking['_id'])}\n"
            f"- **Service Type**: {service_type.capitalize()}\n"
            f"- **Service Details**: {service_summary}\n"
            f"- **Amount Charged**: ${price:.2f}\n"
            f"- **Status**: PENDING. Please ask the user to confirm this booking to finalize."
        )
    except Exception as e:
        logger.error(f"Error booking service: {e}")
        return f"Error creating booking: {str(e)}"

@tool
async def confirm_booking(service_type: str, service_id: str, config: RunnableConfig) -> str:
    """
    Confirm a previously created pending booking. Use this after showing booking details to the user 
    and they have explicitly agreed.
    """
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."

    try:
        db = get_database()
        
        # Find the existing pending booking
        booking = await db.bookings.find_one({
            "user_id": user_id,
            "service_type": service_type,
            "service_id": service_id,
            "status": BookingStatus.pending.value
        })
        
        if not booking:
            # If no pending booking was found, check if it's already confirmed
            already_confirmed = await db.bookings.find_one({
                "user_id": user_id,
                "service_type": service_type,
                "service_id": service_id,
                "status": BookingStatus.confirmed.value
            })
            if already_confirmed:
                service_summary = await _get_service_summary(db, service_type, service_id)
                return f"This booking is already confirmed!\n- **Booking ID**: {str(already_confirmed['_id'])}\n- **Details**: {service_summary}"
                
            return f"Error: No pending booking found for {service_type} with ID {service_id}. Please create the booking first using book_service."
            
        # Update the status to confirmed
        await db.bookings.update_one(
            {"_id": booking["_id"]},
            {"$set": {"status": BookingStatus.confirmed.value, "updated_at": datetime.now(timezone.utc)}}
        )
        
        service_summary = await _get_service_summary(db, service_type, service_id)
        return (
            f"Success! Booking has been officially confirmed (payment simulated successfully).\n"
            f"- **Booking ID**: {str(booking['_id'])}\n"
            f"- **Service Details**: {service_summary}\n"
            f"- **Total Amount Paid**: ${booking['amount']:.2f}\n"
            f"- **Status**: CONFIRMED"
        )
    except Exception as e:
        logger.error(f"Error confirming booking: {e}")
        return f"Error confirming booking: {str(e)}"

@tool
async def cancel_booking(booking_id: str, config: RunnableConfig) -> str:
    """Cancel an active or pending booking."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        booking = await db.bookings.find_one({"_id": ObjectId(booking_id), "user_id": user_id})
        if not booking:
            return "Error: Booking not found or does not belong to you."
            
        if booking["status"] == BookingStatus.cancelled.value:
            return "This booking is already cancelled."
            
        result = await db.bookings.update_one(
            {"_id": ObjectId(booking_id), "user_id": user_id},
            {"$set": {"status": BookingStatus.cancelled.value, "updated_at": datetime.now(timezone.utc)}}
        )
        if result.modified_count == 1:
            service_summary = await _get_service_summary(db, booking["service_type"], booking["service_id"])
            return f"Successfully cancelled booking (ID: {booking_id}) for {service_summary}."
        return "Could not cancel this booking at this time."
    except Exception as e:
        logger.error(f"Error cancelling booking: {e}")
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
            return "You have no bookings recorded in our system yet."
            
        summaries = []
        for r in results:
            b_id = str(r["_id"])
            s_type = r.get("service_type")
            s_type_val = s_type.value if hasattr(s_type, "value") else str(s_type)
            status_val = r.get("status").value if hasattr(r.get("status"), "value") else str(r.get("status"))
            
            service_summary = await _get_service_summary(db, s_type_val, r["service_id"])
            
            summaries.append(
                f"- **Booking ID**: `{b_id}` | **Type**: {s_type_val.capitalize()} | **Details**: {service_summary} | **Amount**: ${r.get('amount'):.2f} | **Status**: {status_val.upper()}"
            )
            
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error fetching user bookings: {e}")
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
            
        b_id = str(doc["_id"])
        s_type = doc.get("service_type")
        s_type_val = s_type.value if hasattr(s_type, "value") else str(s_type)
        status_val = doc.get("status").value if hasattr(doc.get("status"), "value") else str(doc.get("status"))
        
        service_summary = await _get_service_summary(db, s_type_val, doc["service_id"])
        
        created = doc.get("created_at")
        created_str = created.isoformat() if hasattr(created, "isoformat") else str(created)
        
        return (
            f"### Booking details for `{b_id}`:\n"
            f"- **Type**: {s_type_val.capitalize()}\n"
            f"- **Service Details**: {service_summary}\n"
            f"- **Amount**: ${doc.get('amount'):.2f}\n"
            f"- **Status**: {status_val.upper()}\n"
            f"- **Created At**: {created_str}"
        )
    except Exception as e:
        logger.error(f"Error fetching booking detail: {e}")
        return f"Error fetching booking: {str(e)}"
