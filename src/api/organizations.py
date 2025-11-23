from urllib import request

from fastapi import Depends, Request
from fastapi import APIRouter, HTTPException, Request, status ,Depends
from typing import Any
from src.services.orginizations import OrginizationsService
from src.schemas.organizations import OrganizationResponse
from fastapi.security import HTTPBearer
from src.dependencies.permission import require_permissions

bearer = HTTPBearer()
router = APIRouter(prefix="/api/organizations", tags=["Organizations"],dependencies=[Depends(bearer)])

orgservice = OrginizationsService()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_org(name: str, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        org = await orgservice.create_organization(name, user["id"])
        
        return org
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create organization")

@router.get("/get", status_code=status.HTTP_200_OK,description="Get all organization user is joined or created.")
async def get_org(request: Request):
    user = getattr(request.state, "user")
    print(user)
    try :
        org = await orgservice.get_organization_by_id(user["id"])
        return org
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to find organization")

@router.post("/{org_id}/invite", status_code=status.HTTP_201_CREATED, description="Invite to join organization.")
async def invite(org_id: int, email: str, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        org = await orgservice.send_invite(email, user["id"], org_id)
        return org
    except Exception as e:
        # Check if it is a duplicate entry error
        if hasattr(e, "args") and e.args and isinstance(e.args[0], int) and e.args[0] == 1062:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation already sent"
            )
        # Otherwise raise generic error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send invite: {str(e)}"
        )

@router.get("/invite_list", status_code=status.HTTP_200_OK,description="Get all invites")
async def get_invite_list(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        result = await orgservice.invite_list(user["id"])
        return result
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get invite list")


@router.post("/invitations/{invitation_id}/accept", status_code=status.HTTP_200_OK)
async def accept_invitation(invitation_id: int, request: Request):
    """Accept organization invitation"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = await orgservice.accept_invitation(user["id"], invitation_id)
        return result
    except Exception as e:
        if "Invitation not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "already processed" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to accept invitation")


@router.get("/{org_id}/users", dependencies=[Depends(require_permissions(["all", "view_organization_users"]))])
async def get_organization_users(org_id: int, request: Request):
    """Get all users in organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        users = await orgservice.get_organization_users(org_id, user["id"])
        return users
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get organization users")