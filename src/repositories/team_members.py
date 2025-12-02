from src.core.database import db


class TeamMembersRepository:
    async def add_team_member(self, team_id: int, user_id: int) -> int:
        """Add user to team"""
        async for conn in db.connection():
            async with conn.transaction():
                member_record = await conn.fetchrow(
                    "INSERT INTO user_team (team_id, user_id) VALUES ($1, $2) RETURNING id",
                    team_id, user_id
                )
                member_id = member_record['id']
                return member_id
        # Fallback return in case the async for loop doesn't execute
        raise Exception("Failed to add team member")

    async def get_team_members(self, team_id: int) -> list[dict]:
        """Get all team members with user details"""
        query = """
        SELECT ut.id, ut.team_id, ut.user_id, u.name, u.email
        FROM user_team ut
        JOIN users u ON ut.user_id = u.id
        WHERE ut.team_id = $1
        ORDER BY u.name ASC
        """
        return await db.execute_query(query, (team_id,))

    async def remove_team_member(self, team_id: int, user_id: int) -> bool:
        """Remove user from team"""
        query = """
        DELETE FROM user_team
        WHERE team_id = $1 AND user_id = $2
        """
        await db.execute_query(query, (team_id, user_id))
        return True

    async def is_team_member(self, team_id: int, user_id: int) -> bool:
        """Check if user is a member of the team"""
        query = """
        SELECT 1
        FROM user_team
        WHERE team_id = $1 AND user_id = $2
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id, user_id))
        return len(rows) > 0

    async def user_has_team_access(self, user_id: int, team_id: int) -> bool:
        """Check if user has access to team (either member or org member)"""
        # Check if user is team member
        is_member = await self.is_team_member(team_id, user_id)
        if is_member:
            return True

        # Check if user is organization member
        query = """
        SELECT 1
        FROM teams t
        JOIN organization_users ou ON t.organization_id = ou.organization_id
        WHERE t.id = $1 AND ou.user_id = $2
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id, user_id))
        return len(rows) > 0

    async def get_user_by_id(self, user_id: int) -> dict | None:
        """Get user by ID"""
        query = """
        SELECT id, name, email
        FROM users
        WHERE id = $1
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id,))
        return rows[0] if rows else None