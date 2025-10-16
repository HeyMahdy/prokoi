from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SkillResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserSkillCreate(BaseModel):
    skill_id: int
    proficiency_level: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE

class UserSkillUpdate(BaseModel):
    proficiency_level: ProficiencyLevel

class UserSkillResponse(BaseModel):
    user_id: int
    skill_id: int
    skill_name: str
    proficiency_level: ProficiencyLevel
    created_at: datetime

    class Config:
        from_attributes = True

class UserSkillsListResponse(BaseModel):
    user_id: int
    skills: List[UserSkillResponse]
    total_skills: int
