from src.core.database import db


class OrganizationsRepository:
    async def create_organization(self, name: str, user_id: int):
        async for conn in db.connection():
            async with conn.transaction():
                # Create organization
                org_record = await conn.fetchrow(
                    "INSERT INTO organizations (name) VALUES ($1) RETURNING id",
                    name
                )
                org_id = org_record['id']
             

                # Create admin role
                role_record = await conn.fetchrow(
                    "INSERT INTO roles (name, organization_id) VALUES ($1, $2) RETURNING id",
                    "admin", org_id
                )
                role_id = role_record['id']
            

                # Assign role to user
                await conn.execute(
                    "INSERT INTO user_role (user_id, role_id) VALUES ($1, $2)",
                    user_id, role_id
                )

                # Add user to organization
                await conn.execute(
                    "INSERT INTO organization_users (user_id, organization_id) VALUES ($1, $2)",
                    user_id, org_id
                )
                print("user added to organization")

                # Assign default permission
                await conn.execute(
                    "INSERT INTO role_permissions (role_id, permission_id) VALUES ($1, $2)",
                    role_id, 1
                )

                print("this is id")
                print(org_id)
                return org_id

    async def get_organization_by_id(self, org_id: int):
        query = "SELECT * FROM organizations WHERE organizations.id = $1"
        params = (org_id,)
        result = await db.execute_query(query, params)
        return result

    async def get_all_organizations(self, user_id: int):
        print("in insdie the repo")
        query = """
        SELECT DISTINCT o.id, o.name, o.created_at, o.updated_at 
        FROM organizations o
        JOIN organization_users ur ON o.id = ur.organization_id
        WHERE ur.user_id = $1
        """
        params = (user_id,)
        result = await db.execute_query(query, params)
        print("result")
        print(result)
        return result

    async def invite_member(self, invitedBy: int, receiver: int, org_id: int):
        query = """
        INSERT INTO organization_invitations (invited_by, user_id, organization_id) 
        VALUES ($1, $2, $3)
        """
        params = (invitedBy, receiver, org_id)
        result = await db.execute_insert(query, params)
        return result

    async def invite_list(self, user_id: int):
        query = """
        SELECT * FROM organization_invitations
        WHERE invited_by = $1 OR user_id = $1
        """
        params = (user_id,)
        result = await db.execute_query(query, params)
        return result

    async def accept_invitation(self, user_id: int, invitation_id: int):
        """Accept an organization invitation"""
        async for conn in db.connection():
            async with conn.transaction():
                # 1. Get invitation details
                invitation = await conn.fetchrow("""
                    SELECT organization_id, user_id, status
                    FROM organization_invitations
                    WHERE id = $1 AND user_id = $2
                """, invitation_id, user_id)

                if not invitation:
                    raise Exception("Invitation not found")

                if invitation['status'] != 'pending':
                    raise Exception("Invitation already processed")

                # 2. Add user to organization_users
                await conn.execute("""
                    INSERT INTO organization_users (organization_id, user_id)
                    VALUES ($1, $2)
                """, invitation['organization_id'], user_id)

                # 3. Update invitation status to 'accepted'
                await conn.execute("""
                    UPDATE organization_invitations
                    SET status = 'accepted',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = $1
                """, invitation_id)

                # 4. Get organization details for response
                organization = await conn.fetchrow("""
                    SELECT id, name, created_at, updated_at
                    FROM organizations
                    WHERE id = $1
                """, invitation['organization_id'])

                return {
                    "organization": dict(organization),
                    "message": "Successfully joined organization"
                }

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
                WHERE ou.organization_id = $1
                ORDER BY ou.created_at DESC 
                """
        return await db.execute_query(query, (organization_id,))

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
                SELECT 1
                FROM organization_users ou
                WHERE ou.organization_id = $1 
                  AND ou.user_id = $2 
                LIMIT 1
                """
        rows = await db.execute_query(query, (organization_id, user_id))
        return len(rows) > 0