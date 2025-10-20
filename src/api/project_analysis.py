from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer

from src.dependencies.permission import require_permissions
from src.services.project_analysis import ProjectAnalysisService
from src.schemas.project_analysis import ProjectAnalysisDepthResponse

bearer = HTTPBearer()
router = APIRouter(prefix="/api", tags=["Project Analysis"], dependencies=[Depends(bearer)])

project_analysis_service = ProjectAnalysisService()

@router.get("/projects/{project_id}/analysis/depth", response_model=ProjectAnalysisDepthResponse, status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_permissions(["all"]))]
            )
async def get_project_analysis_depth(project_id: int, request: Request):
    """Get detailed project analysis with comprehensive depth metrics"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        analysis_data = await project_analysis_service.get_project_analysis_depth(project_id)
        
        if not analysis_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found or no data available")
        
        return analysis_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch project analysis: {str(e)}")
