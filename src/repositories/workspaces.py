from src.core.database import db
import aiomysql

class WorkspacesRepository:
    async def create_workspace(self, organization_id: int, name: str, user_id: int, team_id: int = None) -> int:
        """Create a new workspace in an organization"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "INSERT INTO workspaces (name, user_id, team_id, organization_id) VALUES (%s, %s, %s, %s)",
                    (name, user_id, team_id, organization_id)
                )
                workspace_id = cur.lastrowid

            await conn.commit()
            return workspace_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_organization_workspaces(self, organization_id: int) -> list[dict]:
        """Get all workspaces for an organization"""
        query = """
        SELECT w.id, w.name, w.user_id, w.team_id, w.organization_id, w.created_at, w.updated_at,
               u.name as creator_name, u.email as creator_email,
               t.name as team_name
        FROM workspaces w
        JOIN users u ON w.user_id = u.id
        LEFT JOIN teams t ON w.team_id = t.id
        WHERE w.organization_id = %s
        ORDER BY w.created_at DESC
        """
        return await db.execute_query(query, (organization_id,))

    async def get_workspace_by_id(self, workspace_id: int) -> dict | None:
        """Get workspace by ID"""
        query = """
        SELECT w.id, w.name, w.user_id, w.team_id, w.organization_id, w.created_at, w.updated_at,
               u.name as creator_name, u.email as creator_email,
               t.name as team_name
        FROM workspaces w
        JOIN users u ON w.user_id = u.id
        LEFT JOIN teams t ON w.team_id = t.id
        WHERE w.id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (workspace_id,))
        return rows[0] if rows else None

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