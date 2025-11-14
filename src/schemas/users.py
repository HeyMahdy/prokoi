from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    jobseeker = "jobseeker"
    recruiter = "recruiter"

class ExperienceLevel(str, Enum):
    fresher = "Fresher"
    junior = "Junior"
    mid = "Mid"
    senior = "Senior"

class BaseUserSchema(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)

class UserSchema(BaseUserSchema):
    password_hash: str = Field(..., min_length=1)
    role: UserRole = UserRole.jobseeker
    education_level: Optional[str] = None
    department: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    preferred_track: Optional[str] = None
    is_new_to_job_market: Optional[bool] = False
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    education_level: Optional[str] = None
    department: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    preferred_track: Optional[str] = None
    is_new_to_job_market: Optional[bool] = None
    is_active: Optional[bool] = None

class UserResponse(BaseUserSchema):
    id: str
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    role: UserRole
    education_level: Optional[str] = None
    department: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    preferred_track: Optional[str] = None
    is_new_to_job_market: bool
    is_active: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str