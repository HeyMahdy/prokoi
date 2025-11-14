from src.repositories.cv_uploads import CVUploadsRepository
from typing import Optional, List, Dict, Any

class CVUploadsService:
    def __init__(self):
        self.uploads_repo = CVUploadsRepository()

    async def create_cv_upload(self, user_id: str, file_name: str, file_url: str, 
                              file_type: str, extracted_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new CV upload record"""
        try:
            upload_id = await self.uploads_repo.create_cv_upload(
                user_id, file_name, file_url, file_type, extracted_data
            )
            
            upload = await self.uploads_repo.get_cv_upload_by_id(upload_id)
            if not upload:
                raise Exception("Failed to create CV upload")
                
            return upload
        except Exception as e:
            raise Exception(f"Failed to create CV upload: {str(e)}")

    async def get_cv_upload_by_id(self, upload_id: str, user_id: str) -> Dict[str, Any]:
        """Get CV upload by ID"""
        try:
            upload = await self.uploads_repo.get_cv_upload_by_id(upload_id)
            if not upload:
                raise Exception("CV upload not found")
                
            # Check if user owns this upload
            if upload["user_id"] != user_id:
                raise Exception("Unauthorized: You can only access your own CV uploads")
                
            return upload
        except Exception as e:
            raise Exception(f"Failed to get CV upload: {str(e)}")

    async def get_user_cv_uploads(self, user_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all CV uploads for a user"""
        try:
            uploads = await self.uploads_repo.get_user_cv_uploads(user_id, limit, offset)
            total_count = await self.uploads_repo.get_user_cv_upload_count(user_id)
            
            return {
                "uploads": uploads,
                "total": total_count,
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            raise Exception(f"Failed to get user CV uploads: {str(e)}")

    async def delete_cv_upload(self, upload_id: str, user_id: str) -> Dict[str, str]:
        """Delete a CV upload by ID"""
        try:
            # First verify the upload exists and belongs to the user
            upload = await self.uploads_repo.get_cv_upload_by_id(upload_id)
            if not upload:
                raise Exception("CV upload not found")
                
            if upload["user_id"] != user_id:
                raise Exception("Unauthorized: You can only delete your own CV uploads")
                
            # Delete the upload
            success = await self.uploads_repo.delete_cv_upload(upload_id)
            if not success:
                raise Exception("Failed to delete CV upload")
                
            return {"message": "CV upload deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete CV upload: {str(e)}")