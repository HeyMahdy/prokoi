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
        print(result)

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








