from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.skills import AppService
from src.schemas.skills import SkillResponse, UserSkillCreate, UserSkillUpdate, UserSkillResponse, UserSkillsListResponse
from src.schemas.velocity import JobCreate , ResourceCreate , ExperienceUpdate
from fastapi.security import HTTPBearer
from src.dependencies.permission import require_permissions

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Skills"], dependencies=[Depends(bearer)])

skillsService = AppService()

@router.get("/skills")
async def get_all_skills(request: Request):
    """Get all global skills"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        skills = await skillsService.get_all_skills()
        return skills
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/skills/{skill_id}")
async def get_skill_by_id(skill_id: int, request: Request):
    """Get skill by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        skill = await skillsService.get_skill_by_id(skill_id)
        return skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/skills")
async def create_skill(skill_data: UserSkillCreate, request: Request):
    """Create a new skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        skill = await skillsService.create_skill(skill_data.name)
        return skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ===========================================================
# USER SKILLS ENDPOINTS
# ===========================================================

@router.get("/users/{user_id}/skills")
async def get_user_skills(user_id: int, request: Request):
    """Get all skills for a user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_user_skills(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/users/{user_id}/skills/{skill_id}")
async def get_user_skill(user_id: int, skill_id: int, request: Request):
    """Get specific user skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        user_skill = await skillsService.get_user_skill(user_id, skill_id)
        return user_skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/users/{user_id}/skills/{skill_id}")
async def add_skill_to_user(user_id: int, skill_id: int, request: Request):
    """Add skill to user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        user_skill = await skillsService.add_skill_to_user(user_id, skill_id)
        return user_skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/users/{user_id}/skills/{skill_id}")
async def remove_user_skill(user_id: int, skill_id: int, request: Request):
    """Remove skill from user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.remove_user_skill(user_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ===========================================================
# JOBS ENDPOINTS
# ===========================================================

@router.get("/jobs")
async def get_all_jobs(request: Request, limit: int = 100, offset: int = 0):
    """Get all jobs with pagination"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_all_jobs(limit, offset)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/jobs/{job_id}")
async def get_job_by_id(job_id: int, request: Request):
    """Get job by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        job = await skillsService.get_job_by_id(job_id)
        return job
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/jobs")
async def create_job(job_data: JobCreate, request: Request):
    """Create a new job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        job = await skillsService.create_job(
            job_data.title,
            job_data.company,
            job_data.location,
            job_data.experience_required,
            job_data.job_type,
            job_data.description
        )
        return job
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/jobs/search/by-title")
async def search_jobs_by_title(title: str, request: Request):
    """Search jobs by title"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.search_jobs_by_title(title)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/jobs/type/{job_type}")
async def get_jobs_by_type(job_type: str, request: Request):
    """Get jobs by type"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_jobs_by_type(job_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ===========================================================
# JOB REQUIRED SKILLS ENDPOINTS
# ===========================================================

@router.get("/jobs/{job_id}/skills")
async def get_job_required_skills(job_id: int, request: Request):
    """Get all required skills for a job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_job_required_skills(job_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/jobs/{job_id}/skills/{skill_id}")
async def add_required_skill_to_job(job_id: int, skill_id: int, request: Request):
    """Add required skill to job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.add_required_skill_to_job(job_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/jobs/{job_id}/skills/{skill_id}")
async def remove_required_skill_from_job(job_id: int, skill_id: int, request: Request):
    """Remove required skill from job"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.remove_required_skill_from_job(job_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/skills/{skill_id}/jobs")
async def get_jobs_by_skill(skill_id: int, request: Request):
    """Get all jobs requiring a specific skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_jobs_by_skill(skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/users/{user_id}/matching-jobs")
async def get_matching_jobs_for_user(user_id: int, request: Request):
    """Get jobs that match user's skills"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_matching_jobs_for_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ===========================================================
# LEARNING RESOURCES ENDPOINTS
# ===========================================================

@router.get("/resources")
async def get_all_resources(request: Request, limit: int = 100, offset: int = 0):
    """Get all learning resources with pagination"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_all_resources(limit, offset)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/resources/{resource_id}")
async def get_resource_by_id(resource_id: int, request: Request):
    """Get learning resource by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        resource = await skillsService.get_resource_by_id(resource_id)
        return resource
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/resources")
async def create_resource(resource_data: ResourceCreate, request: Request):
    """Create a new learning resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        resource = await skillsService.create_resource(
            resource_data.title,
            resource_data.platform,
            resource_data.url,
            resource_data.cost
        )
        return resource
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/resources/platform/{platform}")
async def get_resources_by_platform(platform: str, request: Request):
    """Get resources by platform"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_resources_by_platform(platform)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/resources/filter/free")
async def get_free_resources(request: Request):
    """Get all free resources"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_free_resources()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ===========================================================
# RESOURCE SKILLS ENDPOINTS
# ===========================================================

@router.get("/resources/{resource_id}/skills")
async def get_resource_skills(resource_id: int, request: Request):
    """Get all skills covered by a resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_resource_skills(resource_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/resources/{resource_id}/skills/{skill_id}")
async def add_skill_to_resource(resource_id: int, skill_id: int, request: Request):
    """Add skill to learning resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.add_skill_to_resource(resource_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/resources/{resource_id}/skills/{skill_id}")
async def remove_skill_from_resource(resource_id: int, skill_id: int, request: Request):
    """Remove skill from learning resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.remove_skill_from_resource(resource_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/skills/{skill_id}/resources")
async def get_resources_by_skill(skill_id: int, request: Request):
    """Get all resources that teach a specific skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_resources_by_skill(skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/users/{user_id}/recommended-resources")
async def get_recommended_resources_for_user(user_id: int, request: Request):
    """Get recommended resources based on skills user doesn't have"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_recommended_resources_for_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ===========================================================
# USER EXPERIENCE ENDPOINTS
# ===========================================================

@router.get("/users/{user_id}/experiences")
async def get_user_experiences(user_id: int, request: Request):
    """Get all experiences for a user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_user_experiences(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/experiences/{experience_id}")
async def get_experience_by_id(experience_id: int, request: Request):
    """Get experience by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        experience = await skillsService.get_experience_by_id(experience_id)
        return experience
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/users/{user_id}/experiences")
async def create_experience(user_id: int, experience_data: ExperienceUpdate, request: Request):
    """Create a new user experience"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        experience = await skillsService.create_experience(
            user_id,
            experience_data.title,
            experience_data.description
        )
        return experience
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/experiences/{experience_id}")
async def update_experience(experience_id: int, experience_data: ExperienceUpdate, request: Request):
    """Update user experience"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        experience = await skillsService.update_experience(
            experience_id,
            experience_data.title,
            experience_data.description
        )
        return experience
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/experiences/{experience_id}")
async def delete_experience(experience_id: int, request: Request):
    """Delete user experience"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.delete_experience(experience_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))