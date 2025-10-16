from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class SprintStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class SprintCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    goal: Optional[str] = None
    velocity_target: Optional[int] = None

class SprintUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[SprintStatus] = None
    goal: Optional[str] = None
    velocity_target: Optional[int] = None

class SprintResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: SprintStatus
    goal: Optional[str] = None
    velocity_target: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
