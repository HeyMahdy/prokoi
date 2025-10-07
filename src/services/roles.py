from collections import defaultdict

from src.repositories.RolesRepository import RolesRepository
from src.schemas.roles import roleOut, permission


class RoleService:
    def __init__(self):
        self.role_repository = RolesRepository()

    async def create_role(self, role_name: str, org_id: int):
        try:
            find_org_id = await self.role_repository.create_role(org_id, role_name)
            return find_org_id
        except Exception as e:
            raise Exception("Failed to create role", e)

    async def get_role_list(self, org_id: int):
        try:
            roles = await self.role_repository.list_organization_roles(org_id)
            return roles
        except Exception as e:
            raise Exception("Failed to get role list", e)

    async def get_all_permissions(self):
        try:
            permissions = await self.role_repository.list_all_permissions()
            return permissions
        except Exception as e:
            raise Exception("Failed to get permissions", e)

    async def add_role_permission(self, role_id: int, permission_name: str):
        try:
            result = await self.role_repository.assign_permission_to_role(role_id, permission_name)
            return result
        except Exception as e:
            raise Exception("Failed to add permission", e)

    async def get_all_role_permissions(self, org_id: int):
        try:
            rows = await self.role_repository.get_role_permissions(org_id)
            # Example row: {'name': 'webi', 'p.name': 'assign_task'}

            roles_dict = {}  # normal dict

            for r in rows:
                role_name = r["name"]
                perm = permission(name=r["p.name"])

                if role_name in roles_dict:
                    roles_dict[role_name].append(perm)
                else:
                    roles_dict[role_name] = [perm]

            # Convert to list of RoleOut objects
            all_roles = [roleOut(name=role_name, permissions=perms)
                         for role_name, perms in roles_dict.items()]

            return all_roles

        except Exception as e:
            raise Exception("Failed to get all role permissions", e)




