from src.core.database import db


class IssueRepository:

    async def create_issue_type(self, name: str):
        """Create a new issue type"""
        query = """
        INSERT INTO issue_types (name) 
        VALUES (%s)
        """
        return await db.execute_insert(query, [name])

    async def get_all_issue_types(self):
        """Get all issue types"""
        query = """
        SELECT id, name 
        FROM issue_types 
        ORDER BY name ASC
        """
        return await db.execute_query(query)

    async def get_issue_type_by_id(self, issue_type_id: int):
        """Get a specific issue type by ID"""
        query = """
        SELECT id, name 
        FROM issue_types 
        WHERE id = %s
        """
        result = await db.execute_query(query, [issue_type_id])
        return result[0] if result else None

    async def update_issue_type(self, issue_type_id: int, name: str):
        """Update an existing issue type"""
        query = """
        UPDATE issue_types 
        SET name = %s
        WHERE id = %s
        """
        return await db.execute_query(query, [name, issue_type_id])

    async def delete_issue_type(self, issue_type_id: int):
        """Delete an issue type"""
        query = """
        DELETE FROM issue_types 
        WHERE id = %s
        """
        return await db.execute_query(query, [issue_type_id])

    async def issue_type_exists(self, name: str):
        """Check if an issue type with the given name exists"""
        query = """
        SELECT COUNT(*) as count 
        FROM issue_types 
        WHERE name = %s
        """
        result = await db.execute_query(query, [name])
        return result[0]['count'] > 0 if result else False

    # Issues CRUD operations
    async def create_issue(self, project_id: int, title: str, created_by: int, 
                          type_id: int = None, description: str = None, 
                          story_points: int = None, status: str = "open", 
                          priority: str = "medium", parent_issue_id: int = None):
        """Create a new issue"""
        query = """
        INSERT INTO issues (project_id, type_id, title, description, story_points, 
                          status, priority, created_by, parent_issue_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
         return await db.execute_insert(query, [project_id, type_id, title, description,
                                              story_points, status, priority, created_by, parent_issue_id])
        except Exception as e:
            print("error in the query",e)

    async def get_issues_by_project(self, project_id: int):
        """Get all issues for a specific project"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.project_id = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id])

    async def get_issue_by_id(self, issue_id: int):
        """Get a specific issue by ID"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.id = %s
        """
        result = await db.execute_query(query, [issue_id])
        return result[0] if result else None

    async def update_issue(self, issue_id: int, **kwargs):
        """Update an existing issue"""
        # Build dynamic query based on provided fields
        set_clauses = []
        values = []
        
        for field, value in kwargs.items():
            if value is not None:
                set_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not set_clauses:
            return None
            
        query = f"""
        UPDATE issues 
        SET {', '.join(set_clauses)}
        WHERE id = %s
        """
        values.append(issue_id)
        return await db.execute_query(query, values)

    async def delete_issue(self, issue_id: int):
        """Delete an issue"""
        query = """
        DELETE FROM issues 
        WHERE id = %s
        """
        return await db.execute_query(query, [issue_id])

    async def get_issues_by_status(self, project_id: int, status: str):
        """Get all issues with a specific status for a project"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.project_id = %s AND i.status = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id, status])

    async def get_issues_by_priority(self, project_id: int, priority: str):
        """Get all issues with a specific priority for a project"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.project_id = %s AND i.priority = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id, priority])

    async def get_sub_issues(self, parent_issue_id: int):
        """Get all sub-issues (children) of a parent issue"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.parent_issue_id = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [parent_issue_id])

    async def issue_exists(self, issue_id: int):
        """Check if an issue exists"""
        query = """
        SELECT COUNT(*) as count 
        FROM issues 
        WHERE id = %s
        """
        result = await db.execute_query(query, [issue_id])
        return result[0]['count'] > 0 if result else False




