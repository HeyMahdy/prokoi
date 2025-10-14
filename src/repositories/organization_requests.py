from src.core.database import db

class OrganizationRequestsRepository:
    async def get_outgoing_requests(self, sender_id: int) -> list[dict]:
        """Get all outgoing requests sent by a user"""
        query = """
        SELECT oor.id, oor.organization_id, oor.sender_id, oor.receiver_id, oor.status, 
               oor.created_at, oor.updated_at,
               o.name as organization_name,
               u.name as receiver_name, u.email as receiver_email
        FROM organization_outgoing_requests oor
        JOIN organizations o ON oor.organization_id = o.id
        JOIN users u ON oor.receiver_id = u.id
        WHERE oor.sender_id = %s
        ORDER BY oor.created_at DESC
        """
        return await db.execute_query(query, (sender_id,))

    async def get_incoming_requests(self, receiver_id: int) -> list[dict]:
        """Get all incoming requests for a user"""
        query = """
        SELECT oor.id, oor.organization_id, oor.sender_id, oor.receiver_id, oor.status,
               oor.created_at, oor.updated_at,
               o.name as organization_name,
               u.name as sender_name, u.email as sender_email
        FROM organization_outgoing_requests oor
        JOIN organizations o ON oor.organization_id = o.id
        JOIN users u ON oor.sender_id = u.id
        WHERE oor.receiver_id = %s
        ORDER BY oor.created_at DESC
        """
        return await db.execute_query(query, (receiver_id,))

    async def create_outgoing_request(self, organization_id: int, sender_id: int, receiver_id: int) -> int:
        """Create a new outgoing request"""
        query = """
        INSERT INTO organization_outgoing_requests (organization_id, sender_id, receiver_id)
        VALUES (%s, %s, %s)
        """
        return await db.execute_insert(query, (organization_id, sender_id, receiver_id))

    async def update_request_status(self, request_id: int, status: str, user_id: int) -> bool:
        """Update request status (only receiver can accept/reject)"""
        query = """
        UPDATE organization_outgoing_requests 
        SET status = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s AND receiver_id = %s
        """
        await db.execute_query(query, (status, request_id, user_id))
        return True

    async def get_request_by_id(self, request_id: int, user_id: int) -> dict | None:
        """Get request by ID (sender or receiver)"""
        query = """
        SELECT oor.id, oor.organization_id, oor.sender_id, oor.receiver_id, oor.status,
               oor.created_at, oor.updated_at,
               o.name as organization_name,
               s.name as sender_name, s.email as sender_email,
               r.name as receiver_name, r.email as receiver_email
        FROM organization_outgoing_requests oor
        JOIN organizations o ON oor.organization_id = o.id
        JOIN users s ON oor.sender_id = s.id
        JOIN users r ON oor.receiver_id = r.id
        WHERE oor.id = %s AND (oor.sender_id = %s OR oor.receiver_id = %s)
        LIMIT 1
        """
        rows = await db.execute_query(query, (request_id, user_id, user_id))
        return rows[0] if rows else None

    async def user_has_org_access(self, user_id: int, organization_id: int) -> bool:
        """Check if user has access to organization"""
        query = """
        SELECT 1
        FROM organization_users ou
        WHERE ou.organization_id = %s AND ou.user_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (organization_id, user_id))
        return len(rows) > 0