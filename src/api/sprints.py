from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.sprints import SprintsService
from src.schemas.sprints import SprintCreate, SprintUpdate, SprintResponse
from src.schemas.sprint_planning import IssueAddToSprint, SprintIssueResponse, SprintBacklogReorder
from fastapi.security import HTTPBearer
from src.dependencies.permission import require_permissions

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Sprints"], dependencies=[Depends(bearer)])

sprintsService = SprintsService()

@router.post("/projects/{project_id}/sprints", response_model=SprintResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions(["all", "create_sprint"]))])
async def create_sprint(project_id: int, sprint_data: SprintCreate, request: Request):
    """Create sprint in project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint = await sprintsService.create_sprint(project_id, sprint_data, user["id"])
        return sprint
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create sprint")

@router.get("/projects/{project_id}/sprints", response_model=list[SprintResponse], dependencies=[Depends(require_permissions(["all", "view_sprint"]))])
async def list_project_sprints(project_id: int, request: Request):
    """List all sprints in project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprints = await sprintsService.get_project_sprints(project_id, user["id"])
        return sprints
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get project sprints")

@router.get("/sprints/{sprint_id}", response_model=SprintResponse, dependencies=[Depends(require_permissions(["all", "view_sprint"]))])
async def get_sprint_details(sprint_id: int, request: Request):
    """Get sprint details"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint = await sprintsService.get_sprint_by_id(sprint_id, user["id"])
        return sprint
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get sprint details")

@router.put("/sprints/{sprint_id}", response_model=SprintResponse, dependencies=[Depends(require_permissions(["all", "edit_sprint"]))])
async def update_sprint(sprint_id: int, sprint_data: SprintUpdate, request: Request):
    """Update sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint = await sprintsService.update_sprint(sprint_id, sprint_data, user["id"])
        return sprint
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update sprint")

@router.delete("/sprints/{sprint_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permissions(["all", "delete_sprint"]))])
async def delete_sprint(sprint_id: int, request: Request):
    """Delete sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await sprintsService.delete_sprint(sprint_id, user["id"])
        return None
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete sprint")

@router.post("/sprints/{sprint_id}/start", response_model=SprintResponse, dependencies=[Depends(require_permissions(["all", "start_sprint"]))])
async def start_sprint(sprint_id: int, request: Request):
    """Start sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint = await sprintsService.start_sprint(sprint_id, user["id"])
        return sprint
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to start sprint")

@router.post("/sprints/{sprint_id}/complete", response_model=SprintResponse, dependencies=[Depends(require_permissions(["all", "complete_sprint"]))])
async def complete_sprint(sprint_id: int, request: Request):
    """Complete sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint = await sprintsService.complete_sprint(sprint_id, user["id"])
        return sprint
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to complete sprint")

@router.post("/sprints/{sprint_id}/cancel", response_model=SprintResponse, dependencies=[Depends(require_permissions(["all", "cancel_sprint"]))])
async def cancel_sprint(sprint_id: int, request: Request):
    """Cancel sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint = await sprintsService.cancel_sprint(sprint_id, user["id"])
        return sprint
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to cancel sprint")

@router.post("/sprints/{sprint_id}/issues", dependencies=[Depends(require_permissions(["all", "add_issue_to_sprint"]))])
async def add_issues_to_sprint(sprint_id: int, issue_data: IssueAddToSprint, request: Request):
    """Add issues to sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = await sprintsService.add_issues_to_sprint(sprint_id, issue_data, user["id"])
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add issues to sprint")

@router.delete("/sprints/{sprint_id}/issues/{issue_id}", dependencies=[Depends(require_permissions(["all", "remove_issue_from_sprint"]))])
async def remove_issue_from_sprint(sprint_id: int, issue_id: int, request: Request):
    """Remove issue from sprint"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = await sprintsService.remove_issue_from_sprint(sprint_id, issue_id, user["id"])
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove issue from sprint")

@router.get("/sprints/{sprint_id}/issues", response_model=list[SprintIssueResponse], dependencies=[Depends(require_permissions(["all", "view_sprint_issues"]))])
async def get_sprint_issues(sprint_id: int, request: Request):
    """List sprint issues"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issues = await sprintsService.get_sprint_issues(sprint_id, user["id"])
        return issues
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get sprint issues")

@router.put("/sprints/{sprint_id}/issues/reorder", dependencies=[Depends(require_permissions(["all", "reorder_sprint_backlog"]))])
async def reorder_sprint_backlog(sprint_id: int, reorder_data: SprintBacklogReorder, request: Request):
    """Reorder sprint backlog"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        result = await sprintsService.reorder_sprint_backlog(sprint_id, reorder_data, user["id"])
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "Sprint not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to reorder sprint backlog")
