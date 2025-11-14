from fastapi import APIRouter, HTTPException, Depends,Request, status as fastapi_status
from src.services.cv_uploads import CVUploadsService
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Pydantic models for request/response
class CVUploadCreate(BaseModel):
    file_name: str
    file_url: str
    file_type: str
    extracted_data: Optional[Dict[str, Any]] = None

class CVUploadResponse(BaseModel):
    id: str
    user_id: str
    file_name: str
    file_url: str
    file_type: str
    extracted_data: Optional[Dict[str, Any]] = None
    uploaded_at: datetime
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
# Initialize service
cv_uploads_service = CVUploadsService()

# Create router
router = APIRouter(prefix="/api/cv-uploads", tags=["cv-uploads"],dependencies=[Depends(bearer)])

# CV Upload endpoints
@router.post("/", status_code=fastapi_status.HTTP_201_CREATED)
async def create_cv_upload(upload_data: CVUploadCreate, request: Request):
    """Create a new CV upload record"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        upload = await cv_uploads_service.create_cv_upload(
            user_id=user["id"],
            file_name=upload_data.file_name,
            file_url=upload_data.file_url,
            file_type=upload_data.file_type,
            extracted_data=upload_data.extracted_data
        )
        return upload
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{upload_id}")
async def get_cv_upload(upload_id: str, request: Request):
    """Get CV upload by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        upload = await cv_uploads_service.get_cv_upload_by_id(
            upload_id=upload_id,
            user_id=user["id"]
        )
        return upload
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{upload_id}")
async def delete_cv_upload(upload_id: str, request: Request):
    """Delete CV upload by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await cv_uploads_service.delete_cv_upload(
            upload_id=upload_id,
            user_id=user["id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
async def get_user_cv_uploads(
    request: Request,
    limit: int = 20,
    offset: int = 0
):
    """Get all CV uploads for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        uploads = await cv_uploads_service.get_user_cv_uploads(
            user_id=user["id"],
            limit=limit,
            offset=offset
        )
        return uploads
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))