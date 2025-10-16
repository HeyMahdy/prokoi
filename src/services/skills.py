from src.repositories.skills import SkillsRepository
from src.schemas.skills import UserSkillCreate, UserSkillUpdate, ProficiencyLevel

class SkillsService:
    def __init__(self):
        self.skillsRepo = SkillsRepository()

    async def get_all_skills(self):
        """Get all global skills"""
        try:
            skills = await self.skillsRepo.get_all_skills()
            return skills
        except Exception as e:
            print(f"Failed to get skills: {e}")
            raise

    async def get_skill_by_id(self, skill_id: int):
        """Get skill by ID"""
        try:
            skill = await self.skillsRepo.get_skill_by_id(skill_id)
            if not skill:
                raise Exception("Skill not found")
            return skill
        except Exception as e:
            print(f"Failed to get skill: {e}")
            raise

    async def add_skill_to_user(self, user_id: int, skill_data: UserSkillCreate):
        """Add skill to user with proficiency level"""
        # Check if user exists
        user = await self.skillsRepo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Check if skill exists
        skill = await self.skillsRepo.get_skill_by_id(skill_data.skill_id)
        if not skill:
            raise Exception("Skill not found")

        # Check if user already has this skill
        user_has_skill = await self.skillsRepo.user_has_skill(user_id, skill_data.skill_id)
        if user_has_skill:
            raise Exception("User already has this skill")

        try:
            user_skill_id = await self.skillsRepo.add_skill_to_user(
                user_id=user_id,
                skill_id=skill_data.skill_id,
                proficiency_level=skill_data.proficiency_level.value
            )
            
            # Return the created user skill
            user_skill = await self.skillsRepo.get_user_skill(user_id, skill_data.skill_id)
            return user_skill
        except Exception as e:
            print(f"Failed to add skill to user: {e}")
            raise

    async def update_user_skill(self, user_id: int, skill_id: int, skill_data: UserSkillUpdate):
        """Update user's skill proficiency level"""
        # Check if user exists
        user = await self.skillsRepo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Check if skill exists
        skill = await self.skillsRepo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        # Check if user has this skill
        user_has_skill = await self.skillsRepo.user_has_skill(user_id, skill_id)
        if not user_has_skill:
            raise Exception("User does not have this skill")

        try:
            await self.skillsRepo.update_user_skill(
                user_id=user_id,
                skill_id=skill_id,
                proficiency_level=skill_data.proficiency_level.value
            )
            
            # Return the updated user skill
            user_skill = await self.skillsRepo.get_user_skill(user_id, skill_id)
            return user_skill
        except Exception as e:
            print(f"Failed to update user skill: {e}")
            raise

    async def get_user_skills(self, user_id: int):
        """Get all skills for a user"""
        # Check if user exists
        user = await self.skillsRepo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        try:
            user_skills = await self.skillsRepo.get_user_skills(user_id)
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
        # Check if user exists
        user = await self.skillsRepo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Check if skill exists
        skill = await self.skillsRepo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        try:
            user_skill = await self.skillsRepo.get_user_skill(user_id, skill_id)
            if not user_skill:
                raise Exception("User does not have this skill")
            return user_skill
        except Exception as e:
            print(f"Failed to get user skill: {e}")
            raise

    async def remove_user_skill(self, user_id: int, skill_id: int):
        """Remove skill from user"""
        # Check if user exists
        user = await self.skillsRepo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Check if skill exists
        skill = await self.skillsRepo.get_skill_by_id(skill_id)
        if not skill:
            raise Exception("Skill not found")

        # Check if user has this skill
        user_has_skill = await self.skillsRepo.user_has_skill(user_id, skill_id)
        if not user_has_skill:
            raise Exception("User does not have this skill")

        try:
            await self.skillsRepo.remove_user_skill(user_id, skill_id)
            return {"message": "Skill removed from user successfully"}
        except Exception as e:
            print(f"Failed to remove user skill: {e}")
            raise
