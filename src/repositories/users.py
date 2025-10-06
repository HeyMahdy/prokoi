from typing import Any
from src.core.database import db
from src.schemas.users import UserSchema


class UserRepository:

    async def save_user(self,user_data:dict[str,Any]) -> None:
        query = """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                """
        params = [user_data['name'],user_data['email'],user_data['password_hash']]
        result = await db.execute_insert(query, params)
        return result

    async  def find_user_by_email(self,email:str):
        query = """
                SELECT * 
                FROM users 
                WHERE email = %s
                """

        params = [email]
        result = await db.execute_query(query, params)
        # Return a single user row or None for consistency with find_user_by_id
        return result[0] if result else None

    async def find_user_by_id(self, user_id: int):
        query = "SELECT * FROM users WHERE id = %s"
        params = [user_id]
        result = await db.execute_query(query, params)
        return result[0] if result else None


    async def update_last_login(self, user_id: int):
      """Update user's last login timestamp"""
      query = "UPDATE users SET last_login_at = NOW() WHERE id = %s"
      params = [user_id]
      await db.execute_query(query, params)


