from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, login_user
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: UserRegisterRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await register_user(payload, db)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await login_user(payload, db)


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        email=current_user["email"],
        full_name=current_user["full_name"],
    )
