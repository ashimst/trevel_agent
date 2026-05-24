import json
from typing import Any, Dict, List, Optional
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from fastapi import HTTPException
from app.core.database import get_database
from app.services import trip_service

@tool
async def create_trip(name: str, description: str, config: RunnableConfig) -> str:
    """Create a new trip for the current user."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated. Please log in."
        
    try:
        db = get_database()
        trip = await trip_service.create_trip(db=db, user_id=user_id, name=name, description=description)
        # convert datetime for JSON
        if "created_at" in trip: trip["created_at"] = trip["created_at"].isoformat()
        if "updated_at" in trip: trip["updated_at"] = trip["updated_at"].isoformat()
        return json.dumps(trip)
    except Exception as e:
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
            return "You have no trips yet."
        for t in trips:
            if "created_at" in t: t["created_at"] = t["created_at"].isoformat()
            if "updated_at" in t: t["updated_at"] = t["updated_at"].isoformat()
        return json.dumps(trips)
    except Exception as e:
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
        if "created_at" in trip: trip["created_at"] = trip["created_at"].isoformat()
        if "updated_at" in trip: trip["updated_at"] = trip["updated_at"].isoformat()
        return json.dumps(trip)
    except HTTPException as e:
        return f"Error: {e.detail}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
async def remove_booking_from_trip(trip_id: str, booking_id: str, config: RunnableConfig) -> str:
    """Remove a booking from a trip."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        trip = await trip_service.remove_booking_from_trip(db=db, trip_id=trip_id, booking_id=booking_id, user_id=user_id)
        if "created_at" in trip: trip["created_at"] = trip["created_at"].isoformat()
        if "updated_at" in trip: trip["updated_at"] = trip["updated_at"].isoformat()
        return json.dumps(trip)
    except HTTPException as e:
        return f"Error: {e.detail}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
async def delete_trip(trip_id: str, config: RunnableConfig) -> str:
    """Delete a trip."""
    user_id = config.get("configurable", {}).get("user_id")
    if not user_id:
        return "Error: User is not authenticated."
        
    try:
        db = get_database()
        await trip_service.delete_trip(db=db, trip_id=trip_id, user_id=user_id)
        return "Trip deleted successfully."
    except HTTPException as e:
        return f"Error: {e.detail}"
    except Exception as e:
        return f"Error: {str(e)}"
