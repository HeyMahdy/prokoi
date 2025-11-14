from src.repositories.roadmaps import RoadmapsRepository
from typing import Optional, List, Dict, Any

class RoadmapsService:
    def __init__(self):
        self.roadmaps_repo = RoadmapsRepository()

    async def create_roadmap(self, user_id: str, target_role: str, time_frame: int, 
                          hours_per_week: int, summary: Optional[str] = None, 
                          roadmap_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new roadmap"""
        try:
            if roadmap_data is None:
                roadmap_data = {}
                
            roadmap_id = await self.roadmaps_repo.create_roadmap(
                user_id, target_role, time_frame, hours_per_week, summary, roadmap_data
            )
            
            roadmap = await self.roadmaps_repo.get_roadmap_by_id(roadmap_id)
            if not roadmap:
                raise Exception("Failed to create roadmap")
                
            return roadmap
        except Exception as e:
            raise Exception(f"Failed to create roadmap: {str(e)}")

    async def get_roadmap_by_id(self, roadmap_id: str) -> Dict[str, Any]:
        """Get roadmap by ID"""
        try:
            roadmap = await self.roadmaps_repo.get_roadmap_by_id(roadmap_id)
            if not roadmap:
                raise Exception("Roadmap not found")
            return roadmap
        except Exception as e:
            raise Exception(f"Failed to get roadmap: {str(e)}")

    async def get_user_roadmaps(self, user_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all roadmaps for a user"""
        try:
            roadmaps = await self.roadmaps_repo.get_user_roadmaps(user_id, limit, offset)
            total_count = await self.roadmaps_repo.get_user_roadmap_count(user_id)
            
            return {
                "roadmaps": roadmaps,
                "total": total_count,
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            raise Exception(f"Failed to get user roadmaps: {str(e)}")

    async def update_roadmap(self, roadmap_id: str, user_id: str, **kwargs) -> Dict[str, Any]:
        """Update roadmap details"""
        try:
            # First verify the roadmap exists and belongs to the user
            roadmap = await self.roadmaps_repo.get_roadmap_by_id(roadmap_id)
            if not roadmap:
                raise Exception("Roadmap not found")
                
            if roadmap["user_id"] != user_id:
                raise Exception("Unauthorized: You can only update your own roadmaps")
                
            # Update the roadmap
            success = await self.roadmaps_repo.update_roadmap(roadmap_id, **kwargs)
            if not success:
                raise Exception("Failed to update roadmap")
                
            # Return updated roadmap
            updated_roadmap = await self.roadmaps_repo.get_roadmap_by_id(roadmap_id)
            if not updated_roadmap:
                raise Exception("Failed to retrieve updated roadmap")
            return updated_roadmap
        except Exception as e:
            raise Exception(f"Failed to update roadmap: {str(e)}")

    async def delete_roadmap(self, roadmap_id: str, user_id: str) -> Dict[str, str]:
        """Delete a roadmap by ID"""
        try:
            # First verify the roadmap exists and belongs to the user
            roadmap = await self.roadmaps_repo.get_roadmap_by_id(roadmap_id)
            if not roadmap:
                raise Exception("Roadmap not found")
                
            if roadmap["user_id"] != user_id:
                raise Exception("Unauthorized: You can only delete your own roadmaps")
                
            # Delete the roadmap
            success = await self.roadmaps_repo.delete_roadmap(roadmap_id)
            if not success:
                raise Exception("Failed to delete roadmap")
                
            return {"message": "Roadmap deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete roadmap: {str(e)}")