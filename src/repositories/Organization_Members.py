from src.core.database import db


class OrganizationMembersRepository:

    async def invite_organization_member(self, user_id: int, invited_by: int):
        query = """
        INSERT INTO organization_invitations (user_id, invited_by) VALUES ($1, $2)
        """
        parameters = (user_id, invited_by)
        result = await db.execute_insert(query, parameters)
        return result

    async def get_organization_invitations(self, user_id: int):
        query = """
        SELECT * FROM organization_invitations
        WHERE user_id = $1
        """
        parameters = (user_id,)
        result = await db.execute_query(query, parameters)
        return result

    async def accept_invitations(self, user_id: int, organization_id: int):
        query = """
        INSERT INTO organization_users (user_id, organization_id) VALUES ($1, $2)
        """
        parameters = (user_id, organization_id)
        result = await db.execute_insert(query, parameters)
        return result