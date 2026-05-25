"""
Auth service: register and login logic.
Users are stored with str _id = email (acts as unique key).
"""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse


async def register_user(payload: UserRegisterRequest, db: AsyncIOMotorDatabase) -> TokenResponse:
    existing = await db["users"].find_one({"_id": payload.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    doc = {
        "_id": payload.email,
        "email": payload.email,
        "full_name": payload.full_name,
        "hashed_password": hash_password(payload.password),
        "created_at": datetime.now(timezone.utc),
    }
    await db["users"].insert_one(doc)
    token = create_access_token({"sub": payload.email})
    return TokenResponse(access_token=token)


async def login_user(payload: UserLoginRequest, db: AsyncIOMotorDatabase) -> TokenResponse:
    user = await db["users"].find_one({"_id": payload.email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token({"sub": payload.email})
    return TokenResponse(access_token=token)
