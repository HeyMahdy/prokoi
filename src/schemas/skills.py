from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProficiencyLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class SkillCategory(str, Enum):
    TECHNICAL = "Technical"
    SOFT_SKILL = "Soft Skill"
    DESIGN = "Design"
    BUSINESS = "Business"

class SkillCreate(BaseModel):
    name: str
    category: SkillCategory
    description: Optional[str] = None

class SkillResponse(BaseModel):
    id: str
    name: str
    category: SkillCategory
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserSkillCreate(BaseModel):
    skill_id: str
    proficiency_level: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE

class UserSkillUpdate(BaseModel):
    proficiency_level: ProficiencyLevel

class UserSkillResponse(BaseModel):
    id: str
    user_id: str
    skill_id: str
    skill_name: str
    proficiency_level: ProficiencyLevel
    verified: bool
    verification_score: Optional[int] = None
    verification_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserSkillsListResponse(BaseModel):
    user_id: str
    skills: List[UserSkillResponse]
    total_skills: int

class UserExperienceType(str, Enum):
    PROJECT = "Project"
    WORK = "Work"
    INTERNSHIP = "Internship"
    FREELANCE = "Freelance"
    VOLUNTEER = "Volunteer"

class UserExperienceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: UserExperienceType
    company: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: bool = False

class UserExperienceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[UserExperienceType] = None
    company: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None

class UserExperienceResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    type: UserExperienceType
    company: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserExperiencesListResponse(BaseModel):
    user_id: str
    experiences: List[UserExperienceResponse]
    total_experiences: int