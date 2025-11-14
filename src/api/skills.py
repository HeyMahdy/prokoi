from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.skills import AppService
from src.schemas.skills import (
    SkillCreate, SkillResponse, UserSkillCreate, UserSkillUpdate, 
    UserSkillResponse, UserSkillsListResponse, UserExperienceCreate,
    UserExperienceUpdate, UserExperienceResponse, UserExperiencesListResponse
)
from src.schemas.velocity import JobCreate, ResourceCreate
from fastapi.security import HTTPBearer
from src.dependencies.permission import require_permissions

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Skills"], dependencies=[Depends(bearer)])

skillsService = AppService()

@router.get("/skills", response_model=list[SkillResponse])
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


@router.get("/skills/{skill_id}", response_model=SkillResponse)
async def get_skill_by_id(skill_id: str, request: Request):
    """Get skill by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        skill = await skillsService.get_skill_by_id(skill_id)
        return skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/skills", response_model=SkillResponse)
async def create_skill(skill_data: SkillCreate, request: Request):
    """Create a new skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        skill = await skillsService.create_skill(
            skill_data.name, 
            skill_data.category.value, 
            skill_data.description
        )
        return skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ===========================================================
# USER SKILLS ENDPOINTS
# ===========================================================

@router.get("/users/{user_id}/skills", response_model=UserSkillsListResponse)
async def get_user_skills(user_id: str, request: Request):
    """Get all skills for a user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_user_skills(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/users/{user_id}/skills/{skill_id}", response_model=UserSkillResponse)
async def get_user_skill(user_id: str, skill_id: str, request: Request):
    """Get specific user skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        user_skill = await skillsService.get_user_skill(user_id, skill_id)
        return user_skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/users/{user_id}/skills/{skill_id}", response_model=UserSkillResponse)
async def add_skill_to_user(user_id: str, skill_id: str, skill_data: UserSkillCreate, request: Request):
    """Add skill to user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        user_skill = await skillsService.add_skill_to_user(
            user_id, skill_id, skill_data.proficiency_level.value
        )
        return user_skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/users/{user_id}/skills/{skill_id}", response_model=UserSkillResponse)
async def update_user_skill(user_id: str, skill_id: str, skill_data: UserSkillUpdate, request: Request):
    """Update user skill proficiency"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        user_skill = await skillsService.update_user_skill(
            user_id, skill_id, skill_data.proficiency_level.value
        )
        return user_skill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/users/{user_id}/skills/{skill_id}")
async def remove_user_skill(user_id: str, skill_id: str, request: Request):
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
# USER EXPERIENCE ENDPOINTS
# ===========================================================

@router.get("/users/{user_id}/experiences", response_model=UserExperiencesListResponse)
async def get_user_experiences(user_id: str, request: Request):
    """Get all experiences for a user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.get_user_experiences(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/experiences/{experience_id}", response_model=UserExperienceResponse)
async def get_experience_by_id(experience_id: str, request: Request):
    """Get experience by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        experience = await skillsService.get_experience_by_id(experience_id)
        return experience
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/users/{user_id}/experiences", response_model=UserExperienceResponse)
async def create_experience(user_id: str, experience_data: UserExperienceCreate, request: Request):
    """Create a new user experience"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        experience = await skillsService.create_experience(
            user_id,
            experience_data.title,
            experience_data.description,
            experience_data.type.value if experience_data.type else None,
            experience_data.company,
            experience_data.start_date.isoformat() if experience_data.start_date else None,
            experience_data.end_date.isoformat() if experience_data.end_date else None,
            experience_data.is_current
        )
        return experience
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/experiences/{experience_id}", response_model=UserExperienceResponse)
async def update_experience(experience_id: str, experience_data: UserExperienceUpdate, request: Request):
    """Update user experience"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        experience = await skillsService.update_experience(
            experience_id,
            experience_data.title,
            experience_data.description,
            experience_data.type.value if experience_data.type else None,
            experience_data.company,
            experience_data.start_date.isoformat() if experience_data.start_date else None,
            experience_data.end_date.isoformat() if experience_data.end_date else None,
            experience_data.is_current
        )
        return experience
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/experiences/{experience_id}")
async def delete_experience(experience_id: str, request: Request):
    """Delete user experience"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await skillsService.delete_experience(experience_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))