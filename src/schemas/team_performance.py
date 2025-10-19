from pydantic import BaseModel
from typing import Optional

class TeamPerformanceResponse(BaseModel):
    team_id: int
    team_name: str
    organization_name: str
    
    # Team composition metrics
    team_members: int
    workspaces_assigned: int
    projects_assigned: int
    
    # Work metrics
    total_issues_worked: int
    total_story_points_worked: int
    completed_issues: int
    team_completion_rate: float
    
    # Performance metrics
    team_velocity: Optional[float] = None
    avg_issue_resolution_time: Optional[float] = None
    
    # Collaboration metrics
    team_comments: int
    team_activities: int
    
    class Config:
        from_attributes = True
