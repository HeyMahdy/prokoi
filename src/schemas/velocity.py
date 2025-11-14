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


class JobCreate(BaseModel):
    title: str 
    company: str 
    location: str 
    experience_required: str
    job_type: str 
    description: str 
    

class ResourceCreate(BaseModel):
    title: str
    platform: str
    url: str
    cost: str  # keep it simple, can be "Free" or price string


class ExperienceUpdate(BaseModel):
    title: str
    description: str