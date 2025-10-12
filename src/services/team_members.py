from src.repositories.team_members import TeamMembersRepository
from src.schemas.team_members import TeamMemberCreate

class TeamMembersService:
    def __init__(self):
        self.teamMembersRepo = TeamMembersRepository()

    async def add_team_member(self, team_id: int, user_id: int, requester_id: int):
        """Add user to team"""
        # Check if requester has access to team
        has_access = await self.teamMembersRepo.user_has_team_access(requester_id, team_id)
        if not has_access:
            raise Exception("Access denied to team")

        # Check if user exists
        user = await self.teamMembersRepo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        try:
            member_id = await self.teamMembersRepo.add_team_member(team_id, user_id)
            return {"id": member_id, "team_id": team_id, "user_id": user_id}
        except Exception as e:
            if "Duplicate entry" in str(e) or "unique_team_user" in str(e):
                raise Exception("User is already a member of this team")
            print(f"Failed to add team member: {e}")
            raise

    async def get_team_members(self, team_id: int, requester_id: int):
        """Get all team members"""
        # Check if requester has access to team
        has_access = await self.teamMembersRepo.user_has_team_access(requester_id, team_id)
        if not has_access:
            raise Exception("Access denied to team")

        try:
            members = await self.teamMembersRepo.get_team_members(team_id)
            return members
        except Exception as e:
            print(f"Failed to get team members: {e}")
            raise

    async def remove_team_member(self, team_id: int, user_id: int, requester_id: int):
        """Remove user from team"""
        # Check if requester has access to team
        has_access = await self.teamMembersRepo.user_has_team_access(requester_id, team_id)
        if not has_access:
            raise Exception("Access denied to team")

        try:
            await self.teamMembersRepo.remove_team_member(team_id, user_id)
            return {"message": "Team member removed successfully"}
        except Exception as e:
            print(f"Failed to remove team member: {e}")
            raise
