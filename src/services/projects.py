from src.repositories.projects import ProjectsRepository
from src.repositories.organizations import OrganizationsRepository

class ProjectsService:
    def __init__(self):
        self.projectsRepo = ProjectsRepository()
        self.organizationsRepo = OrganizationsRepository()

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

    async def get_organization_projects(self, organization_id: int, user_id: int):
        """Get all projects in an organization (requires org membership)."""
        # Access check: user must belong to the organization
        has_access = await self.organizationsRepo.user_has_org_access(user_id, organization_id)
        if not has_access:
            raise Exception("Access denied to organization")

        try:
            projects = await self.projectsRepo.get_organization_projects(organization_id)
            return projects
        except Exception as e:
            print(f"Failed to get organization projects: {e}")
            raise

    async def assign_team_to_project(self, project_id: int, team_id: int, user_id: int):
        """Assign team to project"""
        # Check if user has access to project (through workspace)
        project = await self.projectsRepo.get_project_by_id(project_id)
        if not project:
            raise Exception("Project not found")

        has_access = await self.projectsRepo.user_has_workspace_access(user_id, project['workspace_id'])
        if not has_access:
            raise Exception("Access denied to project")

        # Check if team exists
        team = await self.projectsRepo.get_team_by_id(team_id)
        if not team:
            raise Exception("Team not found")

        try:
            assignment_id = await self.projectsRepo.assign_team_to_project(project_id, team_id)
            return {"id": assignment_id, "project_id": project_id, "team_id": team_id}
        except Exception as e:
            if "Duplicate entry" in str(e) or "unique_project_team" in str(e):
                raise Exception("Team is already assigned to this project")
            print(f"Failed to assign team to project: {e}")
            raise

    async def get_project_teams(self, project_id: int, user_id: int):
        """Get all teams assigned to project"""
        # Check if user has access to project (through workspace)
        project = await self.projectsRepo.get_project_by_id(project_id)
        if not project:
            raise Exception("Project not found")

        has_access = await self.projectsRepo.user_has_workspace_access(user_id, project['workspace_id'])
        if not has_access:
            raise Exception("Access denied to project")

        try:
            teams = await self.projectsRepo.get_project_teams(project_id)
            return teams
        except Exception as e:
            print(f"Failed to get project teams: {e}")
            raise

    async def get_project_users(self, project_id: int, user_id: int):
        """Get all users assigned to project"""
        # Check if user has access to project (through workspace)
        project = await self.projectsRepo.get_project_by_id(project_id)
        if not project:
            raise Exception("Project not found")

        has_access = await self.projectsRepo.user_has_workspace_access(user_id, project['workspace_id'])
        if not has_access:
            raise Exception("Access denied to project")

        try:
            users = await self.projectsRepo.get_project_users(project_id)
            return users
        except Exception as e:
            print(f"Failed to get project users: {e}")
            raise

