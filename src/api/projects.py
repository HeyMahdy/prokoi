from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.projects import ProjectsService
from src.services.velocity import VelocityService
from src.schemas.velocity import VelocityUpdate, VelocityResponse
from fastapi.security import HTTPBearer
from src.services.view import View
from src.dependencies.permission import require_permissions
bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Projects"], dependencies=[Depends(bearer)])

projectsService = ProjectsService()
velocityService = VelocityService()
view = View()

@router.post("/workspaces/{workspace_id}/projects", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions(["all", "create_project"]))])
async def create_project(workspace_id: int, name: str, request: Request, decision: str = 'active'):
    """Create project in workspace"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        project = await projectsService.create_project(workspace_id, name, user["id"], decision)
        return project
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create project")

@router.get("/workspaces/{workspace_id}/projects", dependencies=[Depends(require_permissions(["all", "view_project"]))])
async def list_workspace_projects(workspace_id: int, request: Request):
    """List all projects in workspace"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = []
        projects = await projectsService.get_workspace_projects(workspace_id, user["id"])
        for project in projects:
            if(await view.can_view_workspace_projects(project["id"], user["id"])):
                result.append(project)
        return projects
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get workspace projects")

@router.get("/organizations/{organization_id}/projects")
async def list_organization_projects(organization_id: int, request: Request):
    """List all projects in an organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        projects = await projectsService.get_organization_projects(organization_id, user["id"])
        return projects
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get organization projects")

@router.put("/projects/{project_id}/decision", dependencies=[Depends(require_permissions(["all", "update_project_status"]))])
async def update_project_status(project_id: int, decision: str, request: Request):
    """Update project status"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        project = await projectsService.update_project_status(project_id, decision, user["id"])
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

@router.post("/projects/{project_id}/teams", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions(["all", "assign_team_to_project"]))])
async def assign_team_to_project(project_id: int, team_id: int, request: Request):
    """Assign team to project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        assignment = await projectsService.assign_team_to_project(project_id, team_id, user["id"])
        return assignment
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "already assigned" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        elif "Project not found" in str(e) or "Team not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to assign team to project")

@router.get("/projects/{project_id}/teams", dependencies=[Depends(require_permissions(["all", "view_project_teams"]))])
async def list_project_teams(project_id: int, request: Request):
    """List all teams assigned to project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        teams = await projectsService.get_project_teams(project_id, user["id"])
        return teams
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Project not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get project teams")

@router.get("/projects/{project_id}/users", dependencies=[Depends(require_permissions(["all", "view_project_users"]))])
async def list_project_users(project_id: int, request: Request):
    """List all users assigned to project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        users = await projectsService.get_project_users(project_id, user["id"])
        return users
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Project not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get project users")

@router.get("/projects/{project_id}/team-members", dependencies=[Depends(require_permissions(["all", "view_team_members"]))])
async def list_project_team_members(project_id: int, request: Request):
    """List all team members assigned to project through teams"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        team_members = await projectsService.get_project_team_members(project_id, user["id"])
        return team_members
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Project not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get project team members")

@router.get("/projects/{project_id}/teams/{team_id}/velocity", response_model=VelocityResponse, dependencies=[Depends(require_permissions(["all", "view_team_velocity"]))])
async def get_team_project_velocity(project_id: int, team_id: int, request: Request):
    """Get team velocity for specific project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        velocity = await velocityService.get_team_project_velocity(team_id, project_id, user["id"])
        return velocity
    except Exception as e:
        if "Access denied" in str(e) or "Team is not assigned" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get team project velocity")

@router.put("/projects/{project_id}/teams/{team_id}/velocity", response_model=VelocityResponse, dependencies=[Depends(require_permissions(["all", "edit_team_velocity"]))])
async def update_team_project_velocity(project_id: int, team_id: int, velocity_data: VelocityUpdate, request: Request):
    """Update team velocity for specific project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        velocity = await velocityService.update_team_project_velocity(team_id, project_id, velocity_data, user["id"])
        return velocity
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e) or "Team is not assigned" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update team project velocity")