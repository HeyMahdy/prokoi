from src.repositories.RolesRepository import RolesRepository

class RoleService:
    def __init__(self):
        self.role_repository = RolesRepository()

    async def create_role(self, role_name: str,org_id: int):
        try:
            find_org_id = await self.role_repository.create_role(org_id, role_name)
            return  find_org_id
        except Exception as e:
            raise Exception("Failed to create role", e)


    async def get_role_list(self, org_id: int):
        try:
            roles = await self.role_repository.list_organization_roles(org_id)
            return roles
        except Exception as e:
            raise Exception("Failed to get role list", e)



