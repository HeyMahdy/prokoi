from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProjectUser(BaseModel):
    user_id: int
    user_name: str

class ProjectTeam(BaseModel):
    team_id: int
    team_name: str

class ProjectAnalysisDepthResponse(BaseModel):
    project_id: int
    project_name: str
    project_status: str
    workspace_name: str
    organization_name: str
    
    # User and Team metrics
    total_users: int
    total_teams: int
    project_users: List[ProjectUser] = []
    project_teams: List[ProjectTeam] = []
    
    # Issue metrics
    total_issues: int
    open_issues: int
    in_progress_issues: int
    completed_issues: int
    high_priority_issues: int
    critical_issues: int
    
    # Sprint metrics
    total_sprints: int
    active_sprints: int
    
    # Time tracking metrics
    avg_hours_per_log: float
    avg_team_velocity: float
    
    # Activity metrics
    total_comments: int
    recent_activity: int  # Issues updated in last 7 days
    
    # Story points metrics
    total_story_points: int
    avg_story_points: float
    
    class Config:
        from_attributes = True
