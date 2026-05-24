from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.guide import GuideCreate, GuideResponse, GuideBookRequest
from app.schemas.booking import BookingResponse
from app.services.booking_service import create_booking
from app.models.booking import ServiceType
from app.routers._helpers import list_collection, get_one

router = APIRouter(prefix="/guides", tags=["Guides"])


@router.get("/", response_model=List[GuideResponse])
async def list_guides(
    skip: int = 0, limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    return await list_collection(db, "guides", skip, limit)


@router.get("/{guide_id}", response_model=GuideResponse)
async def get_guide(guide_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await get_one(db, "guides", guide_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found")
    return doc


@router.post("/", response_model=GuideResponse, status_code=201)
async def create_guide(
    payload: GuideCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    doc = payload.model_dump()
    from datetime import datetime
    doc["created_at"] = datetime.utcnow()
    result = await db["guides"].insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


@router.post("/{guide_id}/book", response_model=BookingResponse, status_code=201)
async def book_guide(
    guide_id: str,
    payload: GuideBookRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),
):
    guide = await get_one(db, "guides", guide_id)
    if not guide:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found")

    # Validate booking range falls within availability
    from datetime import timezone
    def _as_dt(v):
        if isinstance(v, str):
            from datetime import datetime
            return datetime.fromisoformat(v)
        return v

    avail_from = _as_dt(guide["available_from"])
    avail_to = _as_dt(guide["available_to"])
    book_from = payload.booking_from.replace(tzinfo=None)
    book_to = payload.booking_to.replace(tzinfo=None)

    if book_from < avail_from or book_to > avail_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Guide available {avail_from.date()} – {avail_to.date()} only",
        )

    days = max(1, (book_to - book_from).days)
    amount = guide["daily_rate"] * days
    notes = f"Booking: {book_from.date()} to {book_to.date()}. {payload.notes or ''}".strip()

    return await create_booking(
        db=db,
        user_id=current_user["_id"],
        service_type=ServiceType.guide,
        service_id=guide_id,
        amount=amount,
        notes=notes,
    )
