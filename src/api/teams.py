from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.teams import TeamsService
from src.services.velocity import VelocityService
from src.schemas.velocity import VelocityUpdate, VelocityResponse, TeamVelocityHistory
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Teams"], dependencies=[Depends(bearer)])

teamservice = TeamsService()
velocityService = VelocityService()

@router.post("/organizations/{org_id}/teams", status_code=status.HTTP_201_CREATED)
async def create_team(org_id: int, name: str, request: Request):
    """Create team in organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        team = await teamservice.create_team(org_id, name, user["id"])
        return team
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create team")

@router.get("/organizations/{org_id}/teams")
async def list_organization_teams(org_id: int, request: Request):
    """List all teams in organization"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        teams = await teamservice.get_organization_teams(org_id, user["id"])
        return teams
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get teams")

@router.get("/teams/{team_id}")
async def get_team(team_id: int, request: Request):
    """Get team details"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        team = await teamservice.get_team_by_id(team_id, user["id"])
        return team
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

@router.put("/teams/{team_id}")
async def update_team(team_id: int, name: str, request: Request):
    """Update team"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        team = await teamservice.update_team(team_id, name, user["id"])
        return team
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update team")

@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, request: Request):
    """Delete team"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await teamservice.delete_team(team_id, user["id"])
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete team")

@router.get("/teams/{team_id}/velocity", response_model=list[TeamVelocityHistory])
async def get_team_velocity_history(team_id: int, request: Request):
    """Get team velocity history across all projects"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        velocity_history = await velocityService.get_team_velocity_history(team_id, user["id"])
        return velocity_history
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get team velocity history")

@router.put("/teams/{team_id}/velocity", response_model=VelocityResponse)
async def update_team_velocity(team_id: int, velocity_data: VelocityUpdate, request: Request):
    """Update team velocity"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        velocity = await velocityService.update_team_velocity(team_id, velocity_data, user["id"])
        return velocity
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update team velocity")
