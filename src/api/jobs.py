from fastapi import APIRouter, HTTPException, Request, Depends,status as fastapi_status
from src.services.jobs import JobsService
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from fastapi.security import HTTPBearer

# Pydantic models for request/response
class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    is_remote: bool = False
    recommended_experience: str
    job_type: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    recommended_experience: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    is_active: Optional[bool] = None

class JobResponse(BaseModel):
    id: str
    recruiter_id: str
    title: str
    company: str
    location: str
    is_remote: bool
    recommended_experience: str
    job_type: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[datetime] = None
    posted_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

class JobApplicationCreate(BaseModel):
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None

class JobApplicationResponse(BaseModel):
    id: str
    job_id: str
    user_id: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: str
    applied_at: datetime
    reviewed_at: Optional[datetime] = None
    notes: Optional[str] = None

# Initialize service
jobs_service = JobsService()
bearer = HTTPBearer()
# Create router without bearer dependency
router = APIRouter(prefix="/api/jobs", tags=["jobs"],dependencies=[Depends(bearer)])

# Job endpoints
@router.post("/", status_code=fastapi_status.HTTP_201_CREATED)
async def create_job(job_data: JobCreate, request: Request):
    """Create a new job posting"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can post jobs")
    
    try:
        job = await jobs_service.create_job(
            recruiter_id=user["id"],
            title=job_data.title,
            company=job_data.company,
            location=job_data.location,
            is_remote=job_data.is_remote,
            recommended_experience=job_data.recommended_experience,
            job_type=job_data.job_type,
            description=job_data.description,
            requirements=job_data.requirements,
            responsibilities=job_data.responsibilities,
            salary_range=job_data.salary_range,
            application_deadline=job_data.application_deadline.isoformat() if job_data.application_deadline else None
        )
        return job
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get job by ID"""
    try:
        job = await jobs_service.get_job_by_id(job_id)
        return job
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{job_id}")
async def update_job(job_id: str, job_data: JobUpdate, request: Request):
    """Update job by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can update jobs")
    
    try:
        job = await jobs_service.get_job_by_id(job_id)
        if job["recruiter_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this job")
            
        job = await jobs_service.update_job(
            job_id=job_id,
            recruiter_id=user["id"],
            **job_data.dict(exclude_unset=True)
        )
        return job
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{job_id}")
async def delete_job(job_id: str, request: Request):
    """Delete job by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can delete jobs")
    
    try:
        job = await jobs_service.get_job_by_id(job_id)
        if job["recruiter_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this job")
            
        result = await jobs_service.delete_job(job_id=job_id, recruiter_id=user["id"])
        return {"message": "Job deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
async def search_jobs(
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    is_remote: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0
):
    """Search jobs with filters"""
    try:
        jobs = await jobs_service.search_jobs(
            search_term=search_term,
            location=location,
            job_type=job_type,
            is_remote=is_remote,
            limit=limit,
            offset=offset
        )
        return jobs
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

# Job Skills endpoints
@router.post("/{job_id}/skills/{skill_id}")
async def add_job_skill(job_id: str, skill_id: str, request: Request):
    """Add a skill requirement to a job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can manage job skills")
    
    try:
        job = await jobs_service.get_job_by_id(job_id)
        if job["recruiter_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="You don't have permission to manage this job's skills")
            
        result = await jobs_service.add_skill_to_job(
            job_id=job_id,
            recruiter_id=user["id"],
            skill_id=skill_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{job_id}/skills/{skill_id}")
async def remove_job_skill(job_id: str, skill_id: str, request: Request):
    """Remove a skill requirement from a job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can manage job skills")
    
    try:
        job = await jobs_service.get_job_by_id(job_id)
        if job["recruiter_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="You don't have permission to manage this job's skills")
            
        result = await jobs_service.remove_skill_from_job(
            job_id=job_id,
            recruiter_id=user["id"],
            skill_id=skill_id
        )
        return {"message": "Skill removed from job successfully"}
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{job_id}/skills")
async def get_job_skills(job_id: str):
    """Get all skills for a job"""
    try:
        skills = await jobs_service.get_job_skills(job_id)
        return skills
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

# Job Applications endpoints
@router.post("/{job_id}/apply")
async def apply_for_job(job_id: str, application_data: JobApplicationCreate, request: Request):
    """Apply for a job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a jobseeker
    if user.get("role") != "jobseeker":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only jobseekers can apply for jobs")
    
    try:
        application = await jobs_service.apply_to_job(
            job_id=job_id,
            user_id=user["id"],
            cover_letter=application_data.cover_letter,
            resume_url=application_data.resume_url
        )
        return application
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/applications/my")
async def get_my_applications(request: Request):
    """Get all applications for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        applications = await jobs_service.get_applications_by_user(user["id"])
        return applications
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{job_id}/applications")
async def get_job_applications(job_id: str, request: Request):
    """Get all applications for a job (recruiter only)"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can view job applications")
    
    try:
        job = await jobs_service.get_job_by_id(job_id)
        if job["recruiter_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="You don't have permission to view applications for this job")
            
        applications = await jobs_service.get_applications_by_job(job_id=job_id, recruiter_id=user["id"])
        return applications
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/applications/{application_id}/status")
async def update_application_status(application_id: str, status: str, request: Request, notes: Optional[str] = None):
    """Update application status (recruiter only)"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Check if user is a recruiter
    if user.get("role") != "recruiter":
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Only recruiters can update application status")
    
    try:
        application = await jobs_service.get_application_by_id(application_id=application_id, user_id=user["id"])
        # Get the job to verify ownership
        job = await jobs_service.get_job_by_id(application["job_id"])
        if job["recruiter_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this application")
            
        application = await jobs_service.update_application_status(
            application_id=application_id,
            recruiter_id=user["id"],
            status=status,
            notes=notes
        )
        return application
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))