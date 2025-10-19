from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer
from src.services.user_performance import UserPerformanceService
from src.schemas.user_performance import UserPerformanceResponse
from typing import List

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["User Performance"], dependencies=[Depends(bearer)])

user_performance_service = UserPerformanceService()

@router.get("/users/performance")
async def get_user_performance(request: Request):
    """Get user performance and workload analysis for all users"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        user_metrics = await user_performance_service.get_user_performance_metrics()
        return user_metrics
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch user performance metrics: {str(e)}")
