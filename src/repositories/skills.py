from src.core.database import db
import aiomysql

class SkillsRepository:
    async def get_all_skills(self) :
        """Get all skills"""
        query = """
        SELECT id, name
        FROM skills
        ORDER BY name ASC
        """
        return await db.execute_query(query)

    async def get_skill_by_id(self, skill_id: int) -> dict | None:
        """Get skill by ID"""
        query = """
        SELECT id, name
        FROM skills
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (skill_id,))
        return rows[0] if rows else None

    async def get_skill_by_name(self, name: str) -> dict | None:
        """Get skill by name"""
        query = """
        SELECT id, name
        FROM skills
        WHERE name = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (name,))
        return rows[0] if rows else None

    async def create_skill(self, name: str) -> int:
        """Create a new skill"""
        query = """
        INSERT INTO skills (name)
        VALUES (%s)
        """
        return await db.execute_insert(query, (name,))

    async def get_user_skills(self, user_id: int) -> list[dict]:
        """Get all skills for a user"""
        query = """
        SELECT us.id, us.user_id, us.skill_id, s.name as skill_name
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (user_id,))

    async def get_user_skill(self, user_id: int, skill_id: int) -> dict | None:
        """Get specific user skill"""
        query = """
        SELECT us.id, us.user_id, us.skill_id, s.name as skill_name
        FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id = %s AND us.skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return rows[0] if rows else None

    async def add_skill_to_user(self, user_id: int, skill_id: int) -> int:
        """Add skill to user"""
        query = """
        INSERT INTO user_skills (user_id, skill_id)
        VALUES (%s, %s)
        """
        return await db.execute_insert(query, (user_id, skill_id))

    async def remove_user_skill(self, user_id: int, skill_id: int) -> bool:
        """Remove skill from user"""
        query = """
        DELETE FROM user_skills
        WHERE user_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (user_id, skill_id))
        return True

    async def user_has_skill(self, user_id: int, skill_id: int) -> bool:
        """Check if user has a specific skill"""
        query = """
        SELECT 1
        FROM user_skills
        WHERE user_id = %s AND skill_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return len(rows) > 0

    async def get_all_jobs(self, limit: int = 100, offset: int = 0) -> list[dict]:
        """Get all jobs with pagination"""
        query = """
        SELECT id, title, company, location, experience_required, 
               job_type, description, created_at
        FROM jobs
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        return await db.execute_query(query, (limit, offset))

    async def get_job_by_id(self, job_id: int) -> dict | None:
        """Get job by ID"""
        query = """
        SELECT id, title, company, location, experience_required, 
               job_type, description, created_at
        FROM jobs
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (job_id,))
        return rows[0] if rows else None

    async def create_job(self, title: str, company: str, location: str ,
                        experience_required: str , job_type: str ,
                        description: str ) -> int:
        """Create a new job"""
        query = """
        INSERT INTO jobs (title, company, location, experience_required, job_type, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return await db.execute_insert(query, (title, company, location, 
                                               experience_required, job_type, description))

    async def search_jobs_by_title(self, title: str) -> list[dict]:
        """Search jobs by title"""
        query = """
        SELECT id, title, company, location, experience_required, 
               job_type, description, created_at
        FROM jobs
        WHERE title LIKE %s
        ORDER BY created_at DESC
        """
        return await db.execute_query(query, (f"%{title}%",))

    async def get_jobs_by_type(self, job_type: str) -> list[dict]:
        """Get jobs by type"""
        query = """
        SELECT id, title, company, location, experience_required, 
               job_type, description, created_at
        FROM jobs
        WHERE job_type = %s
        ORDER BY created_at DESC
        """
        return await db.execute_query(query, (job_type,))



    async def get_job_required_skills(self, job_id: int) -> list[dict]:
        """Get all required skills for a job"""
        query = """
        SELECT jrs.id, jrs.job_id, jrs.skill_id, s.name as skill_name
        FROM job_required_skills jrs
        JOIN skills s ON jrs.skill_id = s.id
        WHERE jrs.job_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (job_id,))

    async def add_required_skill_to_job(self, job_id: int, skill_id: int) -> int:
        """Add required skill to job"""
        query = """
        INSERT INTO job_required_skills (job_id, skill_id)
        VALUES (%s, %s)
        """
        return await db.execute_insert(query, (job_id, skill_id))

    async def remove_required_skill_from_job(self, job_id: int, skill_id: int) -> bool:
        """Remove required skill from job"""
        query = """
        DELETE FROM job_required_skills
        WHERE job_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (job_id, skill_id))
        return True

    async def get_jobs_by_skill(self, skill_id: int) -> list[dict]:
        """Get all jobs requiring a specific skill"""
        query = """
        SELECT j.id, j.title, j.company, j.location, j.experience_required, 
               j.job_type, j.description, j.created_at
        FROM jobs j
        JOIN job_required_skills jrs ON j.id = jrs.job_id
        WHERE jrs.skill_id = %s
        ORDER BY j.created_at DESC
        """
        return await db.execute_query(query, (skill_id,))

    async def get_matching_jobs_for_user(self, user_id: int) -> list[dict]:
        """Get jobs that match user's skills"""
        query = """
        SELECT DISTINCT j.id, j.title, j.company, j.location, 
               j.experience_required, j.job_type, j.description, j.created_at,
               COUNT(jrs.skill_id) as matching_skills
        FROM jobs j
        JOIN job_required_skills jrs ON j.id = jrs.job_id
        JOIN user_skills us ON jrs.skill_id = us.skill_id
        WHERE us.user_id = %s
        GROUP BY j.id
        ORDER BY matching_skills DESC, j.created_at DESC
        """
        return await db.execute_query(query, (user_id,))

    async def get_all_resources(self, limit: int = 100, offset: int = 0) -> list[dict]:
        """Get all learning resources with pagination"""
        query = """
        SELECT id, title, platform, url, cost, created_at
        FROM learning_resources
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        return await db.execute_query(query, (limit, offset))

    async def get_resource_by_id(self, resource_id: int) -> dict | None:
        """Get learning resource by ID"""
        query = """
        SELECT id, title, platform, url, cost, created_at
        FROM learning_resources
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (resource_id,))
        return rows[0] if rows else None

    async def create_resource(self, title: str, platform:str,
                             url: str, cost: str ) -> int:
        """Create a new learning resource"""
        query = """
        INSERT INTO learning_resources (title, platform, url, cost)
        VALUES (%s, %s, %s, %s)
        """
        return await db.execute_insert(query, (title, platform, url, cost))

    async def get_resources_by_platform(self, platform: str) -> list[dict]:
        """Get resources by platform"""
        query = """
        SELECT id, title, platform, url, cost, created_at
        FROM learning_resources
        WHERE platform = %s
        ORDER BY created_at DESC
        """
        return await db.execute_query(query, (platform,))

    async def get_free_resources(self) -> list[dict]:
        """Get all free resources"""
        query = """
        SELECT id, title, platform, url, cost, created_at
        FROM learning_resources
        WHERE cost = 'Free'
        ORDER BY created_at DESC
        """
        return await db.execute_query(query)


    async def get_resource_skills(self, resource_id: int) -> list[dict]:
        """Get all skills covered by a resource"""
        query = """
        SELECT rs.id, rs.resource_id, rs.skill_id, s.name as skill_name
        FROM resource_skills rs
        JOIN skills s ON rs.skill_id = s.id
        WHERE rs.resource_id = %s
        ORDER BY s.name ASC
        """
        return await db.execute_query(query, (resource_id,))

    async def add_skill_to_resource(self, resource_id: int, skill_id: int) -> int:
        """Add skill to learning resource"""
        query = """
        INSERT INTO resource_skills (resource_id, skill_id)
        VALUES (%s, %s)
        """
        return await db.execute_insert(query, (resource_id, skill_id))

    async def remove_skill_from_resource(self, resource_id: int, skill_id: int) -> bool:
        """Remove skill from learning resource"""
        query = """
        DELETE FROM resource_skills
        WHERE resource_id = %s AND skill_id = %s
        """
        await db.execute_query(query, (resource_id, skill_id))
        return True

    async def get_resources_by_skill(self, skill_id: int) -> list[dict]:
        """Get all resources that teach a specific skill"""
        query = """
        SELECT lr.id, lr.title, lr.platform, lr.url, lr.cost, lr.created_at
        FROM learning_resources lr
        JOIN resource_skills rs ON lr.id = rs.resource_id
        WHERE rs.skill_id = %s
        ORDER BY lr.created_at DESC
        """
        return await db.execute_query(query, (skill_id,))

    async def get_recommended_resources_for_user(self, user_id: int) -> list[dict]:
        """Get recommended resources based on skills user doesn't have"""
        query = """
        SELECT DISTINCT lr.id, lr.title, lr.platform, lr.url, lr.cost, lr.created_at
        FROM learning_resources lr
        JOIN resource_skills rs ON lr.id = rs.resource_id
        WHERE rs.skill_id NOT IN (
            SELECT skill_id FROM user_skills WHERE user_id = %s
        )
        ORDER BY lr.created_at DESC
        """
        return await db.execute_query(query, (user_id,))



    async def get_user_experiences(self, user_id: int) -> list[dict]:
        """Get all experiences for a user"""
        query = """
        SELECT id, user_id, title, description, created_at
        FROM user_experience
        WHERE user_id = %s
        ORDER BY created_at DESC
        """
        return await db.execute_query(query, (user_id,))

    async def get_experience_by_id(self, experience_id: int) -> dict | None:
        """Get experience by ID"""
        query = """
        SELECT id, user_id, title, description, created_at
        FROM user_experience
        WHERE id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (experience_id,))
        return rows[0] if rows else None

    async def create_experience(self, user_id: int, title: str, 
                               description: str) -> int:
        """Create a new user experience"""
        query = """
        INSERT INTO user_experience (user_id, title, description)
        VALUES (%s, %s, %s)
        """
        return await db.execute_insert(query, (user_id, title, description))

    async def update_experience(self, experience_id: int, title: str ,
                               description: str ) -> bool:
        """Update user experience"""
        if title and description:
            query = """
            UPDATE user_experience
            SET title = %s, description = %s
            WHERE id = %s
            """
            await db.execute_query(query, (title, description, experience_id))
        elif title:
            query = """
            UPDATE user_experience
            SET title = %s
            WHERE id = %s
            """
            await db.execute_query(query, (title, experience_id))
        elif description:
            query = """
            UPDATE user_experience
            SET description = %s
            WHERE id = %s
            """
            await db.execute_query(query, (description, experience_id))
        return True

    async def delete_experience(self, experience_id: int) -> bool:
        """Delete user experience"""
        query = """
        DELETE FROM user_experience
        WHERE id = %s
        """
        await db.execute_query(query, (experience_id,))
        return True
