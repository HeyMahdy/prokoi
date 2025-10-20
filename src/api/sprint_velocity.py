from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer

from src.dependencies.permission import require_permissions
from src.services.sprint_velocity import SprintVelocityService
from src.schemas.sprint_velocity import SprintVelocityResponse
from typing import List

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Sprint Velocity"], dependencies=[Depends(bearer)])

sprint_velocity_service = SprintVelocityService()

@router.get("/sprints/velocity", response_model=List[SprintVelocityResponse], status_code=status.HTTP_200_OK,dependencies=[Depends(require_permissions(["all", "add_issue_to_sprint"]))])
async def get_sprint_velocity_analysis(request: Request):
    """Get sprint velocity analysis for all sprints"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint_metrics = await sprint_velocity_service.get_sprint_velocity_analysis()
        return sprint_metrics
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch sprint velocity analysis: {str(e)}")
