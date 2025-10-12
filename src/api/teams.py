from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.teams import TeamsService
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Teams"], dependencies=[Depends(bearer)])

teamservice = TeamsService()

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
