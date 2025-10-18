from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.issue_skills import IssueSkillsService
from src.schemas.issue_skills import (
    IssueSkillRequirementCreate, 
    IssueSkillRequirementUpdate, 
    IssueSkillRequirementResponse,
    IssueSkillsListResponse,
    SkillMatchResponse
)
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Issue Skills"], dependencies=[Depends(bearer)])

issue_skills_service = IssueSkillsService()

@router.post("/issues/{issue_id}/skills", response_model=IssueSkillRequirementResponse, status_code=status.HTTP_201_CREATED)
async def add_skill_to_issue(issue_id: int, skill_data: IssueSkillRequirementCreate, request: Request):
    """Add skill requirement to an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        requirement = await issue_skills_service.add_skill_to_issue(issue_id, skill_data)
        return requirement
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "already exists" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/issues/{issue_id}/skills/{skill_id}", response_model=IssueSkillRequirementResponse)
async def update_issue_skill_requirement(
    issue_id: int, 
    skill_id: int, 
    skill_data: IssueSkillRequirementUpdate, 
    request: Request
):
    """Update skill requirement level for an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        requirement = await issue_skills_service.update_issue_skill_requirement(issue_id, skill_id, skill_data)
        return requirement
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/issues/{issue_id}/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_skill_from_issue(issue_id: int, skill_id: int, request: Request):
    """Remove skill requirement from an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await issue_skills_service.remove_skill_from_issue(issue_id, skill_id)
        return None
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/issues/{issue_id}/skills", response_model=IssueSkillsListResponse)
async def get_issue_skills(issue_id: int, request: Request):
    """Get all skill requirements for an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        skills = await issue_skills_service.get_issue_skills(issue_id)
        return skills
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/issues/{issue_id}/skills/{skill_id}", response_model=IssueSkillRequirementResponse)
async def get_issue_skill_requirement(issue_id: int, skill_id: int, request: Request):
    """Get specific skill requirement for an issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        requirement = await issue_skills_service.get_issue_skill_requirement(issue_id, skill_id)
        return requirement
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/issues/{issue_id}/skill-match-analysis", response_model=list[SkillMatchResponse])
async def get_skill_match_analysis(issue_id: int, request: Request):
    """Get skill match analysis for current user and issue"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        analysis = await issue_skills_service.get_skill_match_analysis(issue_id, user["id"])
        return analysis
    except Exception as e:
        if "not found" in str(e).lower() or "access" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
