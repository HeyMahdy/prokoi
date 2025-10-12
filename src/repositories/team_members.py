from src.core.database import db
import aiomysql

class TeamMembersRepository:
    async def add_team_member(self, team_id: int, user_id: int) -> int:
        """Add user to team"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "INSERT INTO user_team (team_id, user_id) VALUES (%s, %s)",
                    (team_id, user_id)
                )
                member_id = cur.lastrowid

            await conn.commit()
            return member_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_team_members(self, team_id: int) -> list[dict]:
        """Get all team members with user details"""
        query = """
        SELECT ut.id, ut.team_id, ut.user_id, u.name, u.email
        FROM user_team ut
        JOIN users u ON ut.user_id = u.id
        WHERE ut.team_id = %s
        ORDER BY u.name ASC
        """
        return await db.execute_query(query, (team_id,))

    async def remove_team_member(self, team_id: int, user_id: int) -> bool:
        """Remove user from team"""
        query = """
        DELETE FROM user_team
        WHERE team_id = %s AND user_id = %s
        """
        await db.execute_query(query, (team_id, user_id))
        return True

    async def is_team_member(self, team_id: int, user_id: int) -> bool:
        """Check if user is a member of the team"""
        query = """
        SELECT 1
        FROM user_team
        WHERE team_id = %s AND user_id = %s
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
        WHERE t.id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id, user_id))
        return len(rows) > 0

    async def get_user_by_id(self, user_id: int) -> dict | None:
        """Get user by ID"""
        query = """
        SELECT id, name, email
        FROM users
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id,))
        return rows[0] if rows else None
