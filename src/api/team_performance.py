from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer

from src.dependencies.permission import require_permissions
from src.services.team_performance import TeamPerformanceService
from src.schemas.team_performance import TeamPerformanceResponse
from typing import List

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Team Performance"], dependencies=[Depends(bearer)])

team_performance_service = TeamPerformanceService()

@router.get("/teams/performance", response_model=List[TeamPerformanceResponse], status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_permissions(["all"]))])
async def get_team_performance_metrics(request: Request):
    """Get team performance and collaboration metrics for all teams"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        team_metrics = await team_performance_service.get_team_performance_metrics()
        return team_metrics
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch team performance metrics: {str(e)}")
