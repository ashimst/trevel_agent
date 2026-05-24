"""
seed.py -- Populate MongoDB with realistic sample data for all 6 service types.

Run with:
    python seed.py

Collections populated:
    flights, buses, hotels, activities, guides, car_rentals
"""
import asyncio
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Use timezone-aware UTC now to avoid deprecation warnings
def _now() -> datetime:
    return datetime.now(timezone.utc)

# ── Helpers ───────────────────────────────────────────────────────────────────

def dt(days_offset: int, hour: int = 8, minute: int = 0) -> datetime:
    """Return a timezone-aware datetime N days from today at hh:mm UTC."""
    base = datetime.now(timezone.utc).replace(hour=hour, minute=minute, second=0, microsecond=0)
    return base + timedelta(days=days_offset)


# ── Seed data ─────────────────────────────────────────────────────────────────

FLIGHTS = [
    {
        "origin": "New York (JFK)",
        "destination": "London (LHR)",
        "departure_dt": dt(3, 10, 30),
        "airline": "British Airways",
        "seat_class": "economy",
        "available_seats": 48,
        "price": 520.00,
        "created_at": _now(),
    },
    {
        "origin": "London (LHR)",
        "destination": "Dubai (DXB)",
        "departure_dt": dt(5, 14, 0),
        "airline": "Emirates",
        "seat_class": "business",
        "available_seats": 12,
        "price": 1850.00,
        "created_at": _now(),
    },
    {
        "origin": "Dubai (DXB)",
        "destination": "Kathmandu (KTM)",
        "departure_dt": dt(7, 6, 15),
        "airline": "Air Arabia",
        "seat_class": "economy",
        "available_seats": 30,
        "price": 310.00,
        "created_at": _now(),
    },
    {
        "origin": "Singapore (SIN)",
        "destination": "Tokyo (NRT)",
        "departure_dt": dt(4, 9, 0),
        "airline": "Singapore Airlines",
        "seat_class": "first",
        "available_seats": 4,
        "price": 4200.00,
        "created_at": _now(),
    },
    {
        "origin": "Paris (CDG)",
        "destination": "New York (JFK)",
        "departure_dt": dt(6, 11, 45),
        "airline": "Air France",
        "seat_class": "economy",
        "available_seats": 60,
        "price": 480.00,
        "created_at": _now(),
    },
    {
        "origin": "Nairobi (NBO)",
        "destination": "Johannesburg (JNB)",
        "departure_dt": dt(2, 7, 0),
        "airline": "Kenya Airways",
        "seat_class": "economy",
        "available_seats": 35,
        "price": 195.00,
        "created_at": _now(),
    },
]

BUSES = [
    {
        "origin": "Kathmandu",
        "destination": "Pokhara",
        "departure_dt": dt(1, 6, 30),
        "operator": "Greenline Travels",
        "seat_number": "A1",
        "available_seats": 20,
        "price": 18.00,
        "created_at": _now(),
    },
    {
        "origin": "London Victoria",
        "destination": "Edinburgh",
        "departure_dt": dt(2, 8, 0),
        "operator": "National Express",
        "seat_number": "B5",
        "available_seats": 35,
        "price": 42.00,
        "created_at": _now(),
    },
    {
        "origin": "Bangkok",
        "destination": "Chiang Mai",
        "departure_dt": dt(3, 19, 0),
        "operator": "Nakhonchai Air",
        "seat_number": "C3",
        "available_seats": 28,
        "price": 22.50,
        "created_at": _now(),
    },
    {
        "origin": "Mumbai",
        "destination": "Goa",
        "departure_dt": dt(1, 21, 30),
        "operator": "Paulo Travels",
        "seat_number": "D2",
        "available_seats": 18,
        "price": 14.00,
        "created_at": _now(),
    },
    {
        "origin": "Nairobi",
        "destination": "Mombasa",
        "departure_dt": dt(2, 7, 0),
        "operator": "Easy Coach",
        "seat_number": "A7",
        "available_seats": 40,
        "price": 11.00,
        "created_at": _now(),
    },
]

HOTELS = [
    {
        "property_name": "The Ritz London",
        "location": "London, United Kingdom",
        "check_in": dt(5, 14, 0),
        "check_out": dt(8, 11, 0),
        "room_type": "deluxe",
        "available_rooms": 5,
        "price_per_night": 650.00,
        "created_at": _now(),
    },
    {
        "property_name": "Burj Al Arab",
        "location": "Dubai, UAE",
        "check_in": dt(6, 15, 0),
        "check_out": dt(10, 12, 0),
        "room_type": "suite",
        "available_rooms": 2,
        "price_per_night": 2800.00,
        "created_at": _now(),
    },
    {
        "property_name": "Hotel Shanker",
        "location": "Kathmandu, Nepal",
        "check_in": dt(7, 12, 0),
        "check_out": dt(12, 11, 0),
        "room_type": "standard",
        "available_rooms": 15,
        "price_per_night": 95.00,
        "created_at": _now(),
    },
    {
        "property_name": "Aman Tokyo",
        "location": "Tokyo, Japan",
        "check_in": dt(4, 15, 0),
        "check_out": dt(7, 11, 0),
        "room_type": "suite",
        "available_rooms": 3,
        "price_per_night": 1200.00,
        "created_at": _now(),
    },
    {
        "property_name": "Radisson Blu Nairobi",
        "location": "Nairobi, Kenya",
        "check_in": dt(3, 14, 0),
        "check_out": dt(6, 11, 0),
        "room_type": "deluxe",
        "available_rooms": 10,
        "price_per_night": 180.00,
        "created_at": _now(),
    },
    {
        "property_name": "Ibis Budget Paris Ornano",
        "location": "Paris, France",
        "check_in": dt(6, 14, 0),
        "check_out": dt(9, 11, 0),
        "room_type": "standard",
        "available_rooms": 20,
        "price_per_night": 75.00,
        "created_at": _now(),
    },
]

ACTIVITIES = [
    {
        "name": "Everest Base Camp Trek — Day 1 Orientation",
        "location": "Lukla, Nepal",
        "date": dt(8, 7, 0),
        "duration_hours": 6.0,
        "max_participants": 12,
        "price": 85.00,
        "created_at": _now(),
    },
    {
        "name": "Desert Safari with BBQ Dinner",
        "location": "Dubai, UAE",
        "date": dt(7, 15, 0),
        "duration_hours": 5.0,
        "max_participants": 20,
        "price": 75.00,
        "created_at": _now(),
    },
    {
        "name": "Thames River Cruise",
        "location": "London, United Kingdom",
        "date": dt(6, 11, 0),
        "duration_hours": 2.0,
        "max_participants": 50,
        "price": 28.00,
        "created_at": _now(),
    },
    {
        "name": "Tsukiji Fish Market Early Morning Tour",
        "location": "Tokyo, Japan",
        "date": dt(5, 5, 30),
        "duration_hours": 3.0,
        "max_participants": 8,
        "price": 60.00,
        "created_at": _now(),
    },
    {
        "name": "Maasai Mara Hot Air Balloon Safari",
        "location": "Maasai Mara, Kenya",
        "date": dt(4, 5, 30),
        "duration_hours": 3.5,
        "max_participants": 16,
        "price": 450.00,
        "created_at": _now(),
    },
    {
        "name": "Eiffel Tower Skip-the-Line Summit Tour",
        "location": "Paris, France",
        "date": dt(7, 10, 0),
        "duration_hours": 2.0,
        "max_participants": 25,
        "price": 55.00,
        "created_at": _now(),
    },
    {
        "name": "Phang Nga Bay Kayaking & James Bond Island",
        "location": "Phuket, Thailand",
        "date": dt(3, 8, 0),
        "duration_hours": 8.0,
        "max_participants": 15,
        "price": 95.00,
        "created_at": _now(),
    },
]

GUIDES = [
    {
        "name": "Pemba Sherpa",
        "languages": ["English", "Nepali", "Tibetan"],
        "speciality": "Himalayan Trekking & High Altitude",
        "daily_rate": 120.00,
        "available_from": dt(5, 8, 0),
        "available_to": dt(60, 18, 0),
        "bio": (
            "Certified Himalayan trekking guide with 14 years of experience leading groups "
            "to Everest Base Camp, Annapurna Circuit, and Langtang Valley. "
            "UIAGM certified mountain guide."
        ),
        "created_at": _now(),
    },
    {
        "name": "Fatima Al-Rashid",
        "languages": ["English", "Arabic", "French"],
        "speciality": "Desert Culture & Heritage",
        "daily_rate": 200.00,
        "available_from": dt(3, 8, 0),
        "available_to": dt(45, 18, 0),
        "bio": (
            "Award-winning cultural guide based in Dubai. Specialist in UAE heritage, "
            "falconry traditions, and Arabian cuisine experiences. "
            "Dubai Tourism Board certified."
        ),
        "created_at": _now(),
    },
    {
        "name": "James Ochieng",
        "languages": ["English", "Swahili", "Luo"],
        "speciality": "Wildlife Safari & Birding",
        "daily_rate": 150.00,
        "available_from": dt(2, 6, 0),
        "available_to": dt(90, 18, 0),
        "bio": (
            "Professional safari guide with Kenya Wildlife Service certification. "
            "Specialist in Big Five tracking across Maasai Mara and Amboseli. "
            "Passionate bird-watcher with 800+ species identified."
        ),
        "created_at": _now(),
    },
    {
        "name": "Yuki Tanaka",
        "languages": ["English", "Japanese", "Mandarin"],
        "speciality": "Traditional Japan & Culinary Arts",
        "daily_rate": 180.00,
        "available_from": dt(4, 9, 0),
        "available_to": dt(50, 18, 0),
        "bio": (
            "Tokyo-based cultural ambassador specialising in tea ceremony, sake brewing tours, "
            "Tsukiji market deep-dives, and hidden Kyoto neighbourhood walks."
        ),
        "created_at": _now(),
    },
    {
        "name": "Sophie Beaumont",
        "languages": ["English", "French", "Spanish"],
        "speciality": "Art, Architecture & Gastronomy",
        "daily_rate": 160.00,
        "available_from": dt(6, 9, 0),
        "available_to": dt(70, 18, 0),
        "bio": (
            "Former Louvre museum educator turned private guide. "
            "Curates bespoke Paris experiences from impressionist art walks to "
            "Michelin-star restaurant introductions."
        ),
        "created_at": _now(),
    },
]

CAR_RENTALS = [
    {
        "vehicle_type": "SUV",
        "vehicle_name": "Toyota Land Cruiser",
        "pickup_location": "Nairobi Jomo Kenyatta Airport",
        "pickup_dt": dt(3, 10, 0),
        "dropoff_dt": dt(10, 10, 0),
        "price_per_day": 95.00,
        "available": True,
        "created_at": _now(),
    },
    {
        "vehicle_type": "sedan",
        "vehicle_name": "Toyota Camry",
        "pickup_location": "Dubai International Airport",
        "pickup_dt": dt(6, 12, 0),
        "dropoff_dt": dt(11, 12, 0),
        "price_per_day": 55.00,
        "available": True,
        "created_at": _now(),
    },
    {
        "vehicle_type": "van",
        "vehicle_name": "Ford Transit (7-seater)",
        "pickup_location": "London Heathrow Airport",
        "pickup_dt": dt(5, 11, 0),
        "dropoff_dt": dt(8, 11, 0),
        "price_per_day": 110.00,
        "available": True,
        "created_at": _now(),
    },
    {
        "vehicle_type": "motorcycle",
        "vehicle_name": "Honda CB500F",
        "pickup_location": "Chiang Mai City Centre",
        "pickup_dt": dt(2, 9, 0),
        "dropoff_dt": dt(5, 9, 0),
        "price_per_day": 22.00,
        "available": True,
        "created_at": _now(),
    },
    {
        "vehicle_type": "sedan",
        "vehicle_name": "Renault Clio",
        "pickup_location": "Paris Charles de Gaulle Airport",
        "pickup_dt": dt(6, 13, 0),
        "dropoff_dt": dt(9, 13, 0),
        "price_per_day": 45.00,
        "available": True,
        "created_at": _now(),
    },
    {
        "vehicle_type": "SUV",
        "vehicle_name": "Hyundai Tucson",
        "pickup_location": "Kathmandu Tribhuvan Airport",
        "pickup_dt": dt(7, 10, 0),
        "dropoff_dt": dt(14, 10, 0),
        "price_per_day": 48.00,
        "available": True,
        "created_at": _now(),
    },
]


# ── Main seeder ───────────────────────────────────────────────────────────────

async def seed():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    collections = {
        "flights": FLIGHTS,
        "buses": BUSES,
        "hotels": HOTELS,
        "activities": ACTIVITIES,
        "guides": GUIDES,
        "car_rentals": CAR_RENTALS,
    }

    for col_name, data in collections.items():
        col = db[col_name]
        existing = await col.count_documents({})
        if existing > 0:
            print(f"  [skip] {col_name}: {existing} docs already exist (use --force to overwrite)")
        else:
            result = await col.insert_many(data)
            print(f"  [ok]   {col_name}: inserted {len(result.inserted_ids)} documents")

    client.close()
    print("\nDone! Seed data is ready.")


if __name__ == "__main__":
    import sys

    if "--force" in sys.argv:
        async def force_seed():
            client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = client[settings.DATABASE_NAME]
            for col_name in ("flights", "buses", "hotels", "activities", "guides", "car_rentals"):
                await db[col_name].drop()
                print(f"  [drop] {col_name}")
            client.close()
            await seed()
        asyncio.run(force_seed())
    else:
        asyncio.run(seed())
