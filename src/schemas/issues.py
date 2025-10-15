from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IssueBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    story_points: Optional[int] = Field(None, ge=0)
    status: str = Field(default="open", max_length=50)
    priority: str = Field(default="medium", max_length=50)
    parent_issue_id: Optional[int] = None


class IssueCreate(IssueBase):
    project_id: int = Field(..., gt=0)
    type_id: Optional[int] = Field(None, gt=0)


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    story_points: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, max_length=50)
    type_id: Optional[int] = Field(None, gt=0)
    parent_issue_id: Optional[int] = None


class IssueResponse(BaseModel):
    id: int
    project_id: int
    type_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    story_points: Optional[int] = None
    status: str
    priority: str
    created_by: Optional[int] = None
    parent_issue_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Issue Assignment Schemas
class IssueAssignmentCreate(BaseModel):
    assigned_to: int = Field(..., gt=0, description="User ID to assign the issue to")
    



class IssueAssignmentResponse(BaseModel):
    id: int
    issue_id: int
    assigned_to: int
    assigned_by: int
    assigned_at: datetime
    assigned_to_name: Optional[str] = None
    assigned_to_email: Optional[str] = None
    assigned_by_name: Optional[str] = None
    assigned_by_email: Optional[str] = None


class IssueStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1, max_length=50)
    
    class Config:
        # Common status values for validation
        schema_extra = {
            "example": {
                "status": "open"
            }
        }


class IssueWithAssignment(IssueResponse):
    assignment: Optional[IssueAssignmentResponse] = None


