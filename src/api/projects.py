from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.projects import ProjectsService
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Projects"], dependencies=[Depends(bearer)])

projectsService = ProjectsService()

@router.post("/workspaces/{workspace_id}/projects", status_code=status.HTTP_201_CREATED)
async def create_project(workspace_id: int, name: str, status: str = 'active', request: Request = None):
    """Create project in workspace"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        project = await projectsService.create_project(workspace_id, name, user["id"], status)
        return project
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create project")

@router.get("/workspaces/{workspace_id}/projects")
async def list_workspace_projects(workspace_id: int, request: Request):
    """List all projects in workspace"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        projects = await projectsService.get_workspace_projects(workspace_id, user["id"])
        return projects
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get workspace projects")

@router.put("/projects/{project_id}/status")
async def update_project_status(project_id: int, status: str, request: Request):
    """Update project status"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        project = await projectsService.update_project_status(project_id, status, user["id"])
        return project
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Project not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update project status")