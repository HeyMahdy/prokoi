from fastapi import APIRouter, HTTPException, Request, status, Depends, Query
from fastapi.security import HTTPBearer
from src.services.analytics import AnalyticsService
from typing import List, Dict, Any

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Analytics"], dependencies=[Depends(bearer)])

analytics_service = AnalyticsService()


@router.get("/analytics/projects/dashboard", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_project_analytics_dashboard(request: Request):
    """Get detailed project analytics dashboard data"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        dashboard_data = await analytics_service.get_project_analytics_dashboard()
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch project analytics: {str(e)}")


@router.get("/analytics/projects/summary", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_project_analytics_summary(request: Request):
    """Get overall analytics summary across all projects"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        summary_data = await analytics_service.get_project_analytics_summary()
        return summary_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch analytics summary: {str(e)}")


@router.get("/analytics/projects/top-performing", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_top_performing_projects(
    request: Request,
    limit: int = Query(5, ge=1, le=20, description="Number of top projects to return")
):
    """Get top performing projects by completion percentage"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        top_projects = await analytics_service.get_top_performing_projects(limit)
        return top_projects
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch top performing projects: {str(e)}")


@router.get("/analytics/projects/health", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_project_health_metrics(request: Request):
    """Get project health metrics and insights"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        health_metrics = await analytics_service.get_project_health_metrics()
        return health_metrics
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch project health metrics: {str(e)}")


@router.get("/analytics/projects/{project_id}/details", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_project_analytics_details(project_id: int, request: Request):
    """Get detailed analytics for a specific project"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        dashboard_data = await analytics_service.get_project_analytics_dashboard()
        
        # Find the specific project
        project_data = next((item for item in dashboard_data if item["project_id"] == project_id), None)
        
        if not project_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        return project_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch project details: {str(e)}")


@router.get("/analytics/overview", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_analytics_overview(request: Request):
    """Get comprehensive analytics overview with all key metrics"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        # Get all analytics data
        summary = await analytics_service.get_project_analytics_summary()
        health_metrics = await analytics_service.get_project_health_metrics()
        top_projects = await analytics_service.get_top_performing_projects(5)
        
        return {
            "summary": summary,
            "health_metrics": health_metrics,
            "top_projects": top_projects,
            "generated_at": "2024-01-15T10:30:00Z"  # You can make this dynamic
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch analytics overview: {str(e)}")


@router.get("/analytics/users/performance", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_user_performance_workload_analysis(request: Request):
    """Get user performance and workload analysis data"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        user_analytics = await analytics_service.get_user_performance_workload_analysis()
        return user_analytics
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch user performance analysis: {str(e)}")


@router.get("/analytics/sprints/velocity", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_sprint_velocity_analysis(request: Request):
    """Get sprint velocity analysis data"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        sprint_analytics = await analytics_service.get_sprint_velocity_analysis()
        return sprint_analytics
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch sprint velocity analysis: {str(e)}")


@router.get("/analytics/teams/performance", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_team_performance_collaboration_metrics(request: Request):
    """Get team performance and collaboration metrics data"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        team_analytics = await analytics_service.get_team_performance_collaboration_metrics()
        return team_analytics
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch team performance metrics: {str(e)}")
