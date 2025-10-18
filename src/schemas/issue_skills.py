from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class IssueSkillRequirementCreate(BaseModel):
    skill_id: int
    required_level: ProficiencyLevel

class IssueSkillRequirementUpdate(BaseModel):
    required_level: ProficiencyLevel

class IssueSkillRequirementResponse(BaseModel):
    issue_id: int
    skill_id: int
    skill_name: str
    required_level: ProficiencyLevel
    created_at: datetime

    class Config:
        from_attributes = True

class IssueSkillsListResponse(BaseModel):
    issue_id: int
    total_skills: int
    skills: List[IssueSkillRequirementResponse]

class SkillMatchResponse(BaseModel):
    skill_id: int
    skill_name: str
    required_level: ProficiencyLevel
    user_level: Optional[ProficiencyLevel]
    is_match: bool
    gap: Optional[str]  # "overqualified", "underqualified", "perfect_match"
