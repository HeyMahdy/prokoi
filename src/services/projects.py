from src.repositories.projects import ProjectsRepository

class ProjectsService:
    def __init__(self):
        self.projectsRepo = ProjectsRepository()

    async def create_project(self, workspace_id: int, name: str, user_id: int, status: str = 'active'):
        """Create a new project"""
        name = (name or "").strip()
        if not name:
            raise ValueError("Project name is required")

        # Check if user has access to workspace
        has_access = await self.projectsRepo.user_has_workspace_access(user_id, workspace_id)
        if not has_access:
            raise Exception("Access denied to workspace")

        # Validate status
        valid_statuses = ['active', 'archived', 'on_hold']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")

        try:
            project_id = await self.projectsRepo.create_project(workspace_id, name, user_id, status)
            if not project_id:
                raise Exception("Failed to create project")

            project = await self.projectsRepo.get_project_by_id(project_id)
            if not project:
                raise Exception("Project not found after creation")

            return project
        except Exception as e:
            print(f"Failed to create project: {e}")
            raise

    async def get_workspace_projects(self, workspace_id: int, user_id: int):
        """Get all projects in workspace"""
        # Check if user has access to workspace
        has_access = await self.projectsRepo.user_has_workspace_access(user_id, workspace_id)
        if not has_access:
            raise Exception("Access denied to workspace")

        try:
            projects = await self.projectsRepo.get_workspace_projects(workspace_id)
            return projects
        except Exception as e:
            print(f"Failed to get workspace projects: {e}")
            raise

    async def update_project_status(self, project_id: int, status: str, user_id: int):
        """Update project status"""
        # Check if user has access to project (through workspace)
        project = await self.projectsRepo.get_project_by_id(project_id)
        if not project:
            raise Exception("Project not found")

        has_access = await self.projectsRepo.user_has_workspace_access(user_id, project['workspace_id'])
        if not has_access:
            raise Exception("Access denied to project")

        # Validate status
        valid_statuses = ['active', 'Inactive', 'On hold','Completed']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")

        try:
            await self.projectsRepo.update_project_status(project_id, status)
            updated_project = await self.projectsRepo.get_project_by_id(project_id)
            return updated_project
        except Exception as e:
            print(f"Failed to update project status: {e}")
            raise

