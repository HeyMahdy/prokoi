from src.core.database import db


class WorkspacesRepository:
    async def create_workspace(self, organization_id: int, name: str, user_id: int) -> int:
        """Create a new workspace in an organization"""
        async for conn in db.connection():
            async with conn.transaction():
                workspace_record = await conn.fetchrow(
                    "INSERT INTO workspaces (name, user_id, organization_id) VALUES ($1, $2, $3) RETURNING id",
                    name, user_id, organization_id
                )
                workspace_id = workspace_record['id']
                return workspace_id
        # Fallback return in case the async for loop doesn't execute
        raise Exception("Failed to create workspace")

    async def get_organization_workspaces(self, organization_id: int) -> list[dict]:
        """Get all workspaces for an organization"""
        query = """
        SELECT w.id, w.name, w.user_id, w.organization_id, w.created_at, w.updated_at
        FROM workspaces w
        WHERE w.organization_id = $1
        ORDER BY w.created_at DESC
        """
        return await db.execute_query(query, (organization_id,))

    async def get_workspace_by_id(self, workspace_id: int) -> dict | None:
        """Get workspace by ID"""
        query = """
        SELECT w.id, w.name, w.user_id, w.organization_id, w.created_at, w.updated_at,
               u.name as creator_name, u.email as creator_email
        FROM workspaces w
        JOIN users u ON w.user_id = u.id
        WHERE w.id = $1
        LIMIT 1
        """
        rows = await db.execute_query(query, (workspace_id,))
        print(rows[0] if rows else None)
        return rows[0] if rows else None

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
        SELECT 1
        FROM organization_users ou
        WHERE ou.organization_id = $1 AND ou.user_id = $2
        LIMIT 1
        """
        rows = await db.execute_query(query, (organization_id, user_id))
        return len(rows) > 0

    async def user_has_workspace_access(self, user_id: int, workspace_id: int) -> bool:
        """Check if user has access to workspace"""
        query = """
        SELECT 1
        FROM workspaces w
        JOIN organization_users ou ON w.organization_id = ou.organization_id
        WHERE w.id = $1 AND ou.user_id = $2
        LIMIT 1
        """
        rows = await db.execute_query(query, (workspace_id, user_id))
        return len(rows) > 0

    async def get_team_by_id(self, team_id: int) -> dict | None:
        """Get team by ID"""
        query = """
        SELECT t.id, t.name, t.organization_id
        FROM teams t
        WHERE t.id = $1
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id,))
        return rows[0] if rows else None

    async def assign_team_to_workspace(self, workspace_id: int, team_id: int) -> int:
        """Assign team to workspace"""
        async for conn in db.connection():
            async with conn.transaction():
                assignment_record = await conn.fetchrow(
                    "INSERT INTO team_workspaces (team_id, workspace_id) VALUES ($1, $2) RETURNING id",
                    team_id, workspace_id
                )
                assignment_id = assignment_record['id']
                return assignment_id
        # Fallback return in case the async for loop doesn't execute
        raise Exception("Failed to assign team to workspace")

    async def get_workspace_teams(self, workspace_id: int):
        """Get all teams assigned to workspace"""
        query = """
        SELECT tw.id, tw.team_id, tw.workspace_id, tw.created_at, tw.updated_at,
               t.name as team_name, t.organization_id
        FROM team_workspaces tw
        JOIN teams t ON tw.team_id = t.id
        WHERE tw.workspace_id = $1
        ORDER BY tw.created_at DESC
        """
        try:
            result = await db.execute_query(query, (workspace_id,))
            print(result)
            return result
        except Exception as e:
            print(e)
            raise