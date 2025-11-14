from src.core.database import db
import uuid
from typing import Optional, List, Dict, Any

class ResourcesRepository:
    async def create_resource(self, title: str, platform: str, url: str, cost: str,
                            description: Optional[str], duration_hours: Optional[float],
                            difficulty_level: str, rating: Optional[float]) -> str:
        """Create a new resource"""
        resource_id = str(uuid.uuid4())
        query = """
        INSERT INTO resources (id, title, platform, url, cost, description, 
                              duration_hours, difficulty_level, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [resource_id, title, platform, url, cost, description,
                 duration_hours, difficulty_level, rating]
        await db.execute_insert(query, params)
        return resource_id

    async def get_resource_by_id(self, resource_id: str) -> Optional[Dict[str, Any]]:
        query = """
        SELECT id, title, platform, url, cost, description, duration_hours,
               difficulty_level, rating, created_at, updated_at, is_active
        FROM resources
        WHERE id = %s AND is_active = TRUE
        """
        rows = await db.execute_query(query, (resource_id,))
        return rows[0] if rows else None

    async def get_resources(
        self,
        platform: Optional[str] = None,
        cost: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        min_rating: Optional[float] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        query = """
        SELECT id, title, platform, url, cost, description, duration_hours,
               difficulty_level, rating, created_at, updated_at, is_active
        FROM resources
        WHERE is_active = TRUE
        """
        params = []

        if platform:
            query += " AND platform = %s"
            params.append(platform)

        if cost:
            query += " AND cost = %s"
            params.append(cost)

        if difficulty_level:
            query += " AND difficulty_level = %s"
            params.append(difficulty_level)

        if min_rating is not None:
            query += " AND rating >= %s"
            params.append(min_rating)

        query += " ORDER BY rating DESC, created_at DESC"
        
        # Add LIMIT and OFFSET directly (ensure they are integers)
        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"

        return await db.execute_query(query, params)




    async def update_resource(self, resource_id: str, **kwargs) -> bool:
        """Update resource details"""
        # Build dynamic query based on provided fields
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if value is not None and key in ['title', 'platform', 'url', 'cost', 'description',
                                           'duration_hours', 'difficulty_level', 'rating', 'is_active']:
                updates.append(f"{key} = %s")
                params.append(value)
                
        if not updates:
            return False
            
        query = f"UPDATE resources SET {', '.join(updates)} WHERE id = %s"
        params.append(resource_id)
        
        await db.execute_query(query, params)
        return True

    async def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource (soft delete by setting is_active to False)"""
        query = "UPDATE resources SET is_active = FALSE WHERE id = %s"
        await db.execute_query(query, (resource_id,))
        return True

    async def add_skill_to_resource(self, resource_id: str, skill_id: str) -> str:
        """Add a skill to a resource"""
        resource_skill_id = str(uuid.uuid4())
        query = """
        INSERT INTO resource_skills (id, resource_id, skill_id)
        VALUES (%s, %s, %s)
        """
        params = [resource_skill_id, resource_id, skill_id]
        await db.execute_insert(query, params)
        return resource_skill_id

    async def get_resource_skills(self, resource_id: str) -> List[Dict[str, Any]]:
        """Get all skills for a resource"""
        query = """
        SELECT rs.id, rs.resource_id, rs.skill_id, s.name as skill_name
        FROM resource_skills rs
        JOIN skills s ON rs.skill_id = s.id
        WHERE rs.resource_id = %s
        ORDER BY s.name
        """
        return await db.execute_query(query, (resource_id,))

    async def remove_skill_from_resource(self, resource_id: str, skill_id: str) -> bool:
        """Remove a skill from a resource"""
        query = "DELETE FROM resource_skills WHERE resource_id = %s AND skill_id = %s"
        await db.execute_query(query, (resource_id, skill_id))
        return True

    async def create_user_progress(self, user_id: str, resource_id: str) -> str:
        """Create user progress record"""
        progress_id = str(uuid.uuid4())
        query = """
        INSERT INTO user_resource_progress (id, user_id, resource_id)
        VALUES (%s, %s, %s)
        """
        params = [progress_id, user_id, resource_id]
        await db.execute_insert(query, params)
        return progress_id

    async def get_user_progress(self, user_id: str, resource_id: str) -> Optional[Dict[str, Any]]:
        """Get user progress for a specific resource"""
        query = """
        SELECT id, user_id, resource_id, status, progress_percentage, started_at, 
               completed_at, test_taken, test_score, test_passed
        FROM user_resource_progress
        WHERE user_id = %s AND resource_id = %s
        """
        rows = await db.execute_query(query, (user_id, resource_id))
        return rows[0] if rows else None

    async def update_user_progress(self, progress_id: str, **kwargs) -> bool:
        """Update user progress"""
        # Build dynamic query based on provided fields
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if value is not None and key in ['status', 'progress_percentage', 'started_at',
                                           'completed_at', 'test_taken', 'test_score', 'test_passed']:
                updates.append(f"{key} = %s")
                params.append(value)
                
        if not updates:
            return False
            
        query = f"UPDATE user_resource_progress SET {', '.join(updates)} WHERE id = %s"
        params.append(progress_id)
        
        await db.execute_query(query, params)
        return True

    async def get_user_resources_progress(self, user_id: str, status: Optional[str] = None,
                                         limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all resources progress for a user"""
        query = """
        SELECT urp.id, urp.user_id, urp.resource_id, r.title as resource_title,
               urp.status, urp.progress_percentage, urp.started_at, urp.completed_at,
               urp.test_taken, urp.test_score, urp.test_passed
        FROM user_resource_progress urp
        JOIN resources r ON urp.resource_id = r.id
        WHERE urp.user_id = %s
        """
        params = [user_id]
        
        if status:
            query += " AND urp.status = %s"
            params.append(status)
            
        query += " ORDER BY urp.started_at DESC LIMIT %s OFFSET %s"
        params.extend([str(limit), str(offset)])
        
        return await db.execute_query(query, params)

    async def user_has_progress_record(self, user_id: str, resource_id: str) -> bool:
        """Check if user has a progress record for a resource"""
        query = """
        SELECT 1 FROM user_resource_progress 
        WHERE user_id = %s AND resource_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, resource_id))
        return len(rows) > 0