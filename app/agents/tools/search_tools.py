import json
import logging
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from app.core.database import get_database

logger = logging.getLogger(__name__)

def format_item_summary(item: Dict[str, Any], service_type: str) -> str:
    """Helper to format a database service item into a rich, human-readable string."""
    try:
        item_id = str(item.get("_id", ""))
        if service_type == "flight":
            dep = item.get("departure_dt")
            dep_str = dep.isoformat() if hasattr(dep, "isoformat") else str(dep)
            return (
                f"- **Flight (ID: {item_id})**: {item.get('airline', 'Unknown Airline')} "
                f"from {item.get('origin', 'N/A')} to {item.get('destination', 'N/A')}. "
                f"Departure: {dep_str}. Price: ${item.get('price')}. Available Seats: {item.get('available_seats')}."
            )
        elif service_type == "bus":
            dep = item.get("departure_dt")
            dep_str = dep.isoformat() if hasattr(dep, "isoformat") else str(dep)
            return (
                f"- **Bus (ID: {item_id})**: {item.get('operator', 'Unknown Operator')} "
                f"from {item.get('origin', 'N/A')} to {item.get('destination', 'N/A')}. "
                f"Departure: {dep_str}. Price: ${item.get('price')}. Available Seats: {item.get('available_seats')}."
            )
        elif service_type == "hotel":
            return (
                f"- **Hotel (ID: {item_id})**: {item.get('property_name', 'Unknown Hotel')} "
                f"in {item.get('location', 'N/A')}. Room Type: {item.get('room_type', 'N/A')}. "
                f"Rate: ${item.get('price_per_night')}/night. Available Rooms: {item.get('available_rooms')}."
            )
        elif service_type == "activity":
            return (
                f"- **Activity (ID: {item_id})**: {item.get('activity_name', 'Unknown Activity')} "
                f"in {item.get('location', 'N/A')}. Price: ${item.get('price')}."
            )
        elif service_type == "guide":
            specialities = ", ".join(item.get("specialities", [])) if isinstance(item.get("specialities"), list) else str(item.get("specialities", "N/A"))
            languages = ", ".join(item.get("languages", [])) if isinstance(item.get("languages"), list) else str(item.get("languages", "N/A"))
            return (
                f"- **Guide (ID: {item_id})**: {item.get('guide_name', 'Unknown Guide')}. "
                f"Specialities: {specialities}. Languages: {languages}. Daily Rate: ${item.get('daily_rate')}."
            )
        elif service_type == "car_rental":
            return (
                f"- **Car Rental (ID: {item_id})**: {item.get('company', 'Unknown Rental')} "
                f"in {item.get('location', 'N/A')}. Vehicle: {item.get('vehicle_type', 'N/A')}. "
                f"Rate: ${item.get('price_per_day')}/day."
            )
    except Exception as e:
        logger.error(f"Error formatting item of type {service_type}: {e}")
    return f"- Unknown {service_type} item details: {item}"

@tool
async def search_flights(origin: Optional[str] = None, destination: Optional[str] = None, max_price: Optional[float] = None) -> str:
    """Search for available flights based on origin, destination, and maximum price."""
    db = get_database()
    query = {}
    if origin:
        query["origin"] = {"$regex": origin, "$options": "i"}
    if destination:
        query["destination"] = {"$regex": destination, "$options": "i"}
    if max_price:
        query["price"] = {"$lte": max_price}
        
    try:
        cursor = db.flights.find(query, {"_id": 1, "origin": 1, "destination": 1, "airline": 1, "price": 1, "departure_dt": 1, "available_seats": 1}).limit(10)
        results = await cursor.to_list(length=10)
        if not results:
            return "No flights found matching the criteria in our database."
        
        summaries = [format_item_summary(r, "flight") for r in results]
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in search_flights: {e}")
        return "An error occurred while searching for flights. Please try again."

@tool
async def search_buses(origin: Optional[str] = None, destination: Optional[str] = None, max_price: Optional[float] = None) -> str:
    """Search for available buses based on origin, destination, and maximum price."""
    db = get_database()
    query = {}
    if origin:
        query["origin"] = {"$regex": origin, "$options": "i"}
    if destination:
        query["destination"] = {"$regex": destination, "$options": "i"}
    if max_price:
        query["price"] = {"$lte": max_price}
        
    try:
        cursor = db.buses.find(query, {"_id": 1, "origin": 1, "destination": 1, "operator": 1, "price": 1, "departure_dt": 1, "available_seats": 1}).limit(10)
        results = await cursor.to_list(length=10)
        if not results:
            return "No buses found matching the criteria in our database."
        
        summaries = [format_item_summary(r, "bus") for r in results]
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in search_buses: {e}")
        return "An error occurred while searching for buses. Please try again."

@tool
async def search_hotels(location: Optional[str] = None, room_type: Optional[str] = None, max_price_per_night: Optional[float] = None) -> str:
    """Search for available hotels based on location, room type, and maximum price per night."""
    db = get_database()
    query = {}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if room_type:
        query["room_type"] = {"$regex": room_type, "$options": "i"}
    if max_price_per_night:
        query["price_per_night"] = {"$lte": max_price_per_night}
        
    try:
        cursor = db.hotels.find(query, {"_id": 1, "property_name": 1, "location": 1, "room_type": 1, "price_per_night": 1, "available_rooms": 1}).limit(10)
        results = await cursor.to_list(length=10)
        if not results:
            return "No hotels found matching the criteria in our database."
        
        summaries = [format_item_summary(r, "hotel") for r in results]
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in search_hotels: {e}")
        return "An error occurred while searching for hotels. Please try again."

@tool
async def search_activities(location: Optional[str] = None, max_price: Optional[float] = None, name_keyword: Optional[str] = None) -> str:
    """Search for available activities based on location, name keyword, and maximum price."""
    db = get_database()
    query = {}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if name_keyword:
        query["activity_name"] = {"$regex": name_keyword, "$options": "i"}
    if max_price:
        query["price"] = {"$lte": max_price}
        
    try:
        cursor = db.activities.find(query, {"_id": 1, "activity_name": 1, "location": 1, "price": 1}).limit(10)
        results = await cursor.to_list(length=10)
        if not results:
            return "No activities found matching the criteria in our database."
        
        summaries = [format_item_summary(r, "activity") for r in results]
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in search_activities: {e}")
        return "An error occurred while searching for activities. Please try again."

@tool
async def search_guides(language: Optional[str] = None, speciality: Optional[str] = None) -> str:
    """Search for travel guides based on language and speciality."""
    db = get_database()
    query = {}
    if language:
        query["languages"] = {"$regex": language, "$options": "i"}
    if speciality:
        query["specialities"] = {"$regex": speciality, "$options": "i"}
        
    try:
        cursor = db.guides.find(query, {"_id": 1, "guide_name": 1, "languages": 1, "specialities": 1, "daily_rate": 1}).limit(10)
        results = await cursor.to_list(length=10)
        if not results:
            return "No guides found matching the criteria in our database."
        
        summaries = [format_item_summary(r, "guide") for r in results]
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in search_guides: {e}")
        return "An error occurred while searching for guides. Please try again."

@tool
async def search_car_rentals(location: Optional[str] = None, vehicle_type: Optional[str] = None) -> str:
    """Search for car rentals based on location and vehicle type."""
    db = get_database()
    query = {}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if vehicle_type:
        query["vehicle_type"] = {"$regex": vehicle_type, "$options": "i"}
        
    try:
        cursor = db.car_rentals.find(query, {"_id": 1, "company": 1, "location": 1, "vehicle_type": 1, "price_per_day": 1}).limit(10)
        results = await cursor.to_list(length=10)
        if not results:
            return "No car rentals found matching the criteria in our database."
        
        summaries = [format_item_summary(r, "car_rental") for r in results]
        return "\n".join(summaries)
    except Exception as e:
        logger.error(f"Error in search_car_rentals: {e}")
        return "An error occurred while searching for car rentals. Please try again."

@tool
async def search_all_services(location: str) -> str:
    """
    Search across flights, hotels, buses, activities, guides, and car rentals for a given location or destination.
    Use this to get a comprehensive overview of all services available in our database for a destination.
    """
    db = get_database()
    query_loc = {"$regex": location, "$options": "i"}
    
    # We perform concurrent searches using db collections
    # Flights and buses use destination match
    flight_cursor = db.flights.find({"destination": query_loc}).limit(5)
    bus_cursor = db.buses.find({"destination": query_loc}).limit(5)
    hotel_cursor = db.hotels.find({"location": query_loc}).limit(5)
    activity_cursor = db.activities.find({"location": query_loc}).limit(5)
    guide_cursor = db.guides.find({"specialities": query_loc}).limit(5)
    car_cursor = db.car_rentals.find({"location": query_loc}).limit(5)
    
    try:
        flights = await flight_cursor.to_list(length=5)
        buses = await bus_cursor.to_list(length=5)
        hotels = await hotel_cursor.to_list(length=5)
        activities = await activity_cursor.to_list(length=5)
        guides = await guide_cursor.to_list(length=5)
        cars = await car_cursor.to_list(length=5)
        
        sections = []
        sections.append(f"### Database Search Results for '{location}'")
        
        if flights:
            sections.append("\n**Flights:**\n" + "\n".join([format_item_summary(f, "flight") for f in flights]))
        if buses:
            sections.append("\n**Buses:**\n" + "\n".join([format_item_summary(b, "bus") for b in buses]))
        if hotels:
            sections.append("\n**Hotels:**\n" + "\n".join([format_item_summary(h, "hotel") for h in hotels]))
        if activities:
            sections.append("\n**Activities:**\n" + "\n".join([format_item_summary(a, "activity") for a in activities]))
        if guides:
            sections.append("\n**Local Guides:**\n" + "\n".join([format_item_summary(g, "guide") for g in guides]))
        if cars:
            sections.append("\n**Car Rentals:**\n" + "\n".join([format_item_summary(c, "car_rental") for c in cars]))
            
        if len(sections) == 1:
            return f"No bookable services found for '{location}' in our database inventory. You can still plan a trip here, but actual bookings will need to select from other destinations in our database."
            
        return "\n".join(sections)
    except Exception as e:
        logger.error(f"Error in search_all_services: {e}")
        return f"An error occurred while compiling inventory for '{location}'. Please try again."

@tool
def search_web_for_travel_advice(query: str) -> str:
    """
    Search the web for real-time travel advice, trends, weather, or cultural information using Exa search.
    Use this sparingly, only when the internal database is insufficient to answer the user's travel question.
    """
    from exa_py import Exa
    from app.core.config import settings
    
    if not settings.EXA_API_KEY:
        return "Error: Exa API key is not configured. Web search is currently unavailable."
        
    try:
        exa = Exa(api_key=settings.EXA_API_KEY)
        result = exa.search_and_contents(
            query,
            type="neural",
            num_results=3,
            text=True
        )
        
        formatted_results = []
        for item in result.results:
            text_snippet = item.text[:500] if item.text else "No content preview available."
            formatted_results.append(f"Title: {item.title}\nURL: {item.url}\nSummary: {text_snippet}...")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Error in search_web_for_travel_advice: {e}")
        return f"Web search service is currently encountering an issue: {str(e)}"
