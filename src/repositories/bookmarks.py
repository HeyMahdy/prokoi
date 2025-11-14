from src.core.database import db
import uuid
from typing import Optional, List, Dict, Any

class BookmarksRepository:
    async def create_bookmark(self, user_id: str, bookmark_type: str, bookmark_id: str) -> str:
        """Create a new bookmark"""
        bookmark_id_new = str(uuid.uuid4())
        query = """
        INSERT INTO bookmarks (id, user_id, bookmark_type, bookmark_id)
        VALUES (%s, %s, %s, %s)
        """
        params = [bookmark_id_new, user_id, bookmark_type, bookmark_id]
        await db.execute_insert(query, params)
        return bookmark_id_new

    async def get_bookmark_by_id(self, bookmark_id: str) -> Optional[Dict[str, Any]]:
        """Get bookmark by ID"""
        query = """
        SELECT id, user_id, bookmark_type, bookmark_id, created_at
        FROM bookmarks
        WHERE id = %s
        """
        rows = await db.execute_query(query, (bookmark_id,))
        return rows[0] if rows else None

    async def get_user_bookmarks(self, user_id: str, bookmark_type: Optional[str] = None,
                               limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all bookmarks for a user"""
        query = """
        SELECT id, user_id, bookmark_type, bookmark_id, created_at
        FROM bookmarks
        WHERE user_id = %s
        """
        params = [user_id]
        
        if bookmark_type:
            query += " AND bookmark_type = %s"
            params.append(bookmark_type)
            
        query += " ORDER BY created_at DESC"
        
        # Add LIMIT and OFFSET directly (ensure they are integers)
        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        
        return await db.execute_query(query, params)

    async def check_if_bookmarked(self, user_id: str, bookmark_type: str, bookmark_id: str) -> bool:
        """Check if a specific item is bookmarked by user"""
        query = """
        SELECT 1 FROM bookmarks 
        WHERE user_id = %s AND bookmark_type = %s AND bookmark_id = %s
        LIMIT 1
        """
        params = [user_id, bookmark_type, bookmark_id]
        rows = await db.execute_query(query, params)
        return len(rows) > 0

    async def delete_bookmark(self, bookmark_id: str) -> bool:
        """Delete a bookmark by ID"""
        query = "DELETE FROM bookmarks WHERE id = %s"
        await db.execute_query(query, (bookmark_id,))
        return True

    async def delete_user_bookmark(self, user_id: str, bookmark_type: str, bookmark_id: str) -> bool:
        """Delete a specific bookmark for a user"""
        query = "DELETE FROM bookmarks WHERE user_id = %s AND bookmark_type = %s AND bookmark_id = %s"
        params = [user_id, bookmark_type, bookmark_id]
        await db.execute_query(query, params)
        return True

    async def get_user_bookmark_count(self, user_id: str) -> int:
        """Get total bookmark count for a user"""
        query = "SELECT COUNT(*) as count FROM bookmarks WHERE user_id = %s"
        params = [user_id]
        rows = await db.execute_query(query, params)
        return rows[0]['count'] if rows else 0