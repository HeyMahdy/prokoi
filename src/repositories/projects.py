from src.core.database import db
import aiomysql

class ProjectsRepository:
    async def create_project(self, workspace_id: int, name: str, created_by: int, status: str = 'active') -> int:
        """Create a new project in a workspace"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "INSERT INTO projects (name, workspace_id, created_by, status) VALUES (%s, %s, %s, %s)",
                    (name, workspace_id, created_by, status)
                )
                project_id = cur.lastrowid

            await conn.commit()
            return project_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_workspace_projects(self, workspace_id: int) -> list[dict]:
        """Get all projects in a workspace"""
        query = """
        SELECT p.id, p.name, p.workspace_id, p.created_by, p.status, p.created_at, p.updated_at,
               u.name as creator_name, u.email as creator_email,
               w.name as workspace_name, w.organization_id
        FROM projects p
        JOIN users u ON p.created_by = u.id
        JOIN workspaces w ON p.workspace_id = w.id
        WHERE p.workspace_id = %s
        ORDER BY p.created_at DESC
        """
        return await db.execute_query(query, (workspace_id,))

    async def get_project_by_id(self, project_id: int) -> dict | None:
        """Get project by ID"""
        query = """
        SELECT p.id, p.name, p.workspace_id, p.created_by, p.status, p.created_at, p.updated_at,
               u.name as creator_name, u.email as creator_email,
               w.name as workspace_name, w.organization_id
        FROM projects p
        JOIN users u ON p.created_by = u.id
        JOIN workspaces w ON p.workspace_id = w.id
        WHERE p.id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (project_id,))
        return rows[0] if rows else None

    async def get_organization_projects(self, organization_id: int) -> list[dict]:
        """Get all projects that belong to an organization (via workspaces)."""
        query = """
        SELECT p.id,
               p.name,
               p.workspace_id,
               p.created_by,
               p.status,
               p.created_at,
               p.updated_at,
               u.name  AS creator_name,
               u.email AS creator_email,
               w.name  AS workspace_name,
               w.organization_id
        FROM projects p
                 JOIN users u ON p.created_by = u.id
                 JOIN workspaces w ON p.workspace_id = w.id
        WHERE w.organization_id = %s
        ORDER BY p.created_at DESC
        """
        return await db.execute_query(query, (organization_id,))

    async def user_has_workspace_access(self, user_id: int, workspace_id: int) -> bool:
        """Check if user has access to workspace (through organization)"""
        query = """
        SELECT 1
        FROM workspaces w
        JOIN organization_users ou ON w.organization_id = ou.organization_id
        WHERE w.id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (workspace_id, user_id))
        return len(rows) > 0

    async def update_project_status(self, project_id: int, status: str) -> bool:
        """Update project status"""
        query = """
        UPDATE projects
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        await db.execute_query(query, (status, project_id))
        return True

    async def delete_project(self, project_id: int) -> bool:
        """Delete project"""
        query = "DELETE FROM projects WHERE id = %s"
        await db.execute_query(query, (project_id,))
        return True
    async def get_team_by_id(self, team_id: int) -> dict | None:
        """Get team by ID"""
        query = """
        SELECT t.id, t.name, t.organization_id
        FROM teams t
        WHERE t.id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id,))
        return rows[0] if rows else None

    async def assign_team_to_project(self, project_id: int, team_id: int) -> int:
        """Assign team to project"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Step 1: insert into project_teams
                await cur.execute(
                    "INSERT INTO project_teams (project_id, team_id) VALUES (%s, %s)",
                    (project_id, team_id)
                )
                project_teams_id = cur.lastrowid

            # Step 2: insert all team users into project_users
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    """
                    INSERT INTO project_users (project_id, user_id)
                    SELECT %s, ut.user_id
                    FROM user_team ut
                    WHERE ut.team_id = %s;
                    """,
                    (team_id, project_id)  # <-- Correct order: matches %s placeholders
                )
                project_users = cur.lastrowid

            await conn.commit()
            return project_teams_id

        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_project_teams(self, project_id: int) -> list[dict]:
        """Get all teams assigned to project"""
        query = """
        SELECT pt.id, pt.project_id, pt.team_id, pt.created_at, pt.updated_at,
               t.name as team_name, t.organization_id
        FROM project_teams pt
        JOIN teams t ON pt.team_id = t.id
        WHERE pt.project_id = %s
        ORDER BY pt.created_at DESC
        """
        return await db.execute_query(query, (project_id,))

    async def get_project_users(self, project_id: int) -> list[dict]:
        """Get all users assigned to project"""
        query = """
        SELECT DISTINCT pu.id, pu.project_id, pu.user_id, pu.created_at, pu.updated_at,
               u.name as user_name, u.email as user_email
        FROM project_users pu
        JOIN users u ON pu.user_id = u.id
        WHERE pu.project_id = %s
        ORDER BY u.name ASC
        """
        try:
            rows = await db.execute_query(query, (project_id,))
            return rows
        except Exception as e:
            print("error", e)
            raise

