from src.core.database import db
import aiomysql

class IssueSkillsRepository:
    
    async def add_skill_to_issue(self, issue_id: int, skill_id: int, required_level: str) -> int:
        """Add skill requirement to issue"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    """INSERT INTO issue_skill_requirements (issue_id, skill_id, required_level)
                       VALUES (%s, %s, %s)""",
                    (issue_id, skill_id, required_level)
                )
                requirement_id = cur.lastrowid

            await conn.commit()
            return requirement_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def update_issue_skill_requirement(self, issue_id: int, skill_id: int, required_level: str) -> bool:
        """Update skill requirement level for an issue"""
        query = """
        UPDATE issue_skill_requirements 
        SET required_level = %s
        WHERE issue_id = %s AND skill_id = %s
        """
        try:
            await db.execute_query(query, (required_level, issue_id, skill_id))
            return True
        except Exception as e:
            print(f"Failed to update issue skill requirement: {e}")
            return False

    async def remove_skill_from_issue(self, issue_id: int, skill_id: int) -> bool:
        """Remove skill requirement from issue"""
        query = """
        DELETE FROM issue_skill_requirements 
        WHERE issue_id = %s AND skill_id = %s
        """
        try:
            await db.execute_query(query, (issue_id, skill_id))
            return True
        except Exception as e:
            print(f"Failed to remove skill from issue: {e}")
            return False

    async def get_issue_skills(self, issue_id: int) -> list[dict]:
        """Get all skill requirements for an issue"""
        query = """
        SELECT isr.issue_id, isr.skill_id, s.name as skill_name, 
               isr.required_level, isr.created_at
        FROM issue_skill_requirements isr
        JOIN skills s ON isr.skill_id = s.id
        WHERE isr.issue_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (issue_id,))

    async def get_issue_skill_requirement(self, issue_id: int, skill_id: int) -> dict | None:
        """Get specific skill requirement for an issue"""
        query = """
        SELECT isr.issue_id, isr.skill_id, s.name as skill_name, 
               isr.required_level, isr.created_at
        FROM issue_skill_requirements isr
        JOIN skills s ON isr.skill_id = s.id
        WHERE isr.issue_id = %s AND isr.skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (issue_id, skill_id))
        return rows[0] if rows else None

    async def issue_has_skill_requirement(self, issue_id: int, skill_id: int) -> bool:
        """Check if issue has a specific skill requirement"""
        query = """
        SELECT 1
        FROM issue_skill_requirements
        WHERE issue_id = %s AND skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (issue_id, skill_id))
        return len(rows) > 0

    async def get_skill_match_analysis(self, issue_id: int, user_id: int) -> list[dict]:
        """Get skill match analysis for a user and issue"""
        query = """
        SELECT 
            isr.skill_id,
            s.name as skill_name,
            isr.required_level,
            us.proficiency_level as user_level,
            CASE 
                WHEN us.proficiency_level IS NULL THEN 'missing_skill'
                WHEN us.proficiency_level = 'expert' AND isr.required_level IN ('beginner', 'intermediate', 'advanced') THEN 'overqualified'
                WHEN us.proficiency_level = 'advanced' AND isr.required_level IN ('beginner', 'intermediate') THEN 'overqualified'
                WHEN us.proficiency_level = 'intermediate' AND isr.required_level = 'beginner' THEN 'overqualified'
                WHEN us.proficiency_level = isr.required_level THEN 'perfect_match'
                WHEN (us.proficiency_level = 'beginner' AND isr.required_level = 'intermediate') OR
                     (us.proficiency_level = 'beginner' AND isr.required_level = 'advanced') OR
                     (us.proficiency_level = 'beginner' AND isr.required_level = 'expert') OR
                     (us.proficiency_level = 'intermediate' AND isr.required_level = 'advanced') OR
                     (us.proficiency_level = 'intermediate' AND isr.required_level = 'expert') OR
                     (us.proficiency_level = 'advanced' AND isr.required_level = 'expert') THEN 'underqualified'
                ELSE 'perfect_match'
            END as gap
        FROM issue_skill_requirements isr
        JOIN skills s ON isr.skill_id = s.id
        LEFT JOIN user_skills us ON isr.skill_id = us.skill_id AND us.user_id = %s
        WHERE isr.issue_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (user_id, issue_id))

    async def user_has_project_access(self, user_id: int, project_id: int) -> bool:
        """Check if user has access to project through team membership"""
        query = """
        SELECT 1
        FROM project_teams pt
        JOIN user_team ut ON pt.team_id = ut.team_id
        WHERE pt.project_id = %s AND ut.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (project_id, user_id))
        return len(rows) > 0

    async def get_issue_by_id(self, issue_id: int) -> dict | None:
        """Get issue by ID"""
        query = """
        SELECT id, project_id, title, description, status, priority
        FROM issues
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (issue_id,))
        return rows[0] if rows else None

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
