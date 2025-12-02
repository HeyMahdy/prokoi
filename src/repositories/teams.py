from src.core.database import db


class TeamsRepository:
    async def create_team(self, organization_id: int, name: str) -> int:
        """Create a new team in an organization"""
        async for conn in db.connection():
            async with conn.transaction():
                team_record = await conn.fetchrow(
                    "INSERT INTO teams (organization_id, name) VALUES ($1, $2) RETURNING id",
                    organization_id, name
                )
                team_id = team_record['id']
                return team_id
        # Fallback return in case the async for loop doesn't execute
        raise Exception("Failed to create team")

    async def get_organization_teams(self, organization_id: int) -> list[dict]:
        """Get all teams for an organization"""
        query = """
        SELECT id, organization_id, name
        FROM teams
        WHERE organization_id = $1
        ORDER BY id DESC
        """
        return await db.execute_query(query, (organization_id,))

    async def get_team_by_id(self, team_id: int) -> dict | None:
        """Get team by ID"""
        query = """
        SELECT id, organization_id, name
        FROM teams
        WHERE id = $1
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id,))
        return rows[0] if rows else None

    async def update_team(self, team_id: int, name: str) -> bool:
        """Update team name"""
        query = """
        UPDATE teams
        SET name = $1
        WHERE id = $2
        """
        result = await db.execute_query(query, (name, team_id))
        return True  # Assuming success if no exception

    async def delete_team(self, team_id: int) -> bool:
        """Delete team"""
        query = "DELETE FROM teams WHERE id = $1"
        await db.execute_query(query, (team_id,))
        return True  # Assuming success if no exception

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
        SELECT 1
        FROM organizations o
        JOIN organization_users ou ON o.id = ou.organization_id
        WHERE o.id = $1 AND ou.user_id = $2
        LIMIT 1
        """
        rows = await db.execute_query(query, (organization_id, user_id))
        print(f"Checking access: user_id={user_id}, org_id={organization_id}, rows={len(rows)}")
        return len(rows) > 0


    async def add_team_to_workspace(self, team_id: int, workspace_id: int) :
        """Add team to workspace"""
        query = """
        INSERT INTO team_workspaces (team_id, workspace_id) VALUES ($1, $2)
        """
        result = await db.execute_insert(query, (team_id, workspace_id))
        return result

    async def list_workspace_teams(self,workspace_id: int) :
        """List all teams for a project"""
        query = """
        SELECT * FROM team_workspaces
        WHERE workspace_id = $1
        """
        rows = await db.execute_query(query, (workspace_id,))
        return rows

    async def add_team_to_projects(self, team_id: int, project_id: int) :
        """Add team to workspace"""
        query = """
        INSERT INTO project_teams(team_id,project_id)
        VALUES ($1, $2) 
        """
        result = await db.execute_query(query, (team_id, project_id))
        return result

    async def list_project_teams(self,project_id: int) :
        """List all teams for a project"""
        query = """
        
        SELECT * FROM project_teams
        WHERE project_id = $1
        """
        rows = await db.execute_query(query, (project_id,))
        return rows