from urllib import request

from fastapi import APIRouter, HTTPException, Request, status ,Depends
from typing import Any
from src.services.orginizations import OrginizationsService
from src.schemas.organizations import OrganizationResponse
from fastapi.security import HTTPBearer
from src.services.roles import RoleService

bearer = HTTPBearer()
roleService = RoleService()
router = APIRouter(prefix="/api/roles", tags=["roles"],dependencies=[Depends(bearer)])

@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_role(org_id:int,name:str,request: Request):

        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        try :
            roles = await roleService.create_role(name,org_id)
            return {
                "message": "success",
                "roles": roles
            }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{org_id}/roles",status_code=status.HTTP_200_OK)
async def get_all_roles(org_id:int,request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        roles = await roleService.get_role_list(org_id)
        return {
            "message": "success",
            "roles": roles
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

