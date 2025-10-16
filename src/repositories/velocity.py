from src.core.database import db
import aiomysql

class VelocityRepository:
    async def get_team_velocity_history(self, team_id: int) -> list[dict]:
        """Get team velocity history across all projects"""
        query = """
        SELECT tv.team_id, tv.project_id, tv.avg_hours_per_point, tv.created_at, tv.updated_at,
               t.name as team_name, p.name as project_name
        FROM team_velocity tv
        JOIN teams t ON tv.team_id = t.id
        JOIN projects p ON tv.project_id = p.id
        WHERE tv.team_id = %s
        ORDER BY tv.updated_at DESC
        """
        return await db.execute_query(query, (team_id,))

    async def get_team_project_velocity(self, team_id: int, project_id: int) -> dict | None:
        """Get team velocity for specific project"""
        query = """
        SELECT tv.team_id, tv.project_id, tv.avg_hours_per_point, tv.created_at, tv.updated_at,
               t.name as team_name, p.name as project_name
        FROM team_velocity tv
        JOIN teams t ON tv.team_id = t.id
        JOIN projects p ON tv.project_id = p.id
        WHERE tv.team_id = %s AND tv.project_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id, project_id))
        return rows[0] if rows else None

    async def upsert_team_velocity(self, team_id: int, project_id: int, avg_hours_per_point: float) -> bool:
        """Insert or update team velocity for a project"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Use INSERT ... ON DUPLICATE KEY UPDATE for upsert
                await cur.execute(
                    """INSERT INTO team_velocity (team_id, project_id, avg_hours_per_point, created_at, updated_at)
                       VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                       ON DUPLICATE KEY UPDATE
                       avg_hours_per_point = VALUES(avg_hours_per_point),
                       updated_at = CURRENT_TIMESTAMP""",
                    (team_id, project_id, avg_hours_per_point)
                )

            await conn.commit()
            return True
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def user_has_team_access(self, user_id: int, team_id: int) -> bool:
        """Check if user has access to team"""
        query = """
        SELECT 1
        FROM user_team ut
        JOIN teams t ON ut.team_id = t.id
        JOIN organization_users ou ON t.organization_id = ou.organization_id
        WHERE ut.team_id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id, user_id))
        return len(rows) > 0

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

    async def team_has_project_access(self, team_id: int, project_id: int) -> bool:
        """Check if team has access to project"""
        query = """
        SELECT 1
        FROM project_teams pt
        WHERE pt.team_id = %s AND pt.project_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id, project_id))
        return len(rows) > 0
