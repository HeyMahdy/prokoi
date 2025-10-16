from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IssueAddToSprint(BaseModel):
    issue_ids: List[int]

class SprintIssueResponse(BaseModel):
    issue_id: int
    sprint_id: int
    added_at: datetime
    # Issue details
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    story_points: Optional[int] = None
    type_name: Optional[str] = None
    created_by: Optional[int] = None
    created_by_name: Optional[str] = None

    class Config:
        from_attributes = True

class SprintBacklogReorder(BaseModel):
    issue_ids: List[int]  # Ordered list of issue IDs

class SprintIssueSummary(BaseModel):
    total_issues: int
    total_story_points: Optional[int] = None
    issues_by_status: dict[str, int] = {}
    issues_by_priority: dict[str, int] = {}
