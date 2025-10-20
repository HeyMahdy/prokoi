from fastapi import APIRouter, HTTPException, Request, status, Depends
from src.services.team_members import TeamMembersService
from src.schemas.team_members import TeamMemberCreate, TeamMemberResponse, TeamMemberWithUser
from fastapi.security import HTTPBearer
from src.dependencies.permission import require_permissions

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Team Members"], dependencies=[Depends(bearer)])

teamMembersService = TeamMembersService()

@router.post("/teams/{team_id}/members", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions(["all", "add_team_member"]))])
async def add_team_member(team_id: int, user_id: int, request: Request):
    """Add team member"""
    requester = getattr(request.state, "user", None)
    if not requester:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        member = await teamMembersService.add_team_member(team_id, user_id, requester["id"])
        return member
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "User not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif "already a member" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add team member")

@router.get("/teams/{team_id}/members")
async def list_team_members(team_id: int, request: Request):
    """List team members"""
    requester = getattr(request.state, "user", None)
    if not requester:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        members = await teamMembersService.get_team_members(team_id, requester["id"])
        return members
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get team members")

@router.delete("/teams/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permissions(["all", "remove_team_member"]))])
async def remove_team_member(team_id: int, user_id: int, request: Request):
    """Remove team member"""
    requester = getattr(request.state, "user", None)
    if not requester:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        await teamMembersService.remove_team_member(team_id, user_id, requester["id"])
        return
    except Exception as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove team member")
