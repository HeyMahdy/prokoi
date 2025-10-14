from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer
from src.services.issue_types import IssueTypesService
from src.schemas.issue_types import IssueTypeCreate, IssueTypeResponse
from typing import List

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Issue Types"], dependencies=[Depends(bearer)])

issue_types_service = IssueTypesService()


@router.get("/issue-types", response_model=List[IssueTypeResponse], status_code=status.HTTP_200_OK)
async def get_issue_types(request: Request):
    """Get all default issue types"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue_types = await issue_types_service.get_all_issue_types()
        return issue_types
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issue types")


@router.post("/organizations/{org_id}/issue-types", response_model=IssueTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_organization_issue_type(org_id: int, issue_type_data: IssueTypeCreate, request: Request):
    """Create custom issue type for organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        # Note: Since the current table structure doesn't support organization_id,
        # this endpoint will create a global issue type for now
        # In a future enhancement, you could modify the table to support organization-specific types
        issue_type = await issue_types_service.create_issue_type(issue_type_data)
        return issue_type
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create issue type")


@router.get("/issue-types/{issue_type_id}", response_model=IssueTypeResponse, status_code=status.HTTP_200_OK)
async def get_issue_type(issue_type_id: int, request: Request):
    """Get a specific issue type by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue_type = await issue_types_service.get_issue_type_by_id(issue_type_id)
        if not issue_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue type not found")
        return issue_type
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issue type")


@router.put("/issue-types/{issue_type_id}", response_model=IssueTypeResponse, status_code=status.HTTP_200_OK)
async def update_issue_type(issue_type_id: int, issue_type_data: IssueTypeCreate, request: Request):
    """Update an existing issue type"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issue_type = await issue_types_service.update_issue_type(issue_type_id, issue_type_data)
        return issue_type
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update issue type")


@router.delete("/issue-types/{issue_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue_type(issue_type_id: int, request: Request):
    """Delete an issue type"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await issue_types_service.delete_issue_type(issue_type_id)
        return None
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete issue type")
