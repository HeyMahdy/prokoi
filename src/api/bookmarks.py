from fastapi import APIRouter, HTTPException, Request, Depends ,status as fastapi_status
from src.services.bookmarks import BookmarksService
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Pydantic models for request/response
class BookmarkCreate(BaseModel):
    bookmark_type: str
    bookmark_id: str

class BookmarkResponse(BaseModel):
    id: str
    user_id: str
    bookmark_type: str
    bookmark_id: str
    created_at: datetime

class BookmarkCheckResponse(BaseModel):
    user_id: str
    bookmark_type: str
    bookmark_id: str
    is_bookmarked: bool

from fastapi.security import HTTPBearer

bearer = HTTPBearer()
# Initialize service
bookmarks_service = BookmarksService()

# Create router
router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"],dependencies=[Depends(bearer)])

# Bookmark endpoints
@router.post("/", status_code=fastapi_status.HTTP_201_CREATED)
async def create_bookmark(bookmark_data: BookmarkCreate, request: Request):
    """Create a new bookmark"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        bookmark = await bookmarks_service.create_bookmark(
            user_id=user["id"],
            bookmark_type=bookmark_data.bookmark_type,
            bookmark_id=bookmark_data.bookmark_id
        )
        return bookmark
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{bookmark_id}")
async def get_bookmark(bookmark_id: str, request: Request):
    """Get bookmark by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        bookmark = await bookmarks_service.get_bookmark_by_id(bookmark_id)
        # Check if user owns this bookmark
        if bookmark["user_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Not authorized to access this bookmark")
        return bookmark
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: str, request: Request):
    """Delete bookmark by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        bookmark = await bookmarks_service.get_bookmark_by_id(bookmark_id)
        # Check if user owns this bookmark
        if bookmark["user_id"] != user["id"]:
            raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this bookmark")
            
        result = await bookmarks_service.delete_bookmark(bookmark_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
async def get_user_bookmarks(
    request: Request,
    bookmark_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Get all bookmarks for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        bookmarks = await bookmarks_service.get_user_bookmarks(
            user_id=user["id"],
            bookmark_type=bookmark_type,
            limit=limit,
            offset=offset
        )
        return bookmarks
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/check")
async def check_if_bookmarked(bookmark_data: BookmarkCreate, request: Request):
    """Check if a specific item is bookmarked by the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await bookmarks_service.check_if_bookmarked(
            user_id=user["id"],
            bookmark_type=bookmark_data.bookmark_type,
            bookmark_id=bookmark_data.bookmark_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/user/{bookmark_type}/{bookmark_id}")
async def delete_user_bookmark(bookmark_type: str, bookmark_id: str, request: Request):
    """Delete a specific bookmark for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await bookmarks_service.delete_user_bookmark(
            user_id=user["id"],
            bookmark_type=bookmark_type,
            bookmark_id=bookmark_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))