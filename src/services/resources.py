from src.repositories.resources import ResourcesRepository
from typing import Optional, List, Dict, Any

class ResourcesService:
    def __init__(self):
        self.resources_repo = ResourcesRepository()

    async def create_resource(self, title: str, platform: str, url: str, cost: str,
                            description: Optional[str] = None, duration_hours: Optional[float] = None,
                            difficulty_level: str = "Beginner", rating: Optional[float] = None) -> Dict[str, Any]:
        """Create a new resource"""
        try:
            resource_id = await self.resources_repo.create_resource(
                title, platform, url, cost, description, duration_hours,
                difficulty_level, rating
            )
            
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Failed to create resource")
                
            return resource
        except Exception as e:
            raise Exception(f"Failed to create resource: {str(e)}")

    async def get_resource_by_id(self, resource_id: str) -> Dict[str, Any]:
        """Get resource by ID"""
        try:
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
            return resource
        except Exception as e:
            raise Exception(f"Failed to get resource: {str(e)}")

    async def get_resources(self, platform: Optional[str] = None, cost: Optional[str] = None,
                           difficulty_level: Optional[str] = None, min_rating: Optional[float] = None,
                           limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all resources with optional filters"""
        try:
            resources = await self.resources_repo.get_resources(
                platform, cost, difficulty_level, min_rating, limit, offset
            )
            return {
                "resources": resources,
                "total": len(resources),
                "limit": limit,
                "offset": offset,
                "filters": {
                    "platform": platform,
                    "cost": cost,
                    "difficulty_level": difficulty_level,
                    "min_rating": min_rating
                }
            }
        except Exception as e:
            raise Exception(f"Failed to get resources: {str(e)}")

    async def update_resource(self, resource_id: str, **kwargs) -> Dict[str, Any]:
        """Update resource details"""
        try:
            # First verify the resource exists
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            # Update the resource
            success = await self.resources_repo.update_resource(resource_id, **kwargs)
            if not success:
                raise Exception("Failed to update resource")
                
            # Return updated resource
            updated_resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not updated_resource:
                raise Exception("Failed to retrieve updated resource")
            return updated_resource
        except Exception as e:
            raise Exception(f"Failed to update resource: {str(e)}")

    async def delete_resource(self, resource_id: str) -> Dict[str, str]:
        """Delete a resource"""
        try:
            # First verify the resource exists
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            # Delete the resource
            success = await self.resources_repo.delete_resource(resource_id)
            if not success:
                raise Exception("Failed to delete resource")
                
            return {"message": "Resource deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete resource: {str(e)}")

    async def add_skill_to_resource(self, resource_id: str, skill_id: str) -> Dict[str, Any]:
        """Add a skill to a resource"""
        try:
            # First verify the resource exists
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            # Add skill to resource
            resource_skill_id = await self.resources_repo.add_skill_to_resource(resource_id, skill_id)
            
            # Return resource skills
            skills = await self.resources_repo.get_resource_skills(resource_id)
            return {
                "resource_id": resource_id,
                "skills": skills,
                "message": "Skill added to resource successfully"
            }
        except Exception as e:
            raise Exception(f"Failed to add skill to resource: {str(e)}")

    async def get_resource_skills(self, resource_id: str) -> Dict[str, Any]:
        """Get all skills for a resource"""
        try:
            # First verify the resource exists
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            skills = await self.resources_repo.get_resource_skills(resource_id)
            return {
                "resource_id": resource_id,
                "skills": skills,
                "total_skills": len(skills)
            }
        except Exception as e:
            raise Exception(f"Failed to get resource skills: {str(e)}")

    async def remove_skill_from_resource(self, resource_id: str, skill_id: str) -> Dict[str, str]:
        """Remove a skill from a resource"""
        try:
            # First verify the resource exists
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            # Remove skill from resource
            success = await self.resources_repo.remove_skill_from_resource(resource_id, skill_id)
            if not success:
                raise Exception("Failed to remove skill from resource")
                
            return {"message": "Skill removed from resource successfully"}
        except Exception as e:
            raise Exception(f"Failed to remove skill from resource: {str(e)}")

    async def start_resource_progress(self, user_id: str, resource_id: str) -> Dict[str, Any]:
        """Start tracking progress for a resource"""
        try:
            # First verify the resource exists and is active
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            # Check if user already has a progress record
            has_progress = await self.resources_repo.user_has_progress_record(user_id, resource_id)
            if has_progress:
                # Get existing progress
                progress = await self.resources_repo.get_user_progress(user_id, resource_id)
                if progress:
                    return progress
                else:
                    raise Exception("Failed to retrieve existing progress")
                
            # Create new progress record
            progress_id = await self.resources_repo.create_user_progress(user_id, resource_id)
            
            # Return progress details
            progress = await self.resources_repo.get_user_progress(user_id, resource_id)
            if not progress:
                raise Exception("Failed to retrieve progress")
            return progress
        except Exception as e:
            raise Exception(f"Failed to start resource progress: {str(e)}")

    async def update_resource_progress(self, user_id: str, resource_id: str, 
                                     status: Optional[str] = None, progress_percentage: Optional[int] = None,
                                     test_taken: Optional[bool] = None, test_score: Optional[int] = None,
                                     test_passed: Optional[bool] = None) -> Dict[str, Any]:
        """Update user progress for a resource"""
        try:
            # First verify the resource exists
            resource = await self.resources_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
                
            # Check if user has a progress record
            progress = await self.resources_repo.get_user_progress(user_id, resource_id)
            if not progress:
                raise Exception("User progress record not found")
                
            # Update progress
            success = await self.resources_repo.update_user_progress(
                progress["id"], status=status, progress_percentage=progress_percentage,
                test_taken=test_taken, test_score=test_score, test_passed=test_passed
            )
            if not success:
                raise Exception("Failed to update progress")
                
            # Return updated progress
            updated_progress = await self.resources_repo.get_user_progress(user_id, resource_id)
            if not updated_progress:
                raise Exception("Failed to retrieve updated progress")
            return updated_progress
        except Exception as e:
            raise Exception(f"Failed to update resource progress: {str(e)}")

    async def get_user_progress(self, user_id: str, resource_id: str) -> Dict[str, Any]:
        """Get user progress for a specific resource"""
        try:
            progress = await self.resources_repo.get_user_progress(user_id, resource_id)
            if not progress:
                raise Exception("Progress not found")
            return progress
        except Exception as e:
            raise Exception(f"Failed to get user progress: {str(e)}")

    async def get_user_resources_progress(self, user_id: str, status: Optional[str] = None,
                                         limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all resources progress for a user"""
        try:
            progress = await self.resources_repo.get_user_resources_progress(user_id, status, limit, offset)
            return {
                "user_id": user_id,
                "progress": progress,
                "total": len(progress),
                "limit": limit,
                "offset": offset,
                "status_filter": status
            }
        except Exception as e:
            raise Exception(f"Failed to get user resources progress: {str(e)}")