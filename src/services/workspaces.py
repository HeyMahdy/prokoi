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