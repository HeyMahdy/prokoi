from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.skills import SkillsService
from src.schemas.skills import SkillResponse, UserSkillCreate, UserSkillUpdate, UserSkillResponse, UserSkillsListResponse
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Skills"], dependencies=[Depends(bearer)])

skillsService = SkillsService()

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get skills")

@router.get("/skills/{skill_id}", response_model=SkillResponse)
async def get_skill_by_id(skill_id: int, request: Request):
    """Get skill by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        skill = await skillsService.get_skill_by_id(skill_id)
        return skill
    except Exception as e:
        if "Skill not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get skill")

@router.post("/users/skills", response_model=UserSkillResponse, status_code=status.HTTP_201_CREATED)
async def add_skill_to_user(skill_data: UserSkillCreate, request: Request):
    """Add skill to user with proficiency level"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = user["id"]

    try:
        user_skill = await skillsService.add_skill_to_user(user_id, skill_data)
        return user_skill
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "User not found" in str(e) or "Skill not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "User already has this skill" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add skill to user")

@router.put("/users/skills/{skill_id}", response_model=UserSkillResponse)
async def update_user_skill(skill_id: int, skill_data: UserSkillUpdate, request: Request):
    """Update user's skill proficiency level"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = user["id"]

    try:
        user_skill = await skillsService.update_user_skill(user_id, skill_id, skill_data)
        return user_skill
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "User not found" in str(e) or "Skill not found" in str(e) or "User does not have this skill" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user skill")

@router.get("/users/skills", response_model=UserSkillsListResponse)
async def get_user_skills(request: Request):
    """Get all skills for the authenticated user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = user["id"]

    try:
        user_skills = await skillsService.get_user_skills(user_id)
        return user_skills
    except Exception as e:
        if "User not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get user skills")

@router.get("/users/skills/{skill_id}", response_model=UserSkillResponse)
async def get_user_skill(skill_id: int, request: Request):
    """Get specific user skill"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = user["id"]

    try:
        user_skill = await skillsService.get_user_skill(user_id, skill_id)
        return user_skill
    except Exception as e:
        if "User not found" in str(e) or "Skill not found" in str(e) or "User does not have this skill" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get user skill")

@router.delete("/users/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_skill(skill_id: int, request: Request):
    """Remove skill from user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = user["id"]

    try:
        result = await skillsService.remove_user_skill(user_id, skill_id)
        return result
    except Exception as e:
        if "User not found" in str(e) or "Skill not found" in str(e) or "User does not have this skill" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove user skill")
