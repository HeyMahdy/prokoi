from src.repositories.workspaces import WorkspacesRepository

class WorkspacesService:
    def __init__(self):
        self.workspacesRepo = WorkspacesRepository()

    async def create_workspace(self, organization_id: int, name: str, user_id: int):
        """Create a new workspace"""
        name = (name or "").strip()
        if not name:
            raise ValueError("Workspace name is required")

        # Check if user has access to organization
        has_access = await self.workspacesRepo.user_has_org_access(user_id, organization_id)
        if not has_access:
            raise Exception("Access denied to organization")

        try:
            workspace_id = await self.workspacesRepo.create_workspace(organization_id, name, user_id)
            if not workspace_id:
                raise Exception("Failed to create workspace")

            workspace = await self.workspacesRepo.get_workspace_by_id(workspace_id)
            if not workspace:
                raise Exception("Workspace not found after creation")

            return workspace
        except Exception as e:
            print(f"Failed to create workspace: {e}")
            raise

    async def get_organization_workspaces(self, organization_id: int, user_id: int):
        """Get all workspaces for an organization"""
        # Check if user has access to organization
        has_access = await self.workspacesRepo.user_has_org_access(user_id, organization_id)
        if not has_access:
            raise Exception("Access denied to organization")

        try:
            workspaces = await self.workspacesRepo.get_organization_workspaces(organization_id)
            return workspaces
        except Exception as e:
            print(f"Failed to get workspaces: {e}")
            raise

    async def assign_team_to_workspace(self, workspace_id: int, team_id: int, user_id: int):
        """Assign team to workspace"""
        # Check if user has access to workspace
        has_access = await self.workspacesRepo.user_has_workspace_access(user_id, workspace_id)
        if not has_access:
            raise Exception("Access denied to workspace")

        # Check if workspace exists
        workspace = await self.workspacesRepo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise Exception("Workspace not found")

        # Check if team exists
        team = await self.workspacesRepo.get_team_by_id(team_id)
        if not team:
            raise Exception("Team not found")

        try:
            assignment_id = await self.workspacesRepo.assign_team_to_workspace(workspace_id, team_id)
            return {"id": assignment_id, "workspace_id": workspace_id, "team_id": team_id}
        except Exception as e:
            if "Duplicate entry" in str(e) or "unique_team_workspace" in str(e):
                raise Exception("Team is already assigned to this workspace")
            print(f"Failed to assign team to workspace: {e}")
            raise

    async def get_workspace_teams(self, workspace_id: int, user_id: int):
        """Get all teams assigned to workspace"""
        # Check if user has access to workspace
        has_access = await self.workspacesRepo.user_has_workspace_access(user_id, workspace_id)
        if not has_access:
            raise Exception("Access denied to workspace")

        # Check if workspace exists
        workspace = await self.workspacesRepo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise Exception("Workspace not found")

        try:
            teams = await self.workspacesRepo.get_workspace_teams(workspace_id)
            return teams
        except Exception as e:
            print(f"Failed to get workspace teams: {e}")
            raise