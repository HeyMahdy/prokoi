from src.core.database import db
import uuid
from typing import Optional, List, Dict, Any

class JobsRepository:
    async def create_job(self, recruiter_id: str, title: str, company: str, location: str,
                        is_remote: bool, recommended_experience: str, job_type: str,
                        description: str, requirements: Optional[str] = None,
                        responsibilities: Optional[str] = None, salary_range: Optional[str] = None,
                        application_deadline: Optional[str] = None) -> str:
        """Create a new job posting"""
        job_id = str(uuid.uuid4())
        query = """
        INSERT INTO jobs (id, recruiter_id, title, company, location, is_remote,
                         recommended_experience, job_type, description, requirements,
                         responsibilities, salary_range, application_deadline)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [job_id, recruiter_id, title, company, location, is_remote,
                 recommended_experience, job_type, description, requirements,
                 responsibilities, salary_range, application_deadline]
        await db.execute_insert(query, params)
        return job_id

    async def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job by ID"""
        query = """
        SELECT id, recruiter_id, title, company, location, is_remote,
               recommended_experience, job_type, description, requirements,
               responsibilities, salary_range, application_deadline, posted_date,
               is_active, created_at, updated_at
        FROM jobs
        WHERE id = %s AND is_active = TRUE
        """
        rows = await db.execute_query(query, (job_id,))
        return rows[0] if rows else None

    async def get_jobs_by_recruiter(self, recruiter_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all jobs posted by a recruiter"""
        query = """
        SELECT id, recruiter_id, title, company, location, is_remote,
               recommended_experience, job_type, description, requirements,
               responsibilities, salary_range, application_deadline, posted_date,
               is_active, created_at, updated_at
        FROM jobs
        WHERE recruiter_id = %s
        ORDER BY posted_date DESC
        LIMIT %s OFFSET %s
        """
        return await db.execute_query(query, (recruiter_id, limit, offset))

    async def search_jobs(self, search_term: Optional[str] = None, location: Optional[str] = None,
                         job_type: Optional[str] = None, is_remote: Optional[bool] = None,
                         limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Search jobs with filters"""
        query = """
        SELECT id, recruiter_id, title, company, location, is_remote,
               recommended_experience, job_type, description, requirements,
               responsibilities, salary_range, application_deadline, posted_date,
               is_active, created_at, updated_at
        FROM jobs
        WHERE is_active = TRUE
        """
        params = []
        
        if search_term:
            query += " AND (title LIKE %s OR description LIKE %s OR company LIKE %s)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
            
        if location:
            query += " AND location LIKE %s"
            params.append(f"%{location}%")
            
        if job_type:
            query += " AND job_type = %s"
            params.append(job_type)
            
        if is_remote is not None:
            query += " AND is_remote = %s"
            params.append(is_remote)
            
        query += " ORDER BY posted_date DESC LIMIT %s OFFSET %s"
        params.extend([str(limit), str(offset)])
        
        return await db.execute_query(query, params)

    async def update_job(self, job_id: str, **kwargs) -> bool:
        """Update job details"""
        # Build dynamic query based on provided fields
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if value is not None and key in ['title', 'company', 'location', 'is_remote',
                                           'recommended_experience', 'job_type', 'description',
                                           'requirements', 'responsibilities', 'salary_range',
                                           'application_deadline', 'is_active']:
                updates.append(f"{key} = %s")
                params.append(value)
                
        if not updates:
            return False
            
        query = f"UPDATE jobs SET {', '.join(updates)} WHERE id = %s"
        params.append(job_id)
        
        await db.execute_query(query, params)
        return True

    async def delete_job(self, job_id: str) -> bool:
        """Delete a job (soft delete by setting is_active to False)"""
        query = "UPDATE jobs SET is_active = FALSE WHERE id = %s"
        await db.execute_query(query, (job_id,))
        return True

    async def add_skill_to_job(self, job_id: str, skill_id: str, is_required: bool = True,
                              priority: str = 'Must-have') -> str:
        """Add a skill requirement to a job"""
        job_skill_id = str(uuid.uuid4())
        query = """
        INSERT INTO job_skills (id, job_id, skill_id, is_required, priority)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = [job_skill_id, job_id, skill_id, is_required, priority]
        await db.execute_insert(query, params)
        return job_skill_id

    async def get_job_skills(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all skills for a job"""
        query = """
        SELECT js.id, js.job_id, js.skill_id, s.name as skill_name, 
               js.is_required, js.priority
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.id
        WHERE js.job_id = %s
        ORDER BY js.priority, s.name
        """
        return await db.execute_query(query, (job_id,))

    async def remove_skill_from_job(self, job_id: str, skill_id: str) -> bool:
        """Remove a skill requirement from a job"""
        query = "DELETE FROM job_skills WHERE job_id = %s AND skill_id = %s"
        await db.execute_query(query, (job_id, skill_id))
        return True

    async def create_job_application(self, job_id: str, user_id: str,
                                   cover_letter: Optional[str] = None,
                                   resume_url: Optional[str] = None) -> str:
        """Create a job application"""
        application_id = str(uuid.uuid4())
        query = """
        INSERT INTO job_applications (id, job_id, user_id, cover_letter, resume_url)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = [application_id, job_id, user_id, cover_letter, resume_url]
        await db.execute_insert(query, params)
        return application_id

    async def get_application_by_id(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get job application by ID"""
        query = """
        SELECT id, job_id, user_id, cover_letter, resume_url, status,
               applied_at, reviewed_at, notes
        FROM job_applications
        WHERE id = %s
        """
        rows = await db.execute_query(query, (application_id,))
        return rows[0] if rows else None

    async def get_applications_by_job(self, job_id: str, status: Optional[str] = None,
                                    limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all applications for a job"""
        query = """
        SELECT id, job_id, user_id, cover_letter, resume_url, status,
               applied_at, reviewed_at, notes
        FROM job_applications
        WHERE job_id = %s
        """
        params = [job_id]
        
        if status:
            query += " AND status = %s"
            params.append(status)
            
        query += " ORDER BY applied_at DESC LIMIT %s OFFSET %s"
        params.extend([str(limit), str(offset)])
        
        return await db.execute_query(query, params)

    async def get_applications_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all applications by a user"""
        query = """
        SELECT id, job_id, user_id, cover_letter, resume_url, status,
               applied_at, reviewed_at, notes
        FROM job_applications
        WHERE user_id = %s
        ORDER BY applied_at DESC
        LIMIT %s OFFSET %s
        """
        return await db.execute_query(query, (user_id, str(limit), str(offset)))

    async def update_application_status(self, application_id: str, status: str,
                                      notes: Optional[str] = None) -> bool:
        """Update job application status"""
        query = """
        UPDATE job_applications 
        SET status = %s, reviewed_at = NOW(), notes = %s
        WHERE id = %s
        """
        params = [status, notes, application_id]
        await db.execute_query(query, params)
        return True

    async def user_has_applied_to_job(self, user_id: str, job_id: str) -> bool:
        """Check if user has already applied to a job"""
        query = """
        SELECT 1 FROM job_applications 
        WHERE user_id = %s AND job_id = %s
        LIMIT 1
        """
        rows = await db.execute_query(query, (user_id, job_id))
        return len(rows) > 0