from src.repositories.RolesRepository import RolesRepository
from src.repositories.organizations import OrganizationsRepository
from src.schemas.organizations import OrganizationCreate


class OrginizationsService:
    def __init__(self):
        self.roleRepo = RolesRepository()
        self.orgRepo = OrganizationsRepository()

    async def create_organization(self, name: str, user_id: int):
        name = (name or "").strip()
        if not name:
            raise ValueError("Organization name is required")

        try:
            org_id = await self.orgRepo.create_organization(name, user_id)
            if not org_id:
                raise Exception("Failed to create organization")

            org = await self.orgRepo.get_organization_by_id(org_id)
            if not org:
                raise Exception("Organization not found after creation")
            print(org)

            return org
        except Exception as e:
            print(f"Failed to create organization: {e}")

    async def get_organization_by_id(self, user_id: int):
        try:
         org = await self.orgRepo.get_all_organizations(user_id)
         return org
        except Exception as e:
             raise Exception(e)





