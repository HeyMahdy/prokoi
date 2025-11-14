from src.repositories.skills import SkillsRepository
class AppService:
    def __init__(self):
        self.skills_repo = SkillsRepository()
    async def get_all_skills(self):
        """Get all global skills"""
        try:
            skills = await self.skills_repo.get_all_skills()
            return skills
        except Exception as e:
            print(f"Failed to get skills: {e}")
            raise

    async def get_skill_by_id(self, skill_id: int):
        """Get skill by ID"""
        try:
            skill = await self.skills_repo.get_skill_by_id(skill_id)
            if not skill:
                raise Exception("Skill not found")
            return skill
        except Exception as e:
            print(f"Failed to get skill: {e}")
            raise

    async def get_skill_by_name(self, name: str):
        """Get skill by name"""
        try:
            skill = await self.skills_repo.get_skill_by_name(name)
            if not skill:
                raise Exception("Skill not found")
            return skill
        except Exception as e:
            print(f"Failed to get skill: {e}")
            raise

    async def create_skill(self, name: str):
        """Create a new skill"""
        existing_skill = await self.skills_repo.get_skill_by_name(name)
        if existing_skill:
            raise Exception("Skill already exists")

        try:
            skill_id = await self.skills_repo.create_skill(name)
            skill = await self.skills_repo.get_skill_by_id(skill_id)
            return skill
        except Exception as e:
            print(f"Failed to create skill: {e}")
            raise

    # ===========================================================
    # USER SKILLS METHODS
    # ===========================================================
    async def get_user_skills(self, user_id: int):
        """Get all skills for a user"""
        try:
            user_skills = await self.skills_repo.get_user_skills(user_id)
            return {
                "user_id": user_id,
                "skills": user_skills,
                "total_skills": len(user_skills)
            }
        except Exception as e:
            print(f"Failed to get user skills: {e}")
            raise

    async def get_user_skill(self, user_id: int, skill_id: int):
        """Get specific user skill"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            user_skill = await self.skills_repo.get_user_skill(user_id, skill_id)
            if not user_skill:
                raise Exception("User does not have this skill")
            return user_skill
        except Exception as e:
            print(f"Failed to get user skill: {e}")
            raise

    async def add_skill_to_user(self, user_id: int, skill_id: int):
        """Add skill to user"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        user_has_skill = await self.skills_repo.user_has_skill(user_id, skill_id)
        if user_has_skill:
            raise Exception("User already has this skill")

        try:
            user_skill_id = await self.skills_repo.add_skill_to_user(user_id, skill_id)
            user_skill = await self.skills_repo.get_user_skill(user_id, skill_id)
            return user_skill
        except Exception as e:
            print(f"Failed to add skill to user: {e}")
            raise

    async def remove_user_skill(self, user_id: int, skill_id: int):
        """Remove skill from user"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        user_has_skill = await self.skills_repo.user_has_skill(user_id, skill_id)
        if not user_has_skill:
            raise Exception("User does not have this skill")

        try:
            await self.skills_repo.remove_user_skill(user_id, skill_id)
            return {"message": "Skill removed from user successfully"}
        except Exception as e:
            print(f"Failed to remove user skill: {e}")
            raise

    # ===========================================================
    # JOBS METHODS
    # ===========================================================
    async def get_all_jobs(self, limit: int = 100, offset: int = 0):
        """Get all jobs with pagination"""
        try:
            jobs = await self.skills_repo.get_all_jobs(limit, offset)
            return {
                "jobs": jobs,
                "total": len(jobs),
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            print(f"Failed to get jobs: {e}")
            raise

    async def get_job_by_id(self, job_id: int):
        """Get job by ID"""
        try:
            job = await self.skills_repo.get_job_by_id(job_id)
            if not job:
                raise Exception("Job not found")
            return job
        except Exception as e:
            print(f"Failed to get job: {e}")
            raise

    async def create_job(self, title: str, company: str, location: str,
                        experience_required: str , job_type: str ,
                        description: str ):
        """Create a new job"""
        try:
            job_id = await self.skills_repo.create_job(
                title, company, location, experience_required, job_type, description
            )
            job = await self.skills_repo.get_job_by_id(job_id)
            return job
        except Exception as e:
            print(f"Failed to create job: {e}")
            raise

    async def search_jobs_by_title(self, title: str):
        """Search jobs by title"""
        try:
            jobs = await self.skills_repo.search_jobs_by_title(title)
            return {
                "jobs": jobs,
                "total": len(jobs),
                "search_term": title
            }
        except Exception as e:
            print(f"Failed to search jobs: {e}")
            raise

    async def get_jobs_by_type(self, job_type: str):
        """Get jobs by type"""
        try:
            jobs = await self.skills_repo.get_jobs_by_type(job_type)
            return {
                "jobs": jobs,
                "total": len(jobs),
                "job_type": job_type
            }
        except Exception as e:
            print(f"Failed to get jobs by type: {e}")
            raise

    # ===========================================================
    # JOB REQUIRED SKILLS METHODS
    # ===========================================================
    async def get_job_required_skills(self, job_id: int):
        """Get all required skills for a job"""
        job = await self.skills_repo.get_job_by_id(job_id)
        if not job:
            raise Exception("Job not found")

        try:
            skills = await self.skills_repo.get_job_required_skills(job_id)
            return {
                "job_id": job_id,
                "required_skills": skills,
                "total_skills": len(skills)
            }
        except Exception as e:
            print(f"Failed to get job required skills: {e}")
            raise

    async def add_required_skill_to_job(self, job_id: int, skill_id: int):
        """Add required skill to job"""
        job = await self.skills_repo.get_job_by_id(job_id)
        if not job:
            raise Exception("Job not found")

        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            await self.skills_repo.add_required_skill_to_job(job_id, skill_id)
            skills = await self.skills_repo.get_job_required_skills(job_id)
            return {
                "job_id": job_id,
                "required_skills": skills,
                "message": "Skill added to job successfully"
            }
        except Exception as e:
            print(f"Failed to add skill to job: {e}")
            raise

    async def remove_required_skill_from_job(self, job_id: int, skill_id: int):
        """Remove required skill from job"""
        job = await self.skills_repo.get_job_by_id(job_id)
        if not job:
            raise Exception("Job not found")

        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            await self.skills_repo.remove_required_skill_from_job(job_id, skill_id)
            return {"message": "Skill removed from job successfully"}
        except Exception as e:
            print(f"Failed to remove skill from job: {e}")
            raise

    async def get_jobs_by_skill(self, skill_id: int):
        """Get all jobs requiring a specific skill"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            jobs = await self.skills_repo.get_jobs_by_skill(skill_id)
            return {
                "skill_id": skill_id,
                "skill_name": skill['name'],
                "jobs": jobs,
                "total_jobs": len(jobs)
            }
        except Exception as e:
            print(f"Failed to get jobs by skill: {e}")
            raise

    async def get_matching_jobs_for_user(self, user_id: int):
        """Get jobs that match user's skills"""
        try:
            jobs = await self.skills_repo.get_matching_jobs_for_user(user_id)
            return {
                "user_id": user_id,
                "matching_jobs": jobs,
                "total_jobs": len(jobs)
            }
        except Exception as e:
            print(f"Failed to get matching jobs: {e}")
            raise

    # ===========================================================
    # LEARNING RESOURCES METHODS
    # ===========================================================
    async def get_all_resources(self, limit: int = 100, offset: int = 0):
        """Get all learning resources with pagination"""
        try:
            resources = await self.skills_repo.get_all_resources(limit, offset)
            return {
                "resources": resources,
                "total": len(resources),
                "limit": limit,
                "offset": offset
            }
        except Exception as e:
            print(f"Failed to get resources: {e}")
            raise

    async def get_resource_by_id(self, resource_id: int):
        """Get learning resource by ID"""
        try:
            resource = await self.skills_repo.get_resource_by_id(resource_id)
            if not resource:
                raise Exception("Resource not found")
            return resource
        except Exception as e:
            print(f"Failed to get resource: {e}")
            raise

    async def create_resource(self, title: str, platform: str,
                             url: str, cost: str ):
        """Create a new learning resource"""
        try:
            resource_id = await self.skills_repo.create_resource(
                title, platform, url, cost
            )
            resource = await self.skills_repo.get_resource_by_id(resource_id)
            return resource
        except Exception as e:
            print(f"Failed to create resource: {e}")
            raise

    async def get_resources_by_platform(self, platform: str):
        """Get resources by platform"""
        try:
            resources = await self.skills_repo.get_resources_by_platform(platform)
            return {
                "platform": platform,
                "resources": resources,
                "total": len(resources)
            }
        except Exception as e:
            print(f"Failed to get resources by platform: {e}")
            raise

    async def get_free_resources(self):
        """Get all free resources"""
        try:
            resources = await self.skills_repo.get_free_resources()
            return {
                "resources": resources,
                "total": len(resources),
                "cost": "Free"
            }
        except Exception as e:
            print(f"Failed to get free resources: {e}")
            raise

    # ===========================================================
    # RESOURCE SKILLS METHODS
    # ===========================================================
    async def get_resource_skills(self, resource_id: int):
        """Get all skills covered by a resource"""
        resource = await self.skills_repo.get_resource_by_id(resource_id)
        if not resource:
            raise Exception("Resource not found")

        try:
            skills = await self.skills_repo.get_resource_skills(resource_id)
            return {
                "resource_id": resource_id,
                "skills": skills,
                "total_skills": len(skills)
            }
        except Exception as e:
            print(f"Failed to get resource skills: {e}")
            raise

    async def add_skill_to_resource(self, resource_id: int, skill_id: int):
        """Add skill to learning resource"""
        resource = await self.skills_repo.get_resource_by_id(resource_id)
        if not resource:
            raise Exception("Resource not found")

        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            await self.skills_repo.add_skill_to_resource(resource_id, skill_id)
            skills = await self.skills_repo.get_resource_skills(resource_id)
            return {
                "resource_id": resource_id,
                "skills": skills,
                "message": "Skill added to resource successfully"
            }
        except Exception as e:
            print(f"Failed to add skill to resource: {e}")
            raise

    async def remove_skill_from_resource(self, resource_id: int, skill_id: int):
        """Remove skill from learning resource"""
        resource = await self.skills_repo.get_resource_by_id(resource_id)
        if not resource:
            raise Exception("Resource not found")

        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            await self.skills_repo.remove_skill_from_resource(resource_id, skill_id)
            return {"message": "Skill removed from resource successfully"}
        except Exception as e:
            print(f"Failed to remove skill from resource: {e}")
            raise

    async def get_resources_by_skill(self, skill_id: int):
        """Get all resources that teach a specific skill"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            resources = await self.skills_repo.get_resources_by_skill(skill_id)
            return {
                "skill_id": skill_id,
                "skill_name": skill['name'],
                "resources": resources,
                "total_resources": len(resources)
            }
        except Exception as e:
            print(f"Failed to get resources by skill: {e}")
            raise

    async def get_recommended_resources_for_user(self, user_id: int):
        """Get recommended resources based on skills user doesn't have"""
        try:
            resources = await self.skills_repo.get_recommended_resources_for_user(user_id)
            return {
                "user_id": user_id,
                "recommended_resources": resources,
                "total_resources": len(resources)
            }
        except Exception as e:
            print(f"Failed to get recommended resources: {e}")
            raise

    # ===========================================================
    # USER EXPERIENCE METHODS
    # ===========================================================
    async def get_user_experiences(self, user_id: int):
        """Get all experiences for a user"""
        try:
            experiences = await self.skills_repo.get_user_experiences(user_id)
            return {
                "user_id": user_id,
                "experiences": experiences,
                "total_experiences": len(experiences)
            }
        except Exception as e:
            print(f"Failed to get user experiences: {e}")
            raise

    async def get_experience_by_id(self, experience_id: int):
        """Get experience by ID"""
        try:
            experience = await self.skills_repo.get_experience_by_id(experience_id)
            if not experience:
                raise Exception("Experience not found")
            return experience
        except Exception as e:
            print(f"Failed to get experience: {e}")
            raise

    async def create_experience(self, user_id: int, title: str, description: str = None):
        """Create a new user experience"""
        try:
            experience_id = await self.skills_repo.create_experience(
                user_id, title, description
            )
            experience = await self.skills_repo.get_experience_by_id(experience_id)
            return experience
        except Exception as e:
            print(f"Failed to create experience: {e}")
            raise

    async def update_experience(self, experience_id: int, title: str , 
                               description: str ):
        """Update user experience"""
        experience = await self.skills_repo.get_experience_by_id(experience_id)
        if not experience:
            raise Exception("Experience not found")

        if not title and not description:
            raise Exception("At least one field (title or description) must be provided")

        try:
            await self.skills_repo.update_experience(experience_id, title, description)
            updated_experience = await self.skills_repo.get_experience_by_id(experience_id)
            return updated_experience
        except Exception as e:
            print(f"Failed to update experience: {e}")
            raise

    async def delete_experience(self, experience_id: int):
        """Delete user experience"""
        experience = await self.skills_repo.get_experience_by_id(experience_id)
        if not experience:
            raise Exception("Experience not found")

        try:
            await self.skills_repo.delete_experience(experience_id)
            return {"message": "Experience deleted successfully"}
        except Exception as e:
            print(f"Failed to delete experience: {e}")
            raise

