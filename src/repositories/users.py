from typing import Any
from src.core.database import db
from src.schemas.users import UserSchema
import uuid


class UserRepository:

    async def save_user(self,user_data:dict[str,Any]) -> str:
        # Generate a UUID for the id field
        user_id = str(uuid.uuid4())
        
        query = """
                INSERT INTO users (id, full_name, email, password_hash, role, education_level, department, experience_level, preferred_track, is_new_to_job_market, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        params = [
            user_id,
            user_data['full_name'],
            user_data['email'],
            user_data['password_hash'],
            user_data['role'],
            user_data['education_level'],
            user_data['department'],
            user_data['experience_level'],
            user_data['preferred_track'],
            user_data['is_new_to_job_market'],
            user_data['is_active']
        ]
        result = await db.execute_insert(query, params)
        return user_id

    async  def find_user_by_email(self,email:str):
        query = """
                SELECT id, full_name, email, password_hash, role, education_level, department, experience_level, preferred_track, is_new_to_job_market, is_active, last_login, created_at, updated_at
                FROM users 
                WHERE email = %s
                """

        params = [email,]
        result = await db.execute_query(query, params)
        # Return a single user row or None for consistency with find_user_by_id
        return result[0] if result else None

    async def find_user_by_id(self, user_id: str):
        query = "SELECT id, full_name, email, password_hash, role, education_level, department, experience_level, preferred_track, is_new_to_job_market, is_active, last_login, created_at, updated_at FROM users WHERE id = %s"
        params = [user_id]
        result = await db.execute_query(query, params)
        return result[0] if result else None


    async def update_last_login(self, user_id: str):
      """Update user's last login timestamp"""
      query = "UPDATE users SET last_login = NOW() WHERE id = %s"
      params = [user_id]
      await db.execute_query(query, params)