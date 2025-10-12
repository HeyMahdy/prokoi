from src.repositories.teams import TeamsRepository

class TeamsService:
    def __init__(self):
        self.teamRepo = TeamsRepository()

    async def create_team(self, organization_id: int, name: str, user_id: int):
        """Create a new team"""
        name = (name or "").strip()
        if not name:
            raise ValueError("Team name is required")

        print(f"Creating team: org_id={organization_id}, name={name}, user_id={user_id}")

        # Check if user has access to organization
        has_access = await self.teamRepo.user_has_org_access(user_id, organization_id)
        print(f"Access check result: {has_access}")
        if not has_access:
            raise Exception("Access denied to organization")

        try:
            team_id = await self.teamRepo.create_team(organization_id, name)
            print(f"Created team with id: {team_id}")
            if not team_id:
                raise Exception("Failed to create team")

            team = await self.teamRepo.get_team_by_id(team_id)
            print(f"Retrieved team: {team}")
            if not team:
                raise Exception("Team not found after creation")

            return team
        except Exception as e:
            print(f"Failed to create team: {e}")
            raise

    async def get_organization_teams(self, organization_id: int, user_id: int):
        """Get all teams for an organization"""
        # Check if user has access to organization
        has_access = await self.teamRepo.user_has_org_access(user_id, organization_id)
        if not has_access:
            raise Exception("Access denied to organization")

        try:
            teams = await self.teamRepo.get_organization_teams(organization_id)
            return teams
        except Exception as e:
            print(f"Failed to get teams: {e}")
            raise

    async def get_team_by_id(self, team_id: int, user_id: int):
        """Get team by ID"""
        try:
            team = await self.teamRepo.get_team_by_id(team_id)
            if not team:
                raise Exception("Team not found")

            # Check if user has access to the team's organization
            has_access = await self.teamRepo.user_has_org_access(user_id, team["organization_id"])
            if not has_access:
                raise Exception("Access denied to team")

            return team
        except Exception as e:
            print(f"Failed to get team: {e}")
            raise

    async def update_team(self, team_id: int, name: str, user_id: int):
        """Update team"""
        name = (name or "").strip()
        if not name:
            raise ValueError("Team name is required")

        try:
            # First get the team to check organization access
            team = await self.teamRepo.get_team_by_id(team_id)
            if not team:
                raise Exception("Team not found")

            has_access = await self.teamRepo.user_has_org_access(user_id, team["organization_id"])
            if not has_access:
                raise Exception("Access denied to team")

            await self.teamRepo.update_team(team_id, name)
            updated_team = await self.teamRepo.get_team_by_id(team_id)
            return updated_team
        except Exception as e:
            print(f"Failed to update team: {e}")
            raise

    async def delete_team(self, team_id: int, user_id: int):
        """Delete team"""
        try:
            # First get the team to check organization access
            team = await self.teamRepo.get_team_by_id(team_id)
            if not team:
                raise Exception("Team not found")

            has_access = await self.teamRepo.user_has_org_access(user_id, team["organization_id"])
            if not has_access:
                raise Exception("Access denied to team")

            await self.teamRepo.delete_team(team_id)
            return {"message": "Team deleted successfully"}
        except Exception as e:
            print(f"Failed to delete team: {e}")
            raise
