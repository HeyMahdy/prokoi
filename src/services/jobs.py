from src.repositories.jobs import JobsRepository
from typing import Optional, List, Dict, Any

class JobsService:
    def __init__(self):
        self.jobs_repo = JobsRepository()

    async def create_job(self, recruiter_id: str, title: str, company: str, location: str,
                        is_remote: bool, recommended_experience: str, job_type: str,
                        description: str, requirements: Optional[str] = None,
                        responsibilities: Optional[str] = None, salary_range: Optional[str] = None,
                        application_deadline: Optional[str] = None) -> Dict[str, Any]:
        """Create a new job posting"""
        try:
            job_id = await self.jobs_repo.create_job(
                recruiter_id, title, company, location, is_remote,
                recommended_experience, job_type, description, requirements,
                responsibilities, salary_range, application_deadline
            )
            
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Failed to create job")
                
            return job
        except Exception as e:
            raise Exception(f"Failed to create job: {str(e)}")

    async def get_job_by_id(self, job_id: str) -> Dict[str, Any]:
        """Get job by ID"""
        try:
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
            return job
        except Exception as e:
            raise Exception(f"Failed to get job: {str(e)}")

    async def get_jobs_by_recruiter(self, recruiter_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all jobs posted by a recruiter"""
        try:
            jobs = await self.jobs_repo.get_jobs_by_recruiter(recruiter_id, limit, offset)
            return {
                "jobs": jobs,
                "total": len(jobs),
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            raise Exception(f"Failed to get jobs: {str(e)}")

    async def search_jobs(self, search_term: Optional[str] = None, location: Optional[str] = None,
                         job_type: Optional[str] = None, is_remote: Optional[bool] = None,
                         limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Search jobs with filters"""
        try:
            jobs = await self.jobs_repo.search_jobs(search_term, location, job_type, is_remote, limit, offset)
            return {
                "jobs": jobs,
                "total": len(jobs),
                "limit": limit,
                "offset": offset,
                "filters": {
                    "search_term": search_term,
                    "location": location,
                    "job_type": job_type,
                    "is_remote": is_remote
                }
            }
        except Exception as e:
            raise Exception(f"Failed to search jobs: {str(e)}")

    async def update_job(self, job_id: str, recruiter_id: str, **kwargs) -> Dict[str, Any]:
        """Update job details"""
        try:
            # First verify the job exists and belongs to the recruiter
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            if job["recruiter_id"] != recruiter_id:
                raise Exception("Unauthorized: You can only update your own jobs")
                
            # Update the job
            success = await self.jobs_repo.update_job(job_id, **kwargs)
            if not success:
                raise Exception("Failed to update job")
                
            # Return updated job
            updated_job = await self.jobs_repo.get_job_by_id(job_id)
            if not updated_job:
                raise Exception("Failed to retrieve updated job")
            return updated_job
        except Exception as e:
            raise Exception(f"Failed to update job: {str(e)}")

    async def delete_job(self, job_id: str, recruiter_id: str) -> Dict[str, str]:
        """Delete a job"""
        try:
            # First verify the job exists and belongs to the recruiter
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            if job["recruiter_id"] != recruiter_id:
                raise Exception("Unauthorized: You can only delete your own jobs")
                
            # Delete the job
            success = await self.jobs_repo.delete_job(job_id)
            if not success:
                raise Exception("Failed to delete job")
                
            return {"message": "Job deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete job: {str(e)}")

    async def add_skill_to_job(self, job_id: str, recruiter_id: str, skill_id: str,
                              is_required: bool = True, priority: str = 'Must-have') -> Dict[str, Any]:
        """Add a skill requirement to a job"""
        try:
            # First verify the job exists and belongs to the recruiter
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            if job["recruiter_id"] != recruiter_id:
                raise Exception("Unauthorized: You can only modify your own jobs")
                
            # Add skill to job
            job_skill_id = await self.jobs_repo.add_skill_to_job(job_id, skill_id, is_required, priority)
            
            # Return job skills
            skills = await self.jobs_repo.get_job_skills(job_id)
            return {
                "job_id": job_id,
                "skills": skills,
                "message": "Skill added to job successfully"
            }
        except Exception as e:
            raise Exception(f"Failed to add skill to job: {str(e)}")

    async def get_job_skills(self, job_id: str) -> Dict[str, Any]:
        """Get all skills for a job"""
        try:
            # First verify the job exists
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            skills = await self.jobs_repo.get_job_skills(job_id)
            return {
                "job_id": job_id,
                "skills": skills,
                "total_skills": len(skills)
            }
        except Exception as e:
            raise Exception(f"Failed to get job skills: {str(e)}")

    async def remove_skill_from_job(self, job_id: str, recruiter_id: str, skill_id: str) -> Dict[str, str]:
        """Remove a skill requirement from a job"""
        try:
            # First verify the job exists and belongs to the recruiter
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            if job["recruiter_id"] != recruiter_id:
                raise Exception("Unauthorized: You can only modify your own jobs")
                
            # Remove skill from job
            success = await self.jobs_repo.remove_skill_from_job(job_id, skill_id)
            if not success:
                raise Exception("Failed to remove skill from job")
                
            return {"message": "Skill removed from job successfully"}
        except Exception as e:
            raise Exception(f"Failed to remove skill from job: {str(e)}")

    async def apply_to_job(self, job_id: str, user_id: str, cover_letter: Optional[str] = None,
                          resume_url: Optional[str] = None) -> Dict[str, Any]:
        """Apply to a job"""
        try:
            # First verify the job exists and is active
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            if not job["is_active"]:
                raise Exception("Job is no longer accepting applications")
                
            # Check if user has already applied
            already_applied = await self.jobs_repo.user_has_applied_to_job(user_id, job_id)
            if already_applied:
                raise Exception("You have already applied to this job")
                
            # Create application
            application_id = await self.jobs_repo.create_job_application(
                job_id, user_id, cover_letter, resume_url
            )
            
            # Return application details
            application = await self.jobs_repo.get_application_by_id(application_id)
            if not application:
                raise Exception("Failed to retrieve application")
            return application
        except Exception as e:
            raise Exception(f"Failed to apply to job: {str(e)}")

    async def get_application_by_id(self, application_id: str, user_id: str) -> Dict[str, Any]:
        """Get job application by ID"""
        try:
            application = await self.jobs_repo.get_application_by_id(application_id)
            if not application:
                raise Exception("Application not found")
                
            # Check if user has permission to view this application
            user_jobs = await self.jobs_repo.get_jobs_by_recruiter(user_id)
            user_job_ids = [job["id"] for job in user_jobs] if user_jobs else []
            
            if application["user_id"] != user_id and application["job_id"] not in user_job_ids:
                raise Exception("Unauthorized: You can only view your own applications or applications to your jobs")
                
            return application
        except Exception as e:
            raise Exception(f"Failed to get application: {str(e)}")

    async def get_applications_by_job(self, job_id: str, recruiter_id: str, status: Optional[str] = None,
                                     limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all applications for a job"""
        try:
            # First verify the job exists and belongs to the recruiter
            job = await self.jobs_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
                
            if job["recruiter_id"] != recruiter_id:
                raise Exception("Unauthorized: You can only view applications to your own jobs")
                
            applications = await self.jobs_repo.get_applications_by_job(job_id, status, limit, offset)
            return {
                "job_id": job_id,
                "applications": applications,
                "total": len(applications),
                "limit": limit,
                "offset": offset,
                "status_filter": status
            }
        except Exception as e:
            raise Exception(f"Failed to get job applications: {str(e)}")

    async def get_applications_by_user(self, user_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all applications by a user"""
        try:
            applications = await self.jobs_repo.get_applications_by_user(user_id, limit, offset)
            return {
                "user_id": user_id,
                "applications": applications,
                "total": len(applications),
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            raise Exception(f"Failed to get user applications: {str(e)}")

    async def update_application_status(self, application_id: str, recruiter_id: str, status: str,
                                      notes: Optional[str] = None) -> Dict[str, Any]:
        """Update job application status"""
        try:
            # First verify the application exists
            application = await self.jobs_repo.get_application_by_id(application_id)
            if not application:
                raise Exception("Application not found")
                
            # Verify the recruiter owns the job this application is for
            job = await self.jobs_repo.get_job_by_id(application["job_id"])
            if not job:
                raise Exception("Job not found")
                
            if job["recruiter_id"] != recruiter_id:
                raise Exception("Unauthorized: You can only update applications to your own jobs")
                
            # Update application status
            success = await self.jobs_repo.update_application_status(application_id, status, notes)
            if not success:
                raise Exception("Failed to update application status")
                
            # Return updated application
            updated_application = await self.jobs_repo.get_application_by_id(application_id)
            if not updated_application:
                raise Exception("Failed to retrieve updated application")
            return updated_application
        except Exception as e:
            raise Exception(f"Failed to update application status: {str(e)}")