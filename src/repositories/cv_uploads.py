from src.core.database import db
import uuid
from typing import Optional, List, Dict, Any
import json

class CVUploadsRepository:
    async def create_cv_upload(self, user_id: str, file_name: str, file_url: str, 
                              file_type: str, extracted_data: Optional[Dict] = None) -> str:
        """Create a new CV upload record"""
        upload_id = str(uuid.uuid4())
        query = """
        INSERT INTO cv_uploads (id, user_id, file_name, file_url, file_type, extracted_data)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = [upload_id, user_id, file_name, file_url, file_type, 
                 json.dumps(extracted_data) if extracted_data else None]
        await db.execute_insert(query, params)
        return upload_id

    async def get_cv_upload_by_id(self, upload_id: str) -> Optional[Dict[str, Any]]:
        """Get CV upload by ID"""
        query = """
        SELECT id, user_id, file_name, file_url, file_type, extracted_data, uploaded_at
        FROM cv_uploads
        WHERE id = %s
        """
        rows = await db.execute_query(query, (upload_id,))
        if rows:
            # Parse JSON data
            upload = rows[0]
            if isinstance(upload['extracted_data'], str):
                upload['extracted_data'] = json.loads(upload['extracted_data'])
            return upload
        return None

    async def get_user_cv_uploads(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all CV uploads for a user"""
        query = """
        SELECT id, user_id, file_name, file_url, file_type, extracted_data, uploaded_at
        FROM cv_uploads
        WHERE user_id = %s
        ORDER BY uploaded_at DESC
        """
        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        
        rows = await db.execute_query(query, (user_id,))
        # Parse JSON data for each upload
        for row in rows:
            if row['extracted_data'] and isinstance(row['extracted_data'], str):
                row['extracted_data'] = json.loads(row['extracted_data'])
        return rows

    async def delete_cv_upload(self, upload_id: str) -> bool:
        """Delete a CV upload by ID"""
        query = "DELETE FROM cv_uploads WHERE id = %s"
        await db.execute_query(query, (upload_id,))
        return True

    async def get_user_cv_upload_count(self, user_id: str) -> int:
        """Get total CV upload count for a user"""
        query = "SELECT COUNT(*) as count FROM cv_uploads WHERE user_id = %s"
        params = [user_id]
        rows = await db.execute_query(query, params)
        return rows[0]['count'] if rows else 0