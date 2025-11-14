from src.repositories.bookmarks import BookmarksRepository
from typing import Optional, List, Dict, Any

class BookmarksService:
    def __init__(self):
        self.bookmarks_repo = BookmarksRepository()

    async def create_bookmark(self, user_id: str, bookmark_type: str, bookmark_id: str) -> Dict[str, Any]:
        """Create a new bookmark"""
        try:
            # Check if already bookmarked
            is_bookmarked = await self.bookmarks_repo.check_if_bookmarked(user_id, bookmark_type, bookmark_id)
            if is_bookmarked:
                raise Exception("Item is already bookmarked")
                
            bookmark_id_new = await self.bookmarks_repo.create_bookmark(user_id, bookmark_type, bookmark_id)
            
            bookmark = await self.bookmarks_repo.get_bookmark_by_id(bookmark_id_new)
            if not bookmark:
                raise Exception("Failed to create bookmark")
                
            return bookmark
        except Exception as e:
            raise Exception(f"Failed to create bookmark: {str(e)}")

    async def get_bookmark_by_id(self, bookmark_id: str) -> Dict[str, Any]:
        """Get bookmark by ID"""
        try:
            bookmark = await self.bookmarks_repo.get_bookmark_by_id(bookmark_id)
            if not bookmark:
                raise Exception("Bookmark not found")
            return bookmark
        except Exception as e:
            raise Exception(f"Failed to get bookmark: {str(e)}")

    async def get_user_bookmarks(self, user_id: str, bookmark_type: Optional[str] = None,
                               limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all bookmarks for a user"""
        try:
            bookmarks = await self.bookmarks_repo.get_user_bookmarks(user_id, bookmark_type, limit, offset)
            total_count = await self.bookmarks_repo.get_user_bookmark_count(user_id)
            
            return {
                "bookmarks": bookmarks,
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "bookmark_type": bookmark_type
            }
        except Exception as e:
            raise Exception(f"Failed to get user bookmarks: {str(e)}")

    async def check_if_bookmarked(self, user_id: str, bookmark_type: str, bookmark_id: str) -> Dict[str, Any]:
        """Check if a specific item is bookmarked by user"""
        try:
            is_bookmarked = await self.bookmarks_repo.check_if_bookmarked(user_id, bookmark_type, bookmark_id)
            return {
                "user_id": user_id,
                "bookmark_type": bookmark_type,
                "bookmark_id": bookmark_id,
                "is_bookmarked": is_bookmarked
            }
        except Exception as e:
            raise Exception(f"Failed to check bookmark status: {str(e)}")

    async def delete_bookmark(self, bookmark_id: str) -> Dict[str, str]:
        """Delete a bookmark by ID"""
        try:
            # First verify the bookmark exists
            bookmark = await self.bookmarks_repo.get_bookmark_by_id(bookmark_id)
            if not bookmark:
                raise Exception("Bookmark not found")
                
            # Delete the bookmark
            success = await self.bookmarks_repo.delete_bookmark(bookmark_id)
            if not success:
                raise Exception("Failed to delete bookmark")
                
            return {"message": "Bookmark deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete bookmark: {str(e)}")

    async def delete_user_bookmark(self, user_id: str, bookmark_type: str, bookmark_id: str) -> Dict[str, str]:
        """Delete a specific bookmark for a user"""
        try:
            # Check if bookmark exists
            is_bookmarked = await self.bookmarks_repo.check_if_bookmarked(user_id, bookmark_type, bookmark_id)
            if not is_bookmarked:
                raise Exception("Bookmark not found")
                
            # Delete the bookmark
            success = await self.bookmarks_repo.delete_user_bookmark(user_id, bookmark_type, bookmark_id)
            if not success:
                raise Exception("Failed to delete bookmark")
                
            return {"message": "Bookmark deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete bookmark: {str(e)}")