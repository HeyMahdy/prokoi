from src.core.database import db
import aiomysql
import uuid
from typing import Optional

class SkillsRepository:
    async def get_all_skills(self) :
        """Get all skills"""
        query = """
        SELECT id, name, category, description, created_at
        FROM skills
        ORDER BY name ASC
        """
        return await db.execute_query(query)

    async def get_skill_by_id(self, skill_id: str) -> dict | None:
        """Get skill by ID"""
        query = """
        SELECT id, name, category, description, created_at
        FROM skills
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (skill_id,))
        return rows[0] if rows else None

    async def get_skill_by_name(self, name: str) -> dict | None:
        """Get skill by name"""
        query = """
        SELECT id, name, category, description, created_at
        FROM skills
        WHERE name = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (name,))
        return rows[0] if rows else None

    async def create_skill(self, name: str, category: str, description: Optional[str] = None) -> str:
        """Create a new skill"""
        skill_id = str(uuid.uuid4())
        query = """
        INSERT INTO skills (id, name, category, description)
        VALUES (%s, %s, %s, %s)
        """
        await db.execute_insert(query, (skill_id, name, category, description))
        return skill_id

    async def get_user_skills(self, user_id: str) -> list[dict]:
        """Get all skills for a user"""
        query = """
        SELECT us.id, us.user_id, us.skill_id, s.name as skill_name, 
               us.proficiency as proficiency_level, us.verified, 
               us.verification_score, us.verification_date, us.created_at
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (user_id,))

    async def get_user_skill(self, user_id: str, skill_id: str) -> dict | None:
        """Get specific user skill"""
        query = """
        SELECT us.id, us.user_id, us.skill_id, s.name as skill_name,
               us.proficiency as proficiency_level, us.verified,
               us.verification_score, us.verification_date, us.created_at
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id = %s AND us.skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return rows[0] if rows else None

    async def add_skill_to_user(self, user_id: str, skill_id: str, proficiency: str) -> str:
        """Add skill to user"""
        user_skill_id = str(uuid.uuid4())
        query = """
        INSERT INTO user_skills (id, user_id, skill_id, proficiency)
        VALUES (%s, %s, %s, %s)
        """
        await db.execute_insert(query, (user_skill_id, user_id, skill_id, proficiency))
        return user_skill_id

    async def update_user_skill(self, user_id: str, skill_id: str, proficiency: str) -> bool:
        """Update user skill proficiency"""
        query = """
        UPDATE user_skills 
        SET proficiency = %s
        WHERE user_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (proficiency, user_id, skill_id))
        return True

    async def remove_user_skill(self, user_id: str, skill_id: str) -> bool:
        """Remove skill from user"""
        query = """
        DELETE FROM user_skills
        WHERE user_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (user_id, skill_id))
        return True

    async def user_has_skill(self, user_id: str, skill_id: str) -> bool:
        """Check if user has a specific skill"""
        query = """
        SELECT 1
        FROM user_skills
        WHERE user_id = %s AND skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return len(rows) > 0

    async def get_user_experiences(self, user_id: str) -> list[dict]:
        """Get all experiences for a user"""
        query = """
        SELECT id, user_id, title, description, type, company, 
               start_date, end_date, is_current, created_at, updated_at
        FROM user_experiences
        WHERE user_id = %s
        ORDER BY created_at DESC
        """
        return await db.execute_query(query, (user_id,))

    async def get_experience_by_id(self, experience_id: str) -> dict | None:
        """Get experience by ID"""
        query = """
        SELECT id, user_id, title, description, type, company,
               start_date, end_date, is_current, created_at, updated_at
        FROM user_experiences
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (experience_id,))
        return rows[0] if rows else None

    async def create_experience(self, user_id: str, title: str, description: Optional[str] = None,
                              type: Optional[str] = None, company: Optional[str] = None, 
                              start_date: Optional[str] = None, end_date: Optional[str] = None,
                              is_current: bool = False) -> str:
        """Create a new user experience"""
        experience_id = str(uuid.uuid4())
        query = """
        INSERT INTO user_experiences (id, user_id, title, description, type, company, 
                                    start_date, end_date, is_current)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await db.execute_insert(query, (experience_id, user_id, title, description,
                                       type, company, start_date, end_date, is_current))
        return experience_id

    async def update_experience(self, experience_id: str, title: Optional[str] = None,
                              description: Optional[str] = None, type: Optional[str] = None, 
                              company: Optional[str] = None, start_date: Optional[str] = None, 
                              end_date: Optional[str] = None, is_current: Optional[bool] = None) -> bool:
        """Update user experience"""
        # Build dynamic query based on provided fields
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if type is not None:
            updates.append("type = %s")
            params.append(type)
        if company is not None:
            updates.append("company = %s")
            params.append(company)
        if start_date is not None:
            updates.append("start_date = %s")
            params.append(start_date)
        if end_date is not None:
            updates.append("end_date = %s")
            params.append(end_date)
        if is_current is not None:
            updates.append("is_current = %s")
            params.append(is_current)
            
        if not updates:
            return False
            
        query = f"UPDATE user_experiences SET {', '.join(updates)} WHERE id = %s"
        params.append(experience_id)
        
        await db.execute_query(query, params)
        return True

    async def delete_experience(self, experience_id: str) -> bool:
        """Delete user experience"""
        query = """
        DELETE FROM user_experiences
        WHERE id = %s
        """
        await db.execute_query(query, (experience_id,))
        return True