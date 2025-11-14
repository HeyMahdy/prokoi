from src.repositories.skills import SkillsRepository
import uuid
from typing import Optional

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

    async def get_skill_by_id(self, skill_id: str):
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

    async def create_skill(self, name: str, category: str, description: Optional[str] = None):
        """Create a new skill"""
        existing_skill = await self.skills_repo.get_skill_by_name(name)
        if existing_skill:
            raise Exception("Skill already exists")

        try:
            skill_id = await self.skills_repo.create_skill(name, category, description)
            skill = await self.skills_repo.get_skill_by_id(skill_id)
            return skill
        except Exception as e:
            print(f"Failed to create skill: {e}")
            raise

    # ===========================================================
    # USER SKILLS METHODS
    # ===========================================================
    async def get_user_skills(self, user_id: str):
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

    async def get_user_skill(self, user_id: str, skill_id: str):
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

    async def add_skill_to_user(self, user_id: str, skill_id: str, proficiency_level: str):
        """Add skill to user"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        user_has_skill = await self.skills_repo.user_has_skill(user_id, skill_id)
        if user_has_skill:
            raise Exception("User already has this skill")

        try:
            user_skill_id = await self.skills_repo.add_skill_to_user(user_id, skill_id, proficiency_level)
            user_skill = await self.skills_repo.get_user_skill(user_id, skill_id)
            return user_skill
        except Exception as e:
            print(f"Failed to add skill to user: {e}")
            raise

    async def update_user_skill(self, user_id: str, skill_id: str, proficiency_level: str):
        """Update user skill proficiency"""
        skill = await self.skills_repo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        user_has_skill = await self.skills_repo.user_has_skill(user_id, skill_id)
        if not user_has_skill:
            raise Exception("User does not have this skill")

        try:
            await self.skills_repo.update_user_skill(user_id, skill_id, proficiency_level)
            user_skill = await self.skills_repo.get_user_skill(user_id, skill_id)
            return user_skill
        except Exception as e:
            print(f"Failed to update user skill: {e}")
            raise

    async def remove_user_skill(self, user_id: str, skill_id: str):
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
    # USER EXPERIENCE METHODS
    # ===========================================================
    async def get_user_experiences(self, user_id: str):
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

    async def get_experience_by_id(self, experience_id: str):
        """Get experience by ID"""
        try:
            experience = await self.skills_repo.get_experience_by_id(experience_id)
            if not experience:
                raise Exception("Experience not found")
            return experience
        except Exception as e:
            print(f"Failed to get experience: {e}")
            raise

    async def create_experience(self, user_id: str, title: str, description: Optional[str] = None,
                              type: Optional[str] = None, company: Optional[str] = None,
                              start_date: Optional[str] = None, end_date: Optional[str] = None,
                              is_current: bool = False):
        """Create a new user experience"""
        try:
            experience_id = await self.skills_repo.create_experience(
                user_id, title, description, type, company, start_date, end_date, is_current
            )
            experience = await self.skills_repo.get_experience_by_id(experience_id)
            return experience
        except Exception as e:
            print(f"Failed to create experience: {e}")
            raise

    async def update_experience(self, experience_id: str, title: Optional[str] = None,
                               description: Optional[str] = None, type: Optional[str] = None,
                               company: Optional[str] = None, start_date: Optional[str] = None,
                               end_date: Optional[str] = None, is_current: Optional[bool] = None):
        """Update user experience"""
        experience = await self.skills_repo.get_experience_by_id(experience_id)
        if not experience:
            raise Exception("Experience not found")

        # Check if at least one field is provided
        if all(field is None for field in [title, description, type, company, start_date, end_date, is_current]):
            raise Exception("At least one field must be provided for update")

        try:
            await self.skills_repo.update_experience(experience_id, title, description, type,
                                                   company, start_date, end_date, is_current)
            updated_experience = await self.skills_repo.get_experience_by_id(experience_id)
            return updated_experience
        except Exception as e:
            print(f"Failed to update experience: {e}")
            raise

    async def delete_experience(self, experience_id: str):
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