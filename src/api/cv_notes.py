from fastapi import APIRouter, HTTPException, Depends,Request, status as fastapi_status
from src.services.cv_notes import CVNotesService
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models for request/response
class CVNotesCreate(BaseModel):
    notes: str

class CVNotesUpdate(BaseModel):
    notes: str

class CVNotesResponse(BaseModel):
    id: str
    user_id: str
    notes: str
    created_at: datetime
    updated_at: datetime
from fastapi.security import HTTPBearer

bearer = HTTPBearer()
# Initialize service
cv_notes_service = CVNotesService()

# Create router
router = APIRouter(prefix="/api/cv-notes", tags=["cv-notes"],dependencies=[Depends(bearer)])

# CV Notes endpoints
@router.post("/", status_code=fastapi_status.HTTP_201_CREATED)
async def create_or_update_cv_notes(notes_data: CVNotesCreate, request: Request):
    """Create or update CV notes for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        notes = await cv_notes_service.create_or_update_cv_notes(
            user_id=user["id"],
            notes=notes_data.notes
        )
        return notes
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
async def get_user_cv_notes(request: Request):
    """Get CV notes for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        notes = await cv_notes_service.get_user_cv_notes(user_id=user["id"])
        if not notes:
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail="No CV notes found for this user")
        return notes
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{note_id}")
async def update_cv_notes(note_id: str, notes_data: CVNotesUpdate, request: Request):
    """Update CV notes by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        notes = await cv_notes_service.update_cv_notes(
            note_id=note_id,
            user_id=user["id"],
            notes=notes_data.notes
        )
        return notes
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{note_id}")
async def delete_cv_notes(note_id: str, request: Request):
    """Delete CV notes by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await cv_notes_service.delete_cv_notes(
            note_id=note_id,
            user_id=user["id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))