from src.repositories.skill_verification_tests import SkillVerificationTestsRepository
from typing import Optional, List, Dict, Any

class SkillVerificationTestsService:
    def __init__(self):
        self.tests_repo = SkillVerificationTestsRepository()

    async def create_test(self, user_id: str, skill_id: str, resource_id: Optional[str],
                         test_data: Dict, score: int, total_questions: int, passed: bool) -> Dict[str, Any]:
        """Create a new skill verification test"""
        try:
            # Validate that the skill_id exists (you might want to add actual validation here)
            # Validate that the resource_id exists if provided (you might want to add actual validation here)
            
            test_id = await self.tests_repo.create_test(
                user_id, skill_id, resource_id, test_data, score, total_questions, passed
            )
            
            test = await self.tests_repo.get_test_by_id(test_id)
            if not test:
                raise Exception("Failed to create test")
                
            return test
        except Exception as e:
            raise Exception(f"Failed to create test: {str(e)}")

    async def get_test_by_id(self, test_id: str, user_id: str) -> Dict[str, Any]:
        """Get test by ID"""
        try:
            test = await self.tests_repo.get_test_by_id(test_id)
            if not test:
                raise Exception("Test not found")
                
            # Check if user owns this test
            if test["user_id"] != user_id:
                raise Exception("Unauthorized: You can only access your own tests")
                
            return test
        except Exception as e:
            raise Exception(f"Failed to get test: {str(e)}")

    async def get_user_tests(self, user_id: str, skill_id: Optional[str] = None, 
                           passed: Optional[bool] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all tests for a user"""
        try:
            tests = await self.tests_repo.get_user_tests(user_id, skill_id, passed, limit, offset)
            total_count = await self.tests_repo.get_test_count(user_id, skill_id, passed)
            
            return {
                "tests": tests,
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "filters": {
                    "skill_id": skill_id,
                    "passed": passed
                }
            }
        except Exception as e:
            raise Exception(f"Failed to get user tests: {str(e)}")

    async def get_user_skill_tests(self, user_id: str, skill_id: str) -> Dict[str, Any]:
        """Get all tests for a specific skill for a user"""
        try:
            tests = await self.tests_repo.get_user_skill_tests(user_id, skill_id)
            stats = await self.tests_repo.get_user_skill_test_stats(user_id, skill_id)
            
            return {
                "tests": tests,
                "stats": stats,
                "skill_id": skill_id
            }
        except Exception as e:
            raise Exception(f"Failed to get user skill tests: {str(e)}")

    async def delete_test(self, test_id: str, user_id: str) -> Dict[str, str]:
        """Delete a test by ID"""
        try:
            # First verify the test exists and belongs to the user
            test = await self.tests_repo.get_test_by_id(test_id)
            if not test:
                raise Exception("Test not found")
                
            if test["user_id"] != user_id:
                raise Exception("Unauthorized: You can only delete your own tests")
                
            # Delete the test
            success = await self.tests_repo.delete_test(test_id)
            if not success:
                raise Exception("Failed to delete test")
                
            return {"message": "Test deleted successfully"}
        except Exception as e:
            raise Exception(f"Failed to delete test: {str(e)}")