from src.repositories.RolesRepository import RolesRepository
from src.repositories.organizations import OrganizationsRepository
from src.repositories.users import UserRepository
from src.schemas.organizations import OrganizationCreate


class OrginizationsService:
    def __init__(self):
        self.roleRepo = RolesRepository()
        self.orgRepo = OrganizationsRepository()
        self.userRepo = UserRepository()

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

    async def send_invite(self, email: str, invited_by: int,org_id: int):
        try:
            user = await self.userRepo.find_user_by_email(email)
            if not user:
                raise Exception("Failed to find user")
            print(user)
            invite_id = await self.orgRepo.invite_member(invited_by,user["id"],org_id)
            print("this is inside org")
            print(invite_id)
            return {"id": invite_id, "message": "Invitation sent successfully"}
        except Exception as e:
            print(f"Failed to send invite: {e}")
            raise

    async def invite_list(self,user_id: int):
        try:
            orgs = await self.orgRepo.invite_list(user_id)
            print("this is inside org")
            print(orgs)
            return orgs
        except Exception as e:
            print(f"Failed to get invite list: {e}")
            raise

    async def accept_invitation(self, user_id: int, invitation_id: int):
        """Accept organization invitation"""
        try:
            result = await self.orgRepo.accept_invitation(user_id, invitation_id)
            return result
        except Exception as e:
            print(f"Failed to accept invitation: {e}")
            raise

    async def get_organization_users(self, organization_id: int, requester_id: int):
        """Get all users in organization"""
        # Check if requester has access to organization
        has_access = await self.orgRepo.user_has_org_access(requester_id, organization_id)
        if not has_access:
            raise Exception("Access denied to organization")

        try:
            users = await self.orgRepo.get_organization_users(organization_id)
            return users
        except Exception as e:
            print(f"Failed to get organization users: {e}")
            raise






