from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.organization_requests import OrganizationRequestsService
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Organization Requests"], dependencies=[Depends(bearer)])

requestsService = OrganizationRequestsService()

@router.get("/organization-requests/outgoing")
async def get_outgoing_requests(request: Request):
    """Get all outgoing requests sent by current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        requests = await requestsService.get_outgoing_requests(user["id"])
        return requests
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get outgoing requests")

@router.get("/organization-requests/incoming")
async def get_incoming_requests(request: Request):
    """Get all incoming requests for current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        requests = await requestsService.get_incoming_requests(user["id"])
        return requests
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get incoming requests")

@router.post("/organizations/{org_id}/requests")
async def send_request(org_id: int, receiver_email: str, request: Request):
    """Send request to join organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = await requestsService.send_request(org_id, user["id"], receiver_email)
        return result
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "User not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "already sent" in str(e) or "already processed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send request")

@router.put("/organization-requests/{request_id}/respond/{organization_id}")
async def respond_to_request(request_id: int, decision: str,organization_id:int, request: Request):
    """Respond to request (accept/reject)"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = await requestsService.respond_to_request(request_id, decision, user["id"],organization_id)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Request not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "already processed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to respond to request")