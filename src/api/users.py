from fastapi import APIRouter, HTTPException, status

from src.schemas.auth import Token
from src.schemas.users import *
from src.services.auth import AuthService
from src.services.users import UsersService
from src.schemas.users import UserLogin

router = APIRouter(
    prefix="/users",       # ✅ every route starts with /users
    tags=["Users"]         # ✅ groups routes in Swagger UI
)

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserSchema):
    userservice = UsersService()
    try:
        return await userservice.create_user(user_data)
    except ValueError as ve:
        # Known errors like duplicate email
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        # Unknown/internal errors
        raise HTTPException(
            status_code=500,
            detail="Something went wrong with creating user"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and get access token"""
    auth_service = AuthService()
    return await auth_service.login(user_credentials)

