from src.repositories.organization_requests import OrganizationRequestsRepository
from src.repositories.organizations import OrganizationsRepository

class OrganizationRequestsService:
    def __init__(self):
        self.requestsRepo = OrganizationRequestsRepository()
        self.orgRepo = OrganizationsRepository()

    async def get_outgoing_requests(self, sender_id: int):
        """Get all outgoing requests sent by user"""
        try:
            requests = await self.requestsRepo.get_outgoing_requests(sender_id)
            return requests
        except Exception as e:
            print(f"Failed to get outgoing requests: {e}")
            raise

    async def get_incoming_requests(self, receiver_id: int):
        """Get all incoming requests for user"""
        try:
            requests = await self.requestsRepo.get_incoming_requests(receiver_id)
            return requests
        except Exception as e:
            print(f"Failed to get incoming requests: {e}")
            raise

    async def send_request(self, organization_id: int, sender_id: int, receiver_email: str):
        """Send request to join organization"""
        # Check if sender has access to organization (to send requests on behalf)
        has_access = await self.requestsRepo.user_has_org_access(sender_id, organization_id)
        if not has_access:
            raise Exception("Access denied to organization")

        # Find receiver by email
        from src.repositories.users import UserRepository
        userRepo = UserRepository()
        receiver = await userRepo.find_user_by_email(receiver_email)
        if not receiver:
            raise Exception("User not found")

        # Check if request already exists
        existing_requests = await self.requestsRepo.get_outgoing_requests(sender_id)
        for req in existing_requests:
            if req['organization_id'] == organization_id and req['receiver_id'] == receiver['id']:
                if req['status'] == 'pending':
                    raise Exception("Request already sent and pending")
                elif req['status'] in ['accepted', 'rejected']:
                    raise Exception("Request already processed")

        try:
            request_id = await self.requestsRepo.create_outgoing_request(organization_id, sender_id, receiver['id'])
            return {
                "id": request_id,
                "message": "Request sent successfully",
                "receiver_email": receiver_email
            }
        except Exception as e:
            print(f"Failed to send request: {e}")
            raise

    async def respond_to_request(self, request_id: int, status: str, user_id: int,organization_id:int):
        """Respond to request (accept/reject)"""
        # Validate status
        valid_statuses = ['accepted', 'rejected']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")

        try:
            # Get request details
            request = await self.requestsRepo.get_request_by_id(request_id, user_id)
            if not request:
                raise Exception("Request not found or access denied")

            if request['status'] != 'pending':
                raise Exception("Request already processed")

            # Update status
            await self.requestsRepo.update_request_status(request_id, status, user_id,organization_id)

            # If accepted, add user to organization
            if status == 'accepted':
                await self.orgRepo.invite_member(
                    request['sender_id'],
                    request['receiver_id'],
                    request['organization_id']
                )

            return {
                "message": f"Request {status} successfully",
                "request_id": request_id
            }
        except Exception as e:
            print(f"Failed to respond to request: {e}")
            raise