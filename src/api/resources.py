from fastapi import APIRouter, HTTPException, Request, Depends,status as fastapi_status 
from src.services.resources import ResourcesService
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Pydantic models for request/response
class ResourceCreate(BaseModel):
    title: str
    platform: str
    url: str
    cost: str
    description: Optional[str] = None
    duration_hours: Optional[float] = None
    difficulty_level: str = "Beginner"
    rating: Optional[float] = None

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    platform: Optional[str] = None
    url: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    duration_hours: Optional[float] = None
    difficulty_level: Optional[str] = None
    rating: Optional[float] = None
    is_active: Optional[bool] = None

class ResourceResponse(BaseModel):
    id: str
    title: str
    platform: str
    url: str
    cost: str
    description: Optional[str] = None
    duration_hours: Optional[float] = None
    difficulty_level: str
    rating: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

class ResourceProgressCreate(BaseModel):
    status: Optional[str] = None
    progress_percentage: Optional[int] = None
    test_taken: Optional[bool] = None
    test_score: Optional[int] = None
    test_passed: Optional[bool] = None

class ResourceProgressResponse(BaseModel):
    id: str
    user_id: str
    resource_id: str
    resource_title: Optional[str] = None
    status: str
    progress_percentage: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    test_taken: bool
    test_score: Optional[int] = None
    test_passed: bool

from fastapi.security import HTTPBearer

bearer = HTTPBearer()
# Initialize service
resources_service = ResourcesService()

# Create router
router = APIRouter(prefix="/api/resources", tags=["resources"],dependencies=[Depends(bearer)])

# Resource endpoints
@router.post("/create", status_code=fastapi_status.HTTP_201_CREATED)
async def create_resource(resource_data: ResourceCreate, request: Request):
    """Create a new resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        resource = await resources_service.create_resource(**resource_data.dict())
        return resource
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/get/{resource_id}")
async def get_resource(resource_id: str):
    """Get resource by ID"""
    try:
        resource = await resources_service.get_resource_by_id(resource_id)
        return resource
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/put/{resource_id}")
async def update_resource(resource_id: str, resource_data: ResourceUpdate, request: Request):
    """Update resource by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        resource = await resources_service.update_resource(
            resource_id=resource_id,
            **resource_data.dict(exclude_unset=True)
        )
        return resource
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/del/{resource_id}")
async def delete_resource(resource_id: str, request: Request):
    """Delete resource by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await resources_service.delete_resource(resource_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/getall")
async def get_resources(
    platform: Optional[str] = None,
    cost: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    min_rating: Optional[float] = None,
    limit: int = 20,
    offset: int = 0
):
    """Get all resources with optional filters"""
    try:
        resources = await resources_service.get_resources(
            platform=platform,
            cost=cost,
            difficulty_level=difficulty_level,
            min_rating=min_rating,
            limit=limit,
            offset=offset
        )
        return resources
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

# Resource Skills endpoints
@router.post("/{resource_id}/skills/{skill_id}")
async def add_resource_skill(resource_id: str, skill_id: str, request: Request):
    """Add a skill to a resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await resources_service.add_skill_to_resource(resource_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{resource_id}/skills/{skill_id}")
async def remove_resource_skill(resource_id: str, skill_id: str, request: Request):
    """Remove a skill from a resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await resources_service.remove_skill_from_resource(resource_id, skill_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{resource_id}/skills")
async def get_resource_skills(resource_id: str):
    """Get all skills for a resource"""
    try:
        skills = await resources_service.get_resource_skills(resource_id)
        return skills
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

# Resource Progress endpoints
@router.post("/{resource_id}/progress/start")
async def start_resource_progress(resource_id: str, request: Request):
    """Start tracking progress for a resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        progress = await resources_service.start_resource_progress(user["id"], resource_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{resource_id}/progress")
async def update_resource_progress(resource_id: str, progress_data: ResourceProgressCreate, request: Request):
    """Update user progress for a resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        progress = await resources_service.update_resource_progress(
            user_id=user["id"],
            resource_id=resource_id,
            **progress_data.dict(exclude_unset=True)
        )
        return progress
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{resource_id}/progress")
async def get_user_resource_progress(resource_id: str, request: Request):
    """Get user progress for a specific resource"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        progress = await resources_service.get_user_progress(user["id"], resource_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/progress/my")
async def get_my_resources_progress(request: Request, status: Optional[str] = None, limit: int = 20, offset: int = 0):
    """Get all resources progress for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        progress = await resources_service.get_user_resources_progress(
            user_id=user["id"],
            status=status,
            limit=limit,
            offset=offset
        )
        return progress
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))