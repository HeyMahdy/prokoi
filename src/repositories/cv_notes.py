from src.core.database import db
import uuid
from typing import Optional, Dict, Any

class CVNotesRepository:
    async def create_or_update_cv_notes(self, user_id: str, notes: str) -> str:
        """Create or update CV notes for a user"""
        # First check if notes already exist for this user
        existing_notes = await self.get_user_cv_notes(user_id)
        
        if existing_notes:
            # Update existing notes
            return await self.update_cv_notes(existing_notes['id'], notes)
        else:
            # Create new notes
            note_id = str(uuid.uuid4())
            query = """
            INSERT INTO cv_notes (id, user_id, notes)
            VALUES (%s, %s, %s)
            """
            params = [note_id, user_id, notes]
            await db.execute_insert(query, params)
            return note_id

    async def get_cv_notes_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Get CV notes by ID"""
        query = """
        SELECT id, user_id, notes, created_at, updated_at
        FROM cv_notes
        WHERE id = %s
        """
        rows = await db.execute_query(query, (note_id,))
        return rows[0] if rows else None

    async def get_user_cv_notes(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get CV notes for a user"""
        query = """
        SELECT id, user_id, notes, created_at, updated_at
        FROM cv_notes
        WHERE user_id = %s
        """
        rows = await db.execute_query(query, (user_id,))
        return rows[0] if rows else None

    async def update_cv_notes(self, note_id: str, notes: str) -> str:
        """Update CV notes"""
        query = """
        UPDATE cv_notes 
        SET notes = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        params = [notes, note_id]
        await db.execute_query(query, params)
        return note_id

    async def delete_cv_notes(self, note_id: str) -> bool:
        """Delete CV notes by ID"""
        query = "DELETE FROM cv_notes WHERE id = %s"
        await db.execute_query(query, (note_id,))
        return True