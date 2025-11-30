from datetime import datetime
from fastapi import HTTPException, status
from src.core.security import verify_password, get_password_hash, create_access_token
from src.repositories.users import UserRepository
from src.schemas.users import UserSchema, UserResponse , UserLogin


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def authenticate_user(self, email: str, password: str):
        """Authenticate user with email and password"""
        user = await self.user_repo.find_user_by_email(email) 
        if not user:
            return False
        if not verify_password(password, user['password_hash']):
            return False
        return user

    async def login(self, user_credentials: UserLogin):
        """Login user and return access token"""
        user = await self.authenticate_user(user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last login time
        await self.user_repo.update_last_login(user["id"])


        access_token = create_access_token(data={"sub": user['email']})
        return {"access_token": access_token, "token_type": "bearer"}


    async def get_current_user(self, token: str):
        """Get current user from JWT token"""
        from src.core.security import verify_token

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = verify_token(token)
        if payload is None:
            raise credentials_exception

        email: str = payload["sub"]
        if email is None:
            raise credentials_exception

        user = await self.user_repo.find_user_by_email(email)
        if user is None:
            raise credentials_exception

        return UserResponse(**user)