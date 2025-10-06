from urllib import request

from fastapi import Depends, Request
from fastapi import APIRouter, HTTPException, Request, status ,Depends
from typing import Any
from src.services.orginizations import OrginizationsService
from src.schemas.organizations import OrganizationResponse
from fastapi.security import HTTPBearer

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
        print(org)
        return org
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create organization")

@router.get("/get", status_code=status.HTTP_200_OK)
async def get_org(request: Request):
    user = getattr(request.state, "user", None)
    print(user)
    try :
        org = await orgservice.get_organization_by_id(user["id"])
        return org
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to find organization")






