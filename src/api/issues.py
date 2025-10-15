from fastapi import APIRouter, HTTPException, Request, status, Depends, Query
from fastapi.security import HTTPBearer
from src.services.issues import IssuesService
from src.schemas.issues import IssueCreate, IssueUpdate, IssueResponse, IssueAssignmentCreate, IssueAssignmentResponse, IssueStatusUpdate
from typing import List, Optional

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Issues"], dependencies=[Depends(bearer)])

issues_service = IssuesService()


@router.post("/projects/{project_id}/issues", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(project_id: int, issue_data: IssueCreate, request: Request):
    """Create a new issue in a project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    # Override project_id from URL parameter
    issue_data.project_id = project_id

    try:
        issue = await issues_service.create_issue(issue_data, user["id"])
        return issue
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create issue")


@router.get("/projects/{project_id}/issues", response_model=List[IssueResponse], status_code=status.HTTP_200_OK)
async def get_project_issues(
    project_id: int, 
    request: Request,
    Status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    type_id: Optional[int] = Query(None, description="Filter by issue type ID")
):
    """Get all issues for a specific project with optional filters"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    try:
        if Status or priority or type_id:
            # Use filtered search
            issues = await issues_service.get_issues_with_filters(
                project_id, Status, priority, type_id
            )
        else:
            # Get all issues
            issues = await issues_service.get_issues_by_project(project_id)
        
        return issues
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to fetch issues")


@router.get("/issues/{issue_id}", response_model=IssueResponse, status_code=status.HTTP_200_OK)
async def get_issue(issue_id: int, request: Request):
    """Get a specific issue by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not authenticated")

    try:
        issue = await issues_service.get_issue_by_id(issue_id)
        if not issue:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
        return issue
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issue")


@router.put("/issues/{issue_id}", response_model=IssueResponse, status_code=status.HTTP_200_OK)
async def update_issue(issue_id: int, issue_data: IssueUpdate, request: Request):
    """Update an existing issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue = await issues_service.update_issue(issue_id, issue_data)
        return issue
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update issue")


@router.delete("/issues/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(issue_id: int, request: Request):
    """Delete an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await issues_service.delete_issue(issue_id)
        return None
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete issue")


@router.get("/projects/{project_id}/issues/status/{status}", response_model=List[IssueResponse], status_code=status.HTTP_200_OK)
async def get_issues_by_status(project_id: int, Status: str, request: Request):
    """Get all issues with a specific status for a project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issues = await issues_service.get_issues_by_status(project_id, Status)
        return issues
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issues by status")


@router.get("/projects/{project_id}/issues/priority/{priority}", response_model=List[IssueResponse], status_code=status.HTTP_200_OK)
async def get_issues_by_priority(project_id: int, priority: str, request: Request):
    """Get all issues with a specific priority for a project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issues = await issues_service.get_issues_by_priority(project_id, priority)
        return issues
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issues by priority")


@router.get("/issues/{parent_issue_id}/sub-issues", response_model=List[IssueResponse], status_code=status.HTTP_200_OK)
async def get_sub_issues(parent_issue_id: int, request: Request):
    """Get all sub-issues (children) of a parent issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issues = await issues_service.get_sub_issues(parent_issue_id)
        return issues
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch sub-issues")


# Additional utility endpoints
@router.patch("/issues/{issue_id}/status", response_model=IssueResponse, status_code=status.HTTP_200_OK)
async def update_issue_status_patch(issue_id: int, status_data: IssueStatusUpdate, request: Request):
    """Update only the status of an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue = await issues_service.update_issue_status(issue_id, status_data)
        return issue
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update issue status")


@router.patch("/issues/{issue_id}/priority", response_model=IssueResponse, status_code=status.HTTP_200_OK)
async def update_issue_priority(issue_id: int, priority: str, request: Request):
    """Update only the priority of an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue_data = IssueUpdate(priority=priority)
        issue = await issues_service.update_issue(issue_id, issue_data)
        return issue
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update issue priority")


# Issue Assignment endpoints
@router.post("/issues/{issue_id}/assign", response_model=IssueAssignmentResponse, status_code=status.HTTP_200_OK)
async def assign_issue(issue_id: int, assignment_data: IssueAssignmentCreate, request: Request):
    """Assign an issue to a user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        assignment = await issues_service.assign_issue(issue_id, assignment_data, user["id"])
        return assignment
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to assign issue")


@router.post("/issues/{issue_id}/unassign", status_code=status.HTTP_200_OK)
async def unassign_issue(issue_id: int, request: Request):
    """Unassign an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await issues_service.unassign_issue(issue_id)
        return {"message": "Issue unassigned successfully"}
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to unassign issue")


@router.put("/issues/{issue_id}/status", response_model=IssueResponse, status_code=status.HTTP_200_OK)
async def update_issue_status(issue_id: int, status_data: IssueStatusUpdate, request: Request):
    """Update issue status"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue = await issues_service.update_issue_status(issue_id, status_data)
        return issue
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update issue status")


@router.get("/issues/{issue_id}/assignment", response_model=IssueAssignmentResponse, status_code=status.HTTP_200_OK)
async def get_issue_assignment(issue_id: int, request: Request):
    """Get assignment details for an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        assignment = await issues_service.get_issue_assignment(issue_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue is not assigned")
        return assignment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch assignment")


@router.get("/users/{user_id}/assigned-issues", response_model=List[IssueResponse], status_code=status.HTTP_200_OK)
async def get_user_assigned_issues(
    user_id: int, 
    request: Request,
    project_id: Optional[int] = Query(None, description="Filter by project ID")
):
    """Get all issues assigned to a user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issues = await issues_service.get_user_assigned_issues(user_id, project_id)
        return issues
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch assigned issues")
