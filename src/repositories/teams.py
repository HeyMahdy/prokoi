from src.core.database import db
import aiomysql

class TeamsRepository:
    async def create_team(self, organization_id: int, name: str) -> int:
        """Create a new team in an organization"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "INSERT INTO teams (organization_id, name) VALUES (%s, %s)",
                    (organization_id, name)
                )
                team_id = cur.lastrowid

            await conn.commit()
            return team_id
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_organization_teams(self, organization_id: int) -> list[dict]:
        """Get all teams for an organization"""
        query = """
        SELECT id, organization_id, name
        FROM teams
        WHERE organization_id = %s
        ORDER BY id DESC
        """
        return await db.execute_query(query, (organization_id,))

    async def get_team_by_id(self, team_id: int) -> dict | None:
        """Get team by ID"""
        query = """
        SELECT id, organization_id, name
        FROM teams
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (team_id,))
        return rows[0] if rows else None

    async def update_team(self, team_id: int, name: str) -> bool:
        """Update team name"""
        query = """
        UPDATE teams
        SET name = %s
        WHERE id = %s
        """
        result = await db.execute_query(query, (name, team_id))
        return True  # Assuming success if no exception

    async def delete_team(self, team_id: int) -> bool:
        """Delete team"""
        query = "DELETE FROM teams WHERE id = %s"
        await db.execute_query(query, (team_id,))
        return True  # Assuming success if no exception

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
        SELECT 1
        FROM organizations o
        JOIN organization_users ou ON o.id = ou.organization_id
        WHERE o.id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (organization_id, user_id))
        print(f"Checking access: user_id={user_id}, org_id={organization_id}, rows={len(rows)}")
        return len(rows) > 0
