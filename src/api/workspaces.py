from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.workspaces import WorkspacesService
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Workspaces"], dependencies=[Depends(bearer)])

workspacesService = WorkspacesService()

@router.post("/organizations/{org_id}/workspaces", status_code=status.HTTP_201_CREATED)
async def create_workspace(org_id: int, name: str, request: Request = None):
    """Create workspace in organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        workspace = await workspacesService.create_workspace(org_id, name, user["id"])
        return workspace
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create workspace")

@router.get("/organizations/{org_id}/workspaces")
async def list_organization_workspaces(org_id: int, request: Request):
    """List all workspaces in organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        workspaces = await workspacesService.get_organization_workspaces(org_id, user["id"])
        return workspaces
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get workspaces")