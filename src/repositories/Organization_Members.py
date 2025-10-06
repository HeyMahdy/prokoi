from src.core.database import db


class OrganizationMembersRepository:

    async def invite_organization_member(self, user_id:int, invited_by: int):

        query = """
        insert into organization_invitations (user_id, invited_by) values (%s, %s)
        """
        parameters = (user_id, invited_by)
        result = await db.execute_insert(query, parameters)
        return result

    async def get_organization_invitations(self, user_id:int):
        query = """
        select * from organization_invitations
            """
        parameters = (user_id)
        result = await db.execute_query(query, parameters)


    async def accept_invitations(self, user_id:int,organization_id:int):
        query = """
        insert into organization_users (user_id, organization_id) values (%s, %s)
            """
        parameters = (user_id, organization_id)
        result = await db.execute_insert(query, parameters)
        return result
