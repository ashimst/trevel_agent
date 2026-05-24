import os
if "SSL_CERT_FILE" in os.environ and not os.path.exists(os.environ["SSL_CERT_FILE"]):
    del os.environ["SSL_CERT_FILE"]

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import close_db
from app.routers import auth, flights, buses, hotels, activities, guides, car_rentals, bookings, trips, payments, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — nothing special needed for Motor (lazy connect)
    yield
    # Shutdown — close Motor client cleanly
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
