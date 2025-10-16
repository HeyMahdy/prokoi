from src.repositories.sprints import SprintsRepository
from src.schemas.sprints import SprintCreate, SprintUpdate, SprintStatus
from src.schemas.sprint_planning import IssueAddToSprint, SprintBacklogReorder

class SprintsService:
    def __init__(self):
        self.sprintsRepo = SprintsRepository()

    async def create_sprint(self, project_id: int, sprint_data: SprintCreate, user_id: int):
        """Create a new sprint"""
        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, project_id)
        if not has_access:
            raise Exception("Access denied to project")

        # Validate dates
        if sprint_data.start_date >= sprint_data.end_date:
            raise ValueError("Start date must be before end date")

        try:
            sprint_id = await self.sprintsRepo.create_sprint(
                project_id=project_id,
                name=sprint_data.name,
                description=sprint_data.description,
                start_date=str(sprint_data.start_date),
                end_date=str(sprint_data.end_date),
                goal=sprint_data.goal,
                velocity_target=sprint_data.velocity_target
            )
            if not sprint_id:
                raise Exception("Failed to create sprint")

            sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
            if not sprint:
                raise Exception("Sprint not found after creation")

            return sprint
        except Exception as e:
            print(f"Failed to create sprint: {e}")
            raise

    async def get_project_sprints(self, project_id: int, user_id: int):
        """Get all sprints for a project"""
        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, project_id)
        if not has_access:
            raise Exception("Access denied to project")

        try:
            sprints = await self.sprintsRepo.get_project_sprints(project_id)
            return sprints
        except Exception as e:
            print(f"Failed to get project sprints: {e}")
            raise

    async def get_sprint_by_id(self, sprint_id: int, user_id: int):
        """Get sprint by ID"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        return sprint

    async def update_sprint(self, sprint_id: int, sprint_data: SprintUpdate, user_id: int):
        """Update sprint"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Validate dates if provided
        start_date = sprint_data.start_date if sprint_data.start_date else sprint['start_date']
        end_date = sprint_data.end_date if sprint_data.end_date else sprint['end_date']
        
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")

        try:
            await self.sprintsRepo.update_sprint(
                sprint_id=sprint_id,
                name=sprint_data.name if sprint_data.name else sprint['name'],
                description=sprint_data.description if sprint_data.description is not None else sprint['description'],
                start_date=str(start_date),
                end_date=str(end_date),
                status=sprint_data.status.value if sprint_data.status else sprint['status'],
                goal=sprint_data.goal if sprint_data.goal is not None else sprint['goal'],
                velocity_target=sprint_data.velocity_target if sprint_data.velocity_target is not None else sprint['velocity_target']
            )
            
            updated_sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
            return updated_sprint
        except Exception as e:
            print(f"Failed to update sprint: {e}")
            raise

    async def delete_sprint(self, sprint_id: int, user_id: int):
        """Delete sprint"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        try:
            await self.sprintsRepo.delete_sprint(sprint_id)
            return True
        except Exception as e:
            print(f"Failed to delete sprint: {e}")
            raise

    async def start_sprint(self, sprint_id: int, user_id: int):
        """Start sprint"""
        # Get sprint first to check project access and current status
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Check if sprint can be started
        if sprint['status'] != 'planning':
            raise ValueError(f"Sprint can only be started from 'planning' status. Current status: {sprint['status']}")

        try:
            await self.sprintsRepo.update_sprint_status(sprint_id, 'active')
            updated_sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
            return updated_sprint
        except Exception as e:
            print(f"Failed to start sprint: {e}")
            raise

    async def complete_sprint(self, sprint_id: int, user_id: int):
        """Complete sprint"""
        # Get sprint first to check project access and current status
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Check if sprint can be completed
        if sprint['status'] not in ['planning', 'active']:
            raise ValueError(f"Sprint can only be completed from 'planning' or 'active' status. Current status: {sprint['status']}")

        try:
            await self.sprintsRepo.update_sprint_status(sprint_id, 'completed')
            updated_sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
            return updated_sprint
        except Exception as e:
            print(f"Failed to complete sprint: {e}")
            raise

    async def cancel_sprint(self, sprint_id: int, user_id: int):
        """Cancel sprint"""
        # Get sprint first to check project access and current status
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Check if sprint can be cancelled
        if sprint['status'] in ['completed', 'cancelled']:
            raise ValueError(f"Sprint cannot be cancelled from '{sprint['status']}' status")

        try:
            await self.sprintsRepo.update_sprint_status(sprint_id, 'cancelled')
            updated_sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
            return updated_sprint
        except Exception as e:
            print(f"Failed to cancel sprint: {e}")
            raise

    async def add_issues_to_sprint(self, sprint_id: int, issue_data: IssueAddToSprint, user_id: int):
        """Add issues to sprint"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Validate issues exist and belong to the same project
        for issue_id in issue_data.issue_ids:
            issue = await self.sprintsRepo.get_issue_by_id(issue_id)
            if not issue:
                raise ValueError(f"Issue {issue_id} not found")
            if issue['project_id'] != sprint['project_id']:
                raise ValueError(f"Issue {issue_id} does not belong to the same project as sprint")

        try:
            await self.sprintsRepo.add_issues_to_sprint(sprint_id, issue_data.issue_ids)
            return {"message": f"Successfully added {len(issue_data.issue_ids)} issues to sprint"}
        except Exception as e:
            print(f"Failed to add issues to sprint: {e}")
            raise

    async def remove_issue_from_sprint(self, sprint_id: int, issue_id: int, user_id: int):
        """Remove issue from sprint"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Check if issue exists in sprint
        issue_in_sprint = await self.sprintsRepo.issue_exists_in_sprint(sprint_id, issue_id)
        if not issue_in_sprint:
            raise ValueError("Issue is not in this sprint")

        try:
            await self.sprintsRepo.remove_issue_from_sprint(sprint_id, issue_id)
            return {"message": "Successfully removed issue from sprint"}
        except Exception as e:
            print(f"Failed to remove issue from sprint: {e}")
            raise

    async def get_sprint_issues(self, sprint_id: int, user_id: int):
        """Get all issues in sprint"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        try:
            issues = await self.sprintsRepo.get_sprint_issues(sprint_id)
            return issues
        except Exception as e:
            print(f"Failed to get sprint issues: {e}")
            raise

    async def reorder_sprint_backlog(self, sprint_id: int, reorder_data: SprintBacklogReorder, user_id: int):
        """Reorder sprint backlog"""
        # Get sprint first to check project access
        sprint = await self.sprintsRepo.get_sprint_by_id(sprint_id)
        if not sprint:
            raise Exception("Sprint not found")

        # Check if user has access to project
        has_access = await self.sprintsRepo.user_has_project_access(user_id, sprint['project_id'])
        if not has_access:
            raise Exception("Access denied to sprint")

        # Validate that all issues belong to this sprint
        current_issues = await self.sprintsRepo.get_sprint_issues(sprint_id)
        current_issue_ids = {issue['issue_id'] for issue in current_issues}
        
        for issue_id in reorder_data.issue_ids:
            if issue_id not in current_issue_ids:
                raise ValueError(f"Issue {issue_id} is not in this sprint")

        # Validate that all sprint issues are included in the reorder
        if set(reorder_data.issue_ids) != current_issue_ids:
            raise ValueError("Reorder must include all issues currently in the sprint")

        try:
            await self.sprintsRepo.reorder_sprint_backlog(sprint_id, reorder_data.issue_ids)
            return {"message": "Successfully reordered sprint backlog"}
        except Exception as e:
            print(f"Failed to reorder sprint backlog: {e}")
            raise
