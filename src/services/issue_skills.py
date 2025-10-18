from src.repositories.issue_skills import IssueSkillsRepository
from src.schemas.issue_skills import (
    IssueSkillRequirementCreate, 
    IssueSkillRequirementUpdate, 
    IssueSkillRequirementResponse,
    IssueSkillsListResponse,
    SkillMatchResponse
)

class IssueSkillsService:
    def __init__(self):
        self.issue_skills_repo = IssueSkillsRepository()

    async def add_skill_to_issue(self, issue_id: int, skill_data: IssueSkillRequirementCreate) -> IssueSkillRequirementResponse:
        """Add skill requirement to an issue"""
        try:
            # Validate issue exists
            issue = await self.issue_skills_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")

            # Validate skill exists
            skill = await self.issue_skills_repo.get_skill_by_id(skill_data.skill_id)
            if not skill:
                raise Exception("Skill not found")

            # Check if skill requirement already exists
            existing = await self.issue_skills_repo.issue_has_skill_requirement(issue_id, skill_data.skill_id)
            if existing:
                raise Exception("Skill requirement already exists for this issue")

            # Add skill requirement
            requirement_id = await self.issue_skills_repo.add_skill_to_issue(
                issue_id, skill_data.skill_id, skill_data.required_level.value
            )

            # Fetch the created requirement
            requirement = await self.issue_skills_repo.get_issue_skill_requirement(issue_id, skill_data.skill_id)
            if not requirement:
                raise Exception("Failed to create skill requirement")

            return IssueSkillRequirementResponse(**requirement)

        except Exception as e:
            raise Exception(f"Failed to add skill to issue: {str(e)}")

    async def update_issue_skill_requirement(self, issue_id: int, skill_id: int, skill_data: IssueSkillRequirementUpdate) -> IssueSkillRequirementResponse:
        """Update skill requirement level for an issue"""
        try:
            # Validate issue exists
            issue = await self.issue_skills_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")

            # Check if skill requirement exists
            existing = await self.issue_skills_repo.issue_has_skill_requirement(issue_id, skill_id)
            if not existing:
                raise Exception("Skill requirement not found for this issue")

            # Update skill requirement
            success = await self.issue_skills_repo.update_issue_skill_requirement(
                issue_id, skill_id, skill_data.required_level.value
            )
            if not success:
                raise Exception("Failed to update skill requirement")

            # Fetch the updated requirement
            requirement = await self.issue_skills_repo.get_issue_skill_requirement(issue_id, skill_id)
            if not requirement:
                raise Exception("Skill requirement not found after update")

            return IssueSkillRequirementResponse(**requirement)

        except Exception as e:
            raise Exception(f"Failed to update skill requirement: {str(e)}")

    async def remove_skill_from_issue(self, issue_id: int, skill_id: int) -> bool:
        """Remove skill requirement from an issue"""
        try:
            # Validate issue exists
            issue = await self.issue_skills_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")

            # Check if skill requirement exists
            existing = await self.issue_skills_repo.issue_has_skill_requirement(issue_id, skill_id)
            if not existing:
                raise Exception("Skill requirement not found for this issue")

            # Remove skill requirement
            success = await self.issue_skills_repo.remove_skill_from_issue(issue_id, skill_id)
            if not success:
                raise Exception("Failed to remove skill requirement")

            return True

        except Exception as e:
            raise Exception(f"Failed to remove skill from issue: {str(e)}")

    async def get_issue_skills(self, issue_id: int) -> IssueSkillsListResponse:
        """Get all skill requirements for an issue"""
        try:
            # Validate issue exists
            issue = await self.issue_skills_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")

            # Get skill requirements
            skills = await self.issue_skills_repo.get_issue_skills(issue_id)
            skill_responses = [IssueSkillRequirementResponse(**skill) for skill in skills]

            return IssueSkillsListResponse(
                issue_id=issue_id,
                total_skills=len(skill_responses),
                skills=skill_responses
            )

        except Exception as e:
            raise Exception(f"Failed to get issue skills: {str(e)}")

    async def get_issue_skill_requirement(self, issue_id: int, skill_id: int) -> IssueSkillRequirementResponse:
        """Get specific skill requirement for an issue"""
        try:
            # Validate issue exists
            issue = await self.issue_skills_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")

            # Get skill requirement
            requirement = await self.issue_skills_repo.get_issue_skill_requirement(issue_id, skill_id)
            if not requirement:
                raise Exception("Skill requirement not found")

            return IssueSkillRequirementResponse(**requirement)

        except Exception as e:
            raise Exception(f"Failed to get skill requirement: {str(e)}")

    async def get_skill_match_analysis(self, issue_id: int, user_id: int) -> list[SkillMatchResponse]:
        """Get skill match analysis for a user and issue"""
        try:
            # Validate issue exists
            issue = await self.issue_skills_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")

            # Check if user has access to the project
            has_access = await self.issue_skills_repo.user_has_project_access(user_id, issue['project_id'])
            if not has_access:
                raise Exception("User does not have access to this project")

            # Get skill match analysis
            matches = await self.issue_skills_repo.get_skill_match_analysis(issue_id, user_id)
            
            return [SkillMatchResponse(**match) for match in matches]

        except Exception as e:
            raise Exception(f"Failed to get skill match analysis: {str(e)}")
