from src.core.database import db
import uuid
from typing import Optional, List, Dict, Any
import json

class RoadmapsRepository:
    async def create_roadmap(self, user_id: str, target_role: str, time_frame: int, 
                           hours_per_week: int, summary: Optional[str], roadmap_data: Dict) -> str:
        """Create a new roadmap"""
        roadmap_id = str(uuid.uuid4())
        query = """
        INSERT INTO roadmaps (id, user_id, target_role, time_frame, hours_per_week, summary, roadmap_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = [roadmap_id, user_id, target_role, time_frame, hours_per_week, summary, json.dumps(roadmap_data)]
        await db.execute_insert(query, params)
        return roadmap_id

    async def get_roadmap_by_id(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Get roadmap by ID"""
        query = """
        SELECT id, user_id, target_role, time_frame, hours_per_week, summary, roadmap_data, created_at
        FROM roadmaps
        WHERE id = %s
        """
        rows = await db.execute_query(query, (roadmap_id,))
        if rows:
            # Parse JSON data
            roadmap = rows[0]
            if isinstance(roadmap['roadmap_data'], str):
                roadmap['roadmap_data'] = json.loads(roadmap['roadmap_data'])
            return roadmap
        return None

    async def get_user_roadmaps(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all roadmaps for a user"""
        query = """
        SELECT id, user_id, target_role, time_frame, hours_per_week, summary, roadmap_data, created_at
        FROM roadmaps
        WHERE user_id = %s
        ORDER BY created_at DESC
        """
        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        
        rows = await db.execute_query(query, (user_id,))
        # Parse JSON data for each roadmap
        for row in rows:
            if isinstance(row['roadmap_data'], str):
                row['roadmap_data'] = json.loads(row['roadmap_data'])
        return rows

    async def update_roadmap(self, roadmap_id: str, **kwargs) -> bool:
        """Update roadmap details"""
        # Build dynamic query based on provided fields
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if value is not None and key in ['target_role', 'time_frame', 'hours_per_week', 'summary', 'roadmap_data']:
                if key == 'roadmap_data':
                    updates.append(f"{key} = %s")
                    params.append(json.dumps(value))
                else:
                    updates.append(f"{key} = %s")
                    params.append(value)
                
        if not updates:
            return False
            
        query = f"UPDATE roadmaps SET {', '.join(updates)} WHERE id = %s"
        params.append(roadmap_id)
        
        await db.execute_query(query, params)
        return True

    async def delete_roadmap(self, roadmap_id: str) -> bool:
        """Delete a roadmap by ID"""
        query = "DELETE FROM roadmaps WHERE id = %s"
        await db.execute_query(query, (roadmap_id,))
        return True

    async def get_user_roadmap_count(self, user_id: str) -> int:
        """Get total roadmap count for a user"""
        query = "SELECT COUNT(*) as count FROM roadmaps WHERE user_id = %s"
        params = [user_id]
        rows = await db.execute_query(query, params)
        return rows[0]['count'] if rows else 0