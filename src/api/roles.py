from urllib import request

from fastapi import APIRouter, HTTPException, Request, status ,Depends
from typing import Any
from src.services.orginizations import OrginizationsService
from src.schemas.organizations import OrganizationResponse
from fastapi.security import HTTPBearer
from src.services.roles import RoleService
from src.dependencies.permission import require_permissions


bearer = HTTPBearer()
roleService = RoleService()
router = APIRouter(prefix="/api/roles", tags=["roles"],dependencies=[Depends(bearer)])
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    description="Create a new role for the given organization. Requires `org_id` and `name` of the role.",
    dependencies=[Depends(require_permissions(["role.create", "all"]))],
)
async def create_role(org_id: int, name: str, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        roles = await roleService.create_role(name, org_id)
        return {"message": "success", "roles": roles}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ✅ Get all roles for a given organization
@router.get(
    "/{org_id}/roles",
    status_code=status.HTTP_200_OK,
    description="Get all roles for the given organization.",
    dependencies=[Depends(require_permissions(["role.view", "role.admin", "all"]))],
)
async def get_all_roles(org_id: int, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        roles = await roleService.get_role_list(org_id)
        return {"message": "success", "roles": roles}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ✅ Get all permissions (available system-wide)
@router.get(
    "/permissions",
    status_code=status.HTTP_200_OK,
    description="Get all permissions list.",
    dependencies=[Depends(require_permissions(["role.view_permissions", "role.admin", "all"]))],
)
async def get_all_permissions(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    try:
        permissions = await roleService.get_all_permissions()
        return {"message": "success", "permissions": permissions}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ✅ Add permission to a role
@router.get(
    "/{role_id}/permissions/{permission_name}",
    status_code=status.HTTP_200_OK,
    description="Add a permission to the given role.",
    dependencies=[Depends(require_permissions(["role.assign_permission", "role.admin", "all"]))],
)
async def add_permission_to_role(role_id: int, permission_name: str, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    try:
        result = await roleService.add_role_permission(role_id, permission_name)
        return {
            "message": "success",
            "role_id": role_id,
            "permission_name": permission_name,
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ✅ Get all role-permission mappings in an organization
@router.get(
    "/{org_id}/permissions",
    status_code=status.HTTP_200_OK,
    description="Get all roles with their permissions for the given organization.",
    dependencies=[Depends(require_permissions(["role.view_permissions", "role.admin", "all"]))],
)
async def get_all_role_permissions(org_id: int, request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    try:
        permissions = await roleService.get_all_role_permissions(org_id)
        return {"message": "success", "permissions": permissions}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
