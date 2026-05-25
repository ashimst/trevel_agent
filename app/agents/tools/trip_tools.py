import json
import logging
from typing import Any, Dict, List, Optional
from bson import ObjectId
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from fastapi import HTTPException
from app.core.database import get_database
from app.services import trip_service

logger = logging.getLogger(__name__)

async def _format_trip_summary(db, trip: Dict[str, Any]) -> str:
    """Format a trip object as a beautiful markdown description, resolving all bookings."""
    trip_id = str(trip.get("_id"))
    name = trip.get("name")
    desc = trip.get("description") or "No description provided."
    booking_ids = trip.get("booking_ids", [])
    
    lines = [
        f"### 🌴 Trip: **{name}**",
        f"- **Trip ID**: `{trip_id}`",
        f"- **Description**: {desc}",
        f"- **Total Bookings**: {len(booking_ids)}"
    ]
    
    if not booking_ids:
        lines.append("- *No bookings have been added to this trip's agenda yet.*")
    else:
        lines.append("- **Agenda Details:**")
        from app.agents.tools.booking_tools import _get_service_summary
        for b_id in booking_ids:
            try:
                booking = await db.bookings.find_one({"_id": ObjectId(b_id)})
                if booking:
                    s_type = booking.get("service_type")
                    s_type_val = s_type.value if hasattr(s_type, "value") else str(s_type)
                    status_val = booking.get("status").value if hasattr(booking.get("status"), "value") else str(booking.get("status"))
                    details = await _get_service_summary(db, s_type_val, booking.get("service_id"))
                    lines.append(f"  - **{s_type_val.capitalize()}** (Booking ID: `{b_id}`): {details} | Status: *{status_val.upper()}*")
                else:
                    lines.append(f"  - Booking `{b_id}`: *Booking details not found in database*")
            except Exception as e:
                logger.error(f"Error resolving booking {b_id} for trip summary: {e}")
                lines.append(f"  - Booking `{b_id}`: *Error retrieving details*")
                
    return "\n".join(lines)

@tool
async def create_trip(name: str, description: str, config: RunnableConfig) -> str:
    """Create a new trip for the current user."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated. Please log in."
        
    try:
        db = get_database()
        trip = await trip_service.create_trip(db=db, user_id=user_id, name=name, description=description)
        summary = await _format_trip_summary(db, trip)
        return f"Trip created successfully!\n\n{summary}"
    except Exception as e:
        logger.error(f"Error in create_trip: {e}")
        return f"Error creating trip: {str(e)}"

@tool
async def get_my_trips(config: RunnableConfig) -> str:
    """List all trips created by the current user."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        trips = await trip_service.get_user_trips(db=db, user_id=user_id)
        if not trips:
            return "You have no trips planned yet. Would you like me to help you create one?"
            
        summaries = []
        for trip in trips:
            summary = await _format_trip_summary(db, trip)
            summaries.append(summary)
            
        return "\n\n---\n\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in get_my_trips: {e}")
        return f"Error fetching trips: {str(e)}"

@tool
async def add_booking_to_trip(trip_id: str, booking_id: str, config: RunnableConfig) -> str:
    """Add an existing booking to a trip."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        trip = await trip_service.add_booking_to_trip(db=db, trip_id=trip_id, booking_id=booking_id, user_id=user_id)
        summary = await _format_trip_summary(db, trip)
        return f"Booking added to trip successfully!\n\n{summary}"
    except HTTPException as e:
        return f"Error adding booking: {e.detail}"
    except Exception as e:
        logger.error(f"Error in add_booking_to_trip: {e}")
        return f"Error adding booking: {str(e)}"

@tool
async def remove_booking_from_trip(trip_id: str, booking_id: str, config: RunnableConfig) -> str:
    """Remove a booking from a trip."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        trip = await trip_service.remove_booking_from_trip(db=db, trip_id=trip_id, booking_id=booking_id, user_id=user_id)
        summary = await _format_trip_summary(db, trip)
        return f"Booking removed from trip successfully.\n\n{summary}"
    except HTTPException as e:
        return f"Error removing booking: {e.detail}"
    except Exception as e:
        logger.error(f"Error in remove_booking_from_trip: {e}")
        return f"Error removing booking: {str(e)}"

@tool
async def delete_trip(trip_id: str, config: RunnableConfig) -> str:
    """Delete a trip."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        await trip_service.delete_trip(db=db, trip_id=trip_id, user_id=user_id)
        return f"Trip `{trip_id}` has been successfully deleted."
    except HTTPException as e:
        return f"Error deleting trip: {e.detail}"
    except Exception as e:
        logger.error(f"Error in delete_trip: {e}")
        return f"Error: {str(e)}"
