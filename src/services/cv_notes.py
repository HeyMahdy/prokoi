from src.repositories.cv_notes import CVNotesRepository
from typing import Optional, Dict, Any

class CVNotesService:
    def __init__(self):
        self.notes_repo = CVNotesRepository()

    async def create_or_update_cv_notes(self, user_id: str, notes: str) -> Dict[str, Any]:
        """Create or update CV notes for a user"""
        try:
            note_id = await self.notes_repo.create_or_update_cv_notes(user_id, notes)
            
            note = await self.notes_repo.get_cv_notes_by_id(note_id)
            if not note:
                raise Exception("Failed to create/update CV notes")
                
            return note
        except Exception as e:
            raise Exception(f"Failed to create/update CV notes: {str(e)}")

    async def get_user_cv_notes(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get CV notes for a user"""
        try:
            notes = await self.notes_repo.get_user_cv_notes(user_id)
            return notes
        except Exception as e:
            raise Exception(f"Failed to get CV notes: {str(e)}")

    async def update_cv_notes(self, note_id: str, user_id: str, notes: str) -> Dict[str, Any]:
        """Update CV notes"""
        try:
            # First verify the notes exist and belong to the user
            existing_notes = await self.notes_repo.get_cv_notes_by_id(note_id)
            if not existing_notes:
                raise Exception("CV notes not found")
                
            if existing_notes["user_id"] != user_id:
                raise Exception("Unauthorized: You can only update your own CV notes")
                
            updated_note_id = await self.notes_repo.update_cv_notes(note_id, notes)
            
            updated_notes = await self.notes_repo.get_cv_notes_by_id(updated_note_id)
            if not updated_notes:
                raise Exception("Failed to update CV notes")
                
            return updated_notes
        except Exception as e:
            raise Exception(f"Failed to update CV notes: {str(e)}")

    async def delete_cv_notes(self, note_id: str, user_id: str) -> Dict[str, str]:
        """Delete CV notes by ID"""
        try:
            # First verify the notes exist and belong to the user
            notes = await self.notes_repo.get_cv_notes_by_id(note_id)
            if not notes:
                raise Exception("CV notes not found")
                
            if notes["user_id"] != user_id:
                raise Exception("Unauthorized: You can only delete your own CV notes")
                
            # Delete the notes
            success = await self.notes_repo.delete_cv_notes(note_id)
            if not success:
                raise Exception("Failed to delete CV notes")
                
            return {"message": "CV notes deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete CV notes: {str(e)}")