import hashlib

from src.core.security import get_password_hash
from src.repositories.users import UserRepository
from src.schemas.users import *

class UsersService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def create_user(self, user_data: UserSchema):
        existing_user = await self.user_repo.find_user_by_email(user_data.email)
        if existing_user is not None:
            raise ValueError("User with this email already exists")

        password_hash = get_password_hash(user_data.password_hash)
        user_dict = {
            'full_name': user_data.full_name.strip(),
            'email': user_data.email.strip().lower(),
            'password_hash': password_hash,
            'role': user_data.role.value if user_data.role else 'jobseeker',
            'education_level': user_data.education_level,
            'department': user_data.department,
            'experience_level': user_data.experience_level.value if user_data.experience_level else None,
            'preferred_track': user_data.preferred_track,
            'is_new_to_job_market': user_data.is_new_to_job_market or False,
            'is_active': user_data.is_active if user_data.is_active is not None else True
        }

        user_id = await self.user_repo.save_user(user_dict)
        if not user_id:
            raise Exception("Failed to create user")  # safety check

        user = await self.user_repo.find_user_by_id(user_id)
        return user  # dict with full user info

    async def get_user_by_email(self,email:str):
        try:
            existing_user = await self.user_repo.find_user_by_email(email)
            return existing_user
        except Exception as e:
            raise Exception(f"Failed to fetch user: {str(e)}")