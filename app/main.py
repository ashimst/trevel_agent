import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import close_db, get_database
from app.routers import auth, flights, buses, hotels, activities, guides, car_rentals, bookings, trips, payments, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Travels & Tourism API...")
    yield
    # Shutdown
    logger.info("Shutting down Travels & Tourism API...")
    await close_db()


app = FastAPI(
    title="Travels & Tourism API",
    description=(
        "Book flights, buses, hotels, activities, guides, and car rentals. "
        "Optionally bundle bookings into trip packages. Powered by Stripe."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(buses.router)
app.include_router(hotels.router)
app.include_router(activities.router)
app.include_router(guides.router)
app.include_router(car_rentals.router)
app.include_router(bookings.router)
app.include_router(trips.router)
app.include_router(payments.router)
app.include_router(chat.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Travels & Tourism API is running"}


@app.get("/health", tags=["Health"])
async def health():
    db_status = "unknown"
    try:
        db = get_database()
        # Ping database to check connection
        await db.command("ping")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Health check failed for database: {e}")
        db_status = f"unhealthy: {str(e)}"
        
    return {
        "status": "ok" if "unhealthy" not in db_status else "error",
        "database": db_status
    }
