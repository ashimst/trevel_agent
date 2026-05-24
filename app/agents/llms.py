from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from app.core.config import settings

# ── Supervisor ─────────────────────────────────────────────
# Groq Llama 3.3 70B — single-shot structured output (not a ReAct loop)
def get_supervisor_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=settings.GROQ_API_KEY,
        temperature=0
    )

# ── Travel Planner ─────────────────────────────────────────
# Groq Qwen 3 32B — strong tool calling, 60 RPM
def get_planner_llm():
    return ChatGroq(
        model="qwen/qwen3-32b",
        api_key=settings.GROQ_API_KEY,
        temperature=0
    )

# ── Booking Agent ──────────────────────────────────────────
# Groq Qwen 3 32B — strong reasoning for multi-step booking
def get_booking_llm():
    return ChatGroq(
        model="qwen/qwen3-32b",
        api_key=settings.GROQ_API_KEY,
        temperature=0
    )

# ── Support Agent ──────────────────────────────────────────
# NVIDIA Llama 3.3 70B — warm, verbose responses (light usage)
def get_support_llm():
    return ChatNVIDIA(
        model="meta/llama-3.3-70b-instruct",
        api_key=settings.NVIDIA_API_KEY
    )

# ── Recommender ────────────────────────────────────────────
# NVIDIA Llama 3.3 70B — creative advice + Exa web search (light usage)
def get_recommender_llm():
    return ChatNVIDIA(
        model="meta/llama-3.3-70b-instruct",
        api_key=settings.NVIDIA_API_KEY
    )

# ── Trip Organizer ─────────────────────────────────────────
# Groq Llama 4 Scout — newer MoE model for structured trip management
def get_trip_llm():
    return ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=settings.GROQ_API_KEY,
        temperature=0
    )
