from src.core.database import db
import aiomysql

class SkillsRepository:
    async def get_all_skills(self) -> list[dict]:
        """Get all global skills"""
        query = """
        SELECT id, name, created_at
        FROM skills
        ORDER BY name ASC
        """
        return await db.execute_query(query)

    async def get_skill_by_id(self, skill_id: int) -> dict | None:
        """Get skill by ID"""
        query = """
        SELECT id, name, created_at
        FROM skills
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (skill_id,))
        return rows[0] if rows else None

    async def get_skill_by_name(self, name: str) -> dict | None:
        """Get skill by name"""
        query = """
        SELECT id, name, created_at
        FROM skills
        WHERE name = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (name,))
        return rows[0] if rows else None

    async def add_skill_to_user(self, user_id: int, skill_id: int, proficiency_level: str) -> int:
        """Add skill to user with proficiency level"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    """INSERT INTO user_skills (user_id, skill_id, proficiency_level, created_at)
                       VALUES (%s, %s, %s, CURRENT_TIMESTAMP)""",
                    (user_id, skill_id, proficiency_level)
                )
                user_skill_id = cur.lastrowid

            await conn.commit()
            return user_skill_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def update_user_skill(self, user_id: int, skill_id: int, proficiency_level: str) -> bool:
        """Update user's skill proficiency level"""
        query = """
        UPDATE user_skills
        SET proficiency_level = %s
        WHERE user_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (proficiency_level, user_id, skill_id))
        return True

    async def get_user_skills(self, user_id: int) -> list[dict]:
        """Get all skills for a user with proficiency levels"""
        query = """
        SELECT us.user_id, us.skill_id, us.proficiency_level, us.created_at,
               s.name as skill_name
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (user_id,))

    async def get_user_skill(self, user_id: int, skill_id: int) -> dict | None:
        """Get specific user skill"""
        query = """
        SELECT us.user_id, us.skill_id, us.proficiency_level, us.created_at,
               s.name as skill_name
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id = %s AND us.skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return rows[0] if rows else None

    async def remove_user_skill(self, user_id: int, skill_id: int) -> bool:
        """Remove skill from user"""
        query = """
        DELETE FROM user_skills
        WHERE user_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (user_id, skill_id))
        return True

    async def user_has_skill(self, user_id: int, skill_id: int) -> bool:
        """Check if user has a specific skill"""
        query = """
        SELECT 1
        FROM user_skills
        WHERE user_id = %s AND skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return len(rows) > 0

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
        SELECT 1
        FROM organization_users ou
        WHERE ou.organization_id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (organization_id, user_id))
        return len(rows) > 0

    async def get_user_by_id(self, user_id: int) -> dict | None:
        """Get user by ID"""
        query = """
        SELECT id, name, email
        FROM users
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id,))
        return rows[0] if rows else None
