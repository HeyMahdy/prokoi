from fastapi import APIRouter, HTTPException, Request, Depends,status as fastapi_status
from src.services.roadmaps import RoadmapsService
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi.security import HTTPBearer
from src.services.roadmaps import RoadmapsService
# Pydantic models for request/response
class RoadmapCreate(BaseModel):
    target_role: str
    time_frame: int
    hours_per_week: int
    summary: Optional[str] = None
    roadmap_data: Optional[Dict[str, Any]] = None

class RoadmapUpdate(BaseModel):
    target_role: Optional[str] = None
    time_frame: Optional[int] = None
    hours_per_week: Optional[int] = None
    summary: Optional[str] = None
    roadmap_data: Optional[Dict[str, Any]] = None

class RoadmapResponse(BaseModel):
    id: str
    user_id: str
    target_role: str
    time_frame: int
    hours_per_week: int
    summary: Optional[str] = None
    roadmap_data: Dict[str, Any]
    created_at: datetime

jobs_service = RoadmapsService()
bearer = HTTPBearer()
# Initialize service
roadmaps_service = RoadmapsService()

# Create router
router = APIRouter(prefix="/api/roadmaps", tags=["roadmaps"],dependencies=[Depends(bearer)])

# Roadmap endpoints
@router.post("/", status_code=fastapi_status.HTTP_201_CREATED)
async def create_roadmap(roadmap_data: RoadmapCreate, request: Request):
    """Create a new roadmap"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        roadmap = await roadmaps_service.create_roadmap(
            user_id=user["id"],
            target_role=roadmap_data.target_role,
            time_frame=roadmap_data.time_frame,
            hours_per_week=roadmap_data.hours_per_week,
            summary=roadmap_data.summary,
            roadmap_data=roadmap_data.roadmap_data or {}
        )
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{roadmap_id}")
async def get_roadmap(roadmap_id: str, request: Request):
    """Get roadmap by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        roadmap = await roadmaps_service.get_roadmap_by_id(roadmap_id)
        # Check if user owns this roadmap
        if roadmap["user_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Not authorized to access this roadmap")
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{roadmap_id}")
async def update_roadmap(roadmap_id: str, roadmap_data: RoadmapUpdate, request: Request):
    """Update roadmap by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        roadmap = await roadmaps_service.update_roadmap(
            roadmap_id=roadmap_id,
            user_id=user["id"],
            **roadmap_data.dict(exclude_unset=True)
        )
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{roadmap_id}")
async def delete_roadmap(roadmap_id: str, request: Request):
    """Delete roadmap by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await roadmaps_service.delete_roadmap(
            roadmap_id=roadmap_id,
            user_id=user["id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
async def get_user_roadmaps(
    request: Request,
    limit: int = 20,
    offset: int = 0
):
    """Get all roadmaps for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        roadmaps = await roadmaps_service.get_user_roadmaps(
            user_id=user["id"],
            limit=limit,
            offset=offset
        )
        return roadmaps
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))