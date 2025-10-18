from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VelocityUpdate(BaseModel):
    avg_hours_per_point: Optional[float] = None

class VelocityResponse(BaseModel):
    team_id: int
    project_id: int
    avg_hours_per_point: Optional[float] = None
    created_at: datetime
    updated_at: datetime



class TeamVelocityHistory(BaseModel):
    team_id: int
    team_name: str
    project_id: int
    project_name: str
    avg_hours_per_point: Optional[float] = None
    created_at: datetime
    updated_at: datetime


