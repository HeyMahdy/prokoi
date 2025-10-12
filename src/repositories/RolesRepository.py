


from typing import List, Optional
from src.core.database import db

class RolesRepository:
    async def list_organization_roles(self, organization_id: int):
        query = """
        SELECT r.id, r.name, r.organization_id
        FROM roles r
        WHERE r.organization_id = %s
        ORDER BY r.name ASC
        """
        return await db.execute_query(query, [organization_id])

    async def create_role(self, organization_id: int, name: str) -> int:
        query = """
        INSERT INTO roles (name, organization_id)
        VALUES (%s, %s)
        """
        return await db.execute_insert(query, [name, organization_id])

    async def update_role(self, role_id: int, name: str) -> None:
        query = """
        UPDATE roles
        SET name = %s
        WHERE id = %s
        """
        await db.execute_query(query, [name, role_id])

    async def delete_role(self, role_id: int) -> None:
        # Remove role <-> permissions, user <-> role links, then role
        async with db.get_connection() as conn:
            try:
                await conn.execute("DELETE FROM role_permissions WHERE role_id = %s", [role_id])
                await conn.execute("DELETE FROM user_role WHERE role_id = %s", [role_id])
                await conn.execute("DELETE FROM roles WHERE id = %s", [role_id])
                await conn.commit()
            except Exception:
                await conn.rollback()
                raise

    async def list_all_permissions(self) :
        query = """
        SELECT p.id, p.name
        FROM permissions p
        ORDER BY p.name ASC
        """
        return await db.execute_query(query, [])

    async def assign_permission_to_role(self, role_id: int, permission_name: str):
        query = """
                INSERT INTO role_permissions (role_id, permission_id)
                SELECT %s, id FROM permissions WHERE name = %s;
                """
        try:
            # 👇 correct parameter order!
            return await db.execute_insert(query, [role_id, permission_name])
        except Exception as e:
            raise ValueError(f"Failed to add permission: {e}")


    async def remove_permission_from_role(self, role_id: int, permission_id: int) -> None:
        query = """
        DELETE FROM role_permissions
        WHERE role_id = %s AND permission_id = %s
        """
        await db.execute_query(query, [role_id, permission_id])

    async def list_role_permissions(self, role_id: int) -> List[dict]:
        query = """
        SELECT p.id, p.name, p.code
        FROM role_permissions rp
        JOIN permissions p ON p.id = rp.permission_id
        WHERE rp.role_id = %s
        ORDER BY p.name ASC
        """
        return await db.execute_query(query, [role_id])

    async def get_role_by_id(self, role_id: int) -> Optional[dict]:
        query = """
        SELECT r.id, r.name, r.organization_id
        FROM roles r
        WHERE r.id = %s
        """
        rows = await db.execute_query(query, [role_id])
        return rows[0] if rows else None

    async def is_permission(self, user_id: int, permission_list: list[str]) -> bool:
        """Check if user has any of the specified permissions"""
        if not permission_list:
            return False

        # Create placeholders for the permission names
        placeholders = ','.join(['%s'] * len(permission_list))

        query = """
        SELECT 1
        FROM user_role ur 
        JOIN role_permissions rp ON ur.role_id = rp.role_id
        JOIN permissions p ON rp.permission_id = p.id
        WHERE ur.user_id = %s 
        AND p.name IN ({})
        LIMIT 1
        """.format(placeholders)

        params = [user_id] + permission_list
        rows = await db.execute_query(query, params)
        return len(rows) > 0

    async def get_role_permissions(self, organization_id: int):
      try:
        query = """
        select r.name , p.name
        from roles r
        join role_permissions rp on r.id = rp.role_id
        join permissions p on p.id = rp.permission_id
        where r.organization_id = %s 
        """
        results = await db.execute_query(query, [organization_id,])
        return results
      except Exception as e:
          raise ValueError("error has come",e)























