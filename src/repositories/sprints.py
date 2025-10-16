from src.core.database import db
import aiomysql

class SprintsRepository:
    async def create_sprint(self, project_id: int, name: str, description: str, start_date: str, end_date: str, goal: str, velocity_target: int) -> int:
        """Create a new sprint in a project"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    """INSERT INTO sprints (project_id, name, description, start_date, end_date, goal, velocity_target) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (project_id, name, description, start_date, end_date, goal, velocity_target)
                )
                sprint_id = cur.lastrowid

            await conn.commit()
            return sprint_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_project_sprints(self, project_id: int) -> list[dict]:
        """Get all sprints for a project"""
        query = """
        SELECT s.id, s.project_id, s.name, s.description, s.start_date, s.end_date, 
               s.status, s.goal, s.velocity_target, s.created_at, s.updated_at
        FROM sprints s
        WHERE s.project_id = %s
        ORDER BY s.created_at DESC
        """
        return await db.execute_query(query, (project_id,))

    async def get_sprint_by_id(self, sprint_id: int) -> dict | None:
        """Get sprint by ID"""
        query = """
        SELECT s.id, s.project_id, s.name, s.description, s.start_date, s.end_date, 
               s.status, s.goal, s.velocity_target, s.created_at, s.updated_at
        FROM sprints s
        WHERE s.id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (sprint_id,))
        return rows[0] if rows else None

    async def update_sprint(self, sprint_id: int, name: str, description: str, start_date: str, end_date: str, status: str, goal: str, velocity_target: int) -> bool:
        """Update sprint"""
        query = """
        UPDATE sprints
        SET name = %s, description = %s, start_date = %s, end_date = %s, 
            status = %s, goal = %s, velocity_target = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        await db.execute_query(query, (name, description, start_date, end_date, status, goal, velocity_target, sprint_id))
        return True

    async def delete_sprint(self, sprint_id: int) -> bool:
        """Delete sprint"""
        query = "DELETE FROM sprints WHERE id = %s"
        await db.execute_query(query, (sprint_id,))
        return True

    async def update_sprint_status(self, sprint_id: int, status: str) -> bool:
        """Update sprint status"""
        query = """
        UPDATE sprints
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        await db.execute_query(query, (status, sprint_id))
        return True

    async def user_has_project_access(self, user_id: int, project_id: int) -> bool:
        """Check if user has access to project (through workspace)"""
        query = """
        SELECT 1
        FROM projects p
        JOIN workspaces w ON p.workspace_id = w.id
        JOIN organization_users ou ON w.organization_id = ou.organization_id
        WHERE p.id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (project_id, user_id))
        return len(rows) > 0
