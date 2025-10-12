from src.core.database import db
import aiomysql


class OrganizationsRepository:
    async def create_organization(self, name: str, user_id: int):
        conn = await db.get_connection()
        try:
            
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("INSERT INTO organizations (name) VALUES (%s)", (name,))
                org_id = cur.lastrowid
                print("this is org id ",org_id)

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("INSERT INTO roles (name, organization_id) VALUES (%s, %s)", ("admin", org_id))
                role_id = cur.lastrowid
                print("this is role id ",role_id)



            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("INSERT INTO user_role (user_id,role_id) VALUES (%s, %s)", (user_id, role_id))
                user_role_id = cur.lastrowid
                print("this is fuck id ",role_id)
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("INSERT INTO organization_users (user_id,organization_id) VALUES (%s, %s)", (user_id, org_id))
                organization_users_id = cur.lastrowid
                print("this is muck id ", organization_users_id)

            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("INSERT INTO role_permissions (role_id,permission_id) VALUES (%s, %s)", (role_id, 1))

            await conn.commit()
            return org_id
        except Exception:
            await conn.rollback()
            raise Exception("Failed to create organization",Exception)
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_organization_by_id(self,org_id:int):
        query = "SELECT * FROM organizations WHERE organizations.id = %s"
        params = {org_id,}
        result = await db.execute_query(query, params)
        return result


    async def get_all_organizations(self,user_id:int):
        print(user_id)
        query = """
        SELECT DISTINCT o.id, o.name, o.created_at, o.updated_at 
        FROM organizations o
        JOIN  organization_users ur ON o.id = ur.organization_id
        where ur.user_id = %s
        """
        params = (user_id,)
        result = await db.execute_query(query, params)
        print(result)
        return result

    async def invite_member (self, invitedBy:int, receiver:int,org_id:int):
        query = """
        insert into organization_invitations (invited_by, user_id, organization_id) values (%s, %s,%s)
        """
        params = (invitedBy, receiver,org_id)
        result = await db.execute_insert(query, params)
        return result

    async def invite_list(self,user_id:int):
        query = """
        select * from organization_invitations
        where invited_by = %s or user_id = %s
        """
        params = (user_id,user_id)
        result = await db.execute_query(query, params)
        return result

    async def accept_invitation(self, user_id: int, invitation_id: int):
        """Accept an organization invitation"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            # 1. Get invitation details
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("""
                                  SELECT organization_id, user_id, status
                                  FROM organization_invitations
                                  WHERE id = %s
                                    AND user_id = %s
                                  """, (invitation_id, user_id))
                invitation = await cur.fetchone()

                if not invitation:
                    raise Exception("Invitation not found")

                if invitation['status'] != 'pending':
                    raise Exception("Invitation already processed")

            # 2. Add user to organization_users
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("""
                                  INSERT INTO organization_users (organization_id, user_id)
                                  VALUES (%s, %s)
                                  """, (invitation['organization_id'], user_id))
                org_user_id = cur.lastrowid

            # 3. Update invitation status to 'accepted'
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("""
                                  UPDATE organization_invitations
                                  SET status     = 'accepted',
                                      updated_at = CURRENT_TIMESTAMP
                                  WHERE id = %s
                                  """, (invitation_id,))

            # 4. Get organization details for response
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("""
                                  SELECT id, name, created_at, updated_at
                                  FROM organizations
                                  WHERE id = %s
                                  """, (invitation['organization_id'],))
                organization = await cur.fetchone()

            await conn.commit()
            return {
                "organization": organization,
                "message": "Successfully joined organization"
            }

        except Exception as e:
            await conn.rollback()
            raise e
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def get_organization_users(self, organization_id: int) -> list[dict]:
        """Get all users in an organization"""
        query = """
                SELECT u.id, 
                       u.name, 
                       u.email, 
                       u.created_at, 
                       u.last_login_at, 
                       ou.created_at as joined_at
                FROM organization_users ou
                         JOIN users u ON ou.user_id = u.id
                WHERE ou.organization_id = %s
                ORDER BY ou.created_at DESC 
                """
        return await db.execute_query(query, (organization_id,))

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
                SELECT 1
                FROM organization_users ou
                WHERE ou.organization_id = %s \
                  AND ou.user_id = %s LIMIT 1 \
                """
        rows = await db.execute_query(query, (organization_id, user_id))
        return len(rows) > 0

