import json
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from app.core.database import get_database

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
        
    cursor = db.flights.find(query, {"_id": 1, "origin": 1, "destination": 1, "airline": 1, "price": 1, "departure_dt": 1, "available_seats": 1}).limit(10)
    results = await cursor.to_list(length=10)
    if not results:
        return "No flights found matching the criteria."
    for r in results:
        r["_id"] = str(r["_id"])
        if "departure_dt" in r:
            r["departure_dt"] = r["departure_dt"].isoformat()
    return json.dumps(results)

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
        
    cursor = db.buses.find(query, {"_id": 1, "origin": 1, "destination": 1, "operator": 1, "price": 1, "departure_dt": 1, "available_seats": 1}).limit(10)
    results = await cursor.to_list(length=10)
    if not results:
        return "No buses found matching the criteria."
    for r in results:
        r["_id"] = str(r["_id"])
        if "departure_dt" in r:
            r["departure_dt"] = r["departure_dt"].isoformat()
    return json.dumps(results)

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
        
    cursor = db.hotels.find(query, {"_id": 1, "property_name": 1, "location": 1, "room_type": 1, "price_per_night": 1, "available_rooms": 1}).limit(10)
    results = await cursor.to_list(length=10)
    if not results:
        return "No hotels found matching the criteria."
    for r in results:
        r["_id"] = str(r["_id"])
    return json.dumps(results)

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
        
    cursor = db.activities.find(query, {"_id": 1, "activity_name": 1, "location": 1, "price": 1}).limit(10)
    results = await cursor.to_list(length=10)
    if not results:
        return "No activities found matching the criteria."
    for r in results:
        r["_id"] = str(r["_id"])
    return json.dumps(results)

@tool
async def search_guides(language: Optional[str] = None, speciality: Optional[str] = None) -> str:
    """Search for travel guides based on language and speciality."""
    db = get_database()
    query = {}
    if language:
        query["languages"] = {"$regex": language, "$options": "i"}
    if speciality:
        query["specialities"] = {"$regex": speciality, "$options": "i"}
        
    cursor = db.guides.find(query, {"_id": 1, "guide_name": 1, "languages": 1, "specialities": 1, "daily_rate": 1}).limit(10)
    results = await cursor.to_list(length=10)
    if not results:
        return "No guides found matching the criteria."
    for r in results:
        r["_id"] = str(r["_id"])
    return json.dumps(results)

@tool
async def search_car_rentals(location: Optional[str] = None, vehicle_type: Optional[str] = None) -> str:
    """Search for car rentals based on location and vehicle type."""
    db = get_database()
    query = {}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if vehicle_type:
        query["vehicle_type"] = {"$regex": vehicle_type, "$options": "i"}
        
    cursor = db.car_rentals.find(query, {"_id": 1, "company": 1, "location": 1, "vehicle_type": 1, "price_per_day": 1}).limit(10)
    results = await cursor.to_list(length=10)
    if not results:
        return "No car rentals found matching the criteria."
    for r in results:
        r["_id"] = str(r["_id"])
    return json.dumps(results)

@tool
def search_web_for_travel_advice(query: str) -> str:
    """
    Search the web for real-time travel advice, trends, weather, or cultural information using Exa search.
    Use this sparingly, only when the internal database is insufficient to answer the user's travel question.
    """
    from exa_py import Exa
    from app.core.config import settings
    
    if not settings.EXA_API_KEY:
        return "Error: Exa API key is not configured."
        
    try:
        exa = Exa(api_key=settings.EXA_API_KEY)
        # We use a travel-specific category or general search
        result = exa.search_and_contents(
            query,
            type="neural",
            use_autoprompt=True,
            num_results=3,
            text=True
        )
        
        # Format the response
        formatted_results = []
        for item in result.results:
            formatted_results.append(f"Title: {item.title}\nURL: {item.url}\nSummary: {item.text[:500]}...")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"
