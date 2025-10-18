from fastapi import APIRouter, HTTPException, Request, status, Depends, Query
from fastapi.security import HTTPBearer
from src.services.labels import LabelsService
from src.schemas.labels import LabelCreate, LabelUpdate, LabelResponse, IssueLabelAssignment, IssueLabelResponse
from typing import List

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Labels"], dependencies=[Depends(bearer)])

labels_service = LabelsService()


# Project Label Endpoints
@router.post("/projects/{project_id}/labels", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
async def create_project_label(project_id: int, label_data: LabelCreate, request: Request):
    """Create a new label for a project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        label = await labels_service.create_label(project_id, label_data)
        return label
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create label")


@router.get("/projects/{project_id}/labels", response_model=List[LabelResponse], status_code=status.HTTP_200_OK)
async def get_project_labels(project_id: int, request: Request):
    """Get all labels for a specific project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        labels = await labels_service.get_project_labels(project_id)
        return labels
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch project labels")


@router.get("/labels/{label_id}", response_model=LabelResponse, status_code=status.HTTP_200_OK)
async def get_label(label_id: int, request: Request):
    """Get a specific label by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        label = await labels_service.get_label_by_id(label_id)
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        return label
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch label")


@router.put("/labels/{label_id}", response_model=LabelResponse, status_code=status.HTTP_200_OK)
async def update_label(label_id: int, label_data: LabelUpdate, request: Request):
    """Update an existing label"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        label = await labels_service.update_label(label_id, label_data)
        return label
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update label")


@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(label_id: int, request: Request):
    """Delete a label"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await labels_service.delete_label(label_id)
        return None
    except ValueError as ve:
        if "not found" in str(ve).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete label")


# Issue Label Endpoints
@router.post("/issues/{issue_id}/labels", response_model=IssueLabelResponse, status_code=status.HTTP_201_CREATED)
async def add_label_to_issue(issue_id: int, label_assignment: IssueLabelAssignment, request: Request):
    """Add a label to an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await labels_service.add_label_to_issue(issue_id, label_assignment.label_id)
        
        # Get the label details to return
        label = await labels_service.get_label_by_id(label_assignment.label_id)
        if not label:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
        
        return IssueLabelResponse(
            issue_id=issue_id,
            label_id=label.id,
            label_name=label.name,
            label_color=label.color
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add label to issue")


@router.delete("/issues/{issue_id}/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_label_from_issue(issue_id: int, label_id: int, request: Request):
    """Remove a label from an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await labels_service.remove_label_from_issue(issue_id, label_id)
        return None
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove label from issue")


@router.get("/issues/{issue_id}/labels", response_model=List[IssueLabelResponse], status_code=status.HTTP_200_OK)
async def get_issue_labels(issue_id: int, request: Request):
    """Get all labels for a specific issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        labels = await labels_service.get_issue_labels(issue_id)
        return labels
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issue labels")


# Additional utility endpoints
@router.get("/projects/{project_id}/labels/{label_id}/issues", status_code=status.HTTP_200_OK)
async def get_issues_by_label(project_id: int, label_id: int, request: Request):
    """Get all issues with a specific label in a project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        issues = await labels_service.get_issues_by_label(project_id, label_id)
        return issues
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch issues by label")
