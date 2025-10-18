from src.repositories.velocity import VelocityRepository
from src.schemas.velocity import VelocityUpdate

class VelocityService:
    def __init__(self):
        self.velocityRepo = VelocityRepository()

    async def get_team_velocity_history(self, team_id: int, user_id: int):
        """Get team velocity history across all projects"""
        # Check if user has access to team

        try:
            velocity_history = await self.velocityRepo.get_team_velocity_history(team_id)
            return velocity_history
        except Exception as e:
            print(f"Failed to get team velocity history: {e}")
            raise

    async def update_team_velocity(self, team_id: int, velocity_data: VelocityUpdate, user_id: int):
        """Update team velocity (requires project context)"""
        # Check if user has access to team


        # Validate velocity data
        if velocity_data.avg_hours_per_point is not None:
            if velocity_data.avg_hours_per_point < 0:
                raise ValueError("Average hours per point cannot be negative")

        try:
            # For general team velocity update, we need to get all projects the team is assigned to
            # This is a simplified approach - in practice, you might want to specify a project
            velocity_history = await self.velocityRepo.get_team_velocity_history(team_id)
            
            if not velocity_history:
                raise ValueError("Team must be assigned to at least one project to update velocity")
            
            # Update velocity for the most recent project (or you could require project_id in the request)
            latest_project = velocity_history[0]
            project_id = latest_project['project_id']
            
            await self.velocityRepo.upsert_team_velocity(
                team_id=team_id,
                project_id=project_id,
                avg_hours_per_point=velocity_data.avg_hours_per_point
            )
            
            updated_velocity = await self.velocityRepo.get_team_project_velocity(team_id, project_id)
            return updated_velocity
        except Exception as e:
            print(f"Failed to update team velocity: {e}")
            raise

    async def get_team_project_velocity(self, team_id: int, project_id: int, user_id: int):
        """Get team velocity for specific project"""
        # Check if user has access to project
        has_project_access = await self.velocityRepo.user_has_project_access(user_id, project_id)
        if not has_project_access:
            raise Exception("Access denied to project")

        # Check if team has access to project
        has_team_access = await self.velocityRepo.team_has_project_access(team_id, project_id)
        if not has_team_access:
            raise Exception("Team is not assigned to this project")

        try:
            velocity = await self.velocityRepo.get_team_project_velocity(team_id, project_id)
            if not velocity:
                # Return default structure if no velocity data exists
                return {
                    "team_id": team_id,
                    "project_id": project_id,
                    "avg_hours_per_point": None,
                    "team_name": None,
                    "project_name": None,
                    "created_at": None,
                    "updated_at": None
                }
            return velocity
        except Exception as e:
            print(f"Failed to get team project velocity: {e}")
            raise

    async def update_team_project_velocity(self, team_id: int, project_id: int, velocity_data: VelocityUpdate, user_id: int):
        """Update team velocity for specific project"""
        # Check if user has access to project
        has_project_access = await self.velocityRepo.user_has_project_access(user_id, project_id)
        if not has_project_access:
            raise Exception("Access denied to project")

        # Check if team has access to project
        has_team_access = await self.velocityRepo.team_has_project_access(team_id, project_id)
        if not has_team_access:
            raise Exception("Team is not assigned to this project")

        # Validate velocity data
        if velocity_data.avg_hours_per_point is not None:
            if velocity_data.avg_hours_per_point < 0:
                raise ValueError("Average hours per point cannot be negative")

        try:
            await self.velocityRepo.upsert_team_velocity(
                team_id=team_id,
                project_id=project_id,
                avg_hours_per_point=velocity_data.avg_hours_per_point
            )
            
            updated_velocity = await self.velocityRepo.get_team_project_velocity(team_id, project_id)
            return updated_velocity
        except Exception as e:
            print(f"Failed to update team project velocity: {e}")
            raise
