from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

from app.agents.llms import (
    get_planner_llm,
    get_booking_llm,
    get_support_llm,
    get_recommender_llm,
    get_trip_llm
)
from app.agents.tools.search_tools import (
    search_flights, search_hotels, search_buses, search_activities,
    search_guides, search_car_rentals, search_web_for_travel_advice
)
from app.agents.tools.booking_tools import (
    book_service, confirm_booking, cancel_booking, get_my_bookings, get_booking_detail
)
from app.agents.tools.trip_tools import (
    create_trip, get_my_trips, add_booking_to_trip, remove_booking_from_trip, delete_trip
)

# ── Shared persona rules injected into every agent ──────────────────────
CONCIERGE_RULES = """
STRICT RULES YOU MUST FOLLOW:
1. NEVER mention internal IDs, database fields, service_id, _id, user_id, or any technical identifiers to the user.
2. NEVER mention tool names, function names, or say things like "I will call a function" or "The tool returned". Act as if you know the information naturally.
3. If you need an internal ID to perform an action (like booking), silently use your search tools behind the scenes to find it. NEVER ask the user for an ID.
4. Present information beautifully — destinations, prices, dates, and descriptions only. The user is a traveler, not an engineer.
5. Be warm, enthusiastic, and conversational. You are a premium travel concierge.
"""


def create_planner_agent():
    """Google Gemma 27B — reliable tool calling for search."""
    tools = [search_flights, search_hotels, search_buses, search_activities]
    prompt = SystemMessage(content=(
        "You are a premium Travel Planner concierge. "
        "Help users discover flights, buses, hotels, and activities for their trips. "
        "When presenting results, go beyond raw data — share your knowledge about the destinations, "
        "suggest the best times to visit, mention local culture and weather, and make the user excited. "
        "Always search first, then present the results in a beautiful, organized way.\n"
        f"{CONCIERGE_RULES}"
    ))
    return create_react_agent(get_planner_llm(), tools, prompt=prompt)


def create_booking_agent():
    """NVIDIA Qwen 32B — strong reasoning for multi-step booking flows."""
    tools = [
        search_flights, search_hotels, search_buses, search_activities,
        search_guides, search_car_rentals,
        book_service, confirm_booking, cancel_booking, get_my_bookings
    ]
    prompt = SystemMessage(content=(
        "You are a meticulous Booking Agent concierge. You handle all reservations for the user.\n\n"
        "BOOKING WORKFLOW:\n"
        "1. If a user says 'book me a flight to Paris', you MUST first search for available flights autonomously, "
        "then present the best options with prices, airlines, and times.\n"
        "2. Once the user picks an option, call book_service with the correct service_type and service_id (which you found from your search).\n"
        "3. Show the user the booking summary and ask for confirmation.\n"
        "4. Only call confirm_booking after the user explicitly says 'yes' or 'confirm'.\n\n"
        "If the user asks to see their bookings, use get_my_bookings and present them nicely.\n"
        f"{CONCIERGE_RULES}"
    ))
    return create_react_agent(get_booking_llm(), tools, prompt=prompt)


def create_support_agent():
    """NVIDIA Llama 70B — warm, detailed support responses."""
    tools = [get_booking_detail, get_my_bookings]
    prompt = SystemMessage(content=(
        "You are a warm, empathetic Support Agent concierge. "
        "Help users with general questions, greetings, booking lookups, and any concerns. "
        "When a user says hello, respond warmly and let them know what you can help with. "
        "Always provide thorough, clear, and friendly explanations.\n"
        f"{CONCIERGE_RULES}"
    ))
    return create_react_agent(get_support_llm(), tools, prompt=prompt)


def create_recommender_agent():
    """Google Gemma 27B — creative travel advice with Exa web search."""
    tools = [search_guides, search_car_rentals, search_web_for_travel_advice]
    prompt = SystemMessage(content=(
        "You are an inspiring Recommendation Agent concierge. "
        "Your mission is to provide breathtaking travel advice, suggest immersive itineraries, and inspire wanderlust. "
        "You can search the web for live travel trends, current weather, and up-to-date destination info. "
        "Use your web search tool sparingly (only when you truly need live data). "
        "Write rich, detailed, and exciting recommendations that paint a vivid picture of the destination.\n"
        f"{CONCIERGE_RULES}"
    ))
    return create_react_agent(get_recommender_llm(), tools, prompt=prompt)


def create_trip_organizer_agent():
    """NVIDIA Qwen 32B — structured multi-step trip management."""
    tools = [create_trip, get_my_trips, add_booking_to_trip, remove_booking_from_trip, delete_trip, get_my_bookings]
    prompt = SystemMessage(content=(
        "You are a meticulous Trip Organizer concierge. "
        "Help users create trips, group their bookings into itineraries, and manage their travel plans. "
        "When creating a trip, give it a beautiful name based on the destination. "
        "When adding bookings to a trip, first look up the user's existing bookings to find the right ones.\n"
        f"{CONCIERGE_RULES}"
    ))
    return create_react_agent(get_trip_llm(), tools, prompt=prompt)
