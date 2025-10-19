from pydantic import BaseModel
from typing import Optional

class UserPerformanceResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    organization_name: str
    
    # Issue assignment metrics
    assigned_issues: int
    completed_issues: int
    open_issues: int
    completion_rate: float
    
    # Story points metrics
    total_story_points_assigned: int
    completed_story_points: int
    avg_story_points_per_issue: float
    
    # Activity metrics
    comments_made: int
    activities_logged: int
    
    # Workload metrics
    weekly_hours: Optional[int] = None
    total_hours_spent: Optional[float] = None
    
    # User tenure
    days_since_joined: int
    
    class Config:
        from_attributes = True
