from pydantic import BaseModel
from typing import Optional
from datetime import date

class SprintVelocityResponse(BaseModel):
    sprint_id: int
    sprint_name: str
    project_name: str
    start_date: date
    end_date: date
    status: str
    velocity_target: Optional[int] = None
    
    # Sprint content metrics
    issues_in_sprint: int
    total_story_points: int
    completed_issues: int
    completed_story_points: int
    
    # Velocity metrics
    avg_hours_per_point: Optional[float] = None
    velocity_achievement_percentage: float
    
    # Sprint timing
    sprint_duration_days: int
    sprint_status: str  # completed, active, upcoming
    
    class Config:
        from_attributes = True
