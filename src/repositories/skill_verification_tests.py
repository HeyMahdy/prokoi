from src.core.database import db
import uuid
from typing import Optional, List, Dict, Any
import json

class SkillVerificationTestsRepository:
    async def create_test(self, user_id: str, skill_id: str, resource_id: Optional[str],
                         test_data: Dict, score: int, total_questions: int, passed: bool) -> str:
        """Create a new skill verification test"""
        test_id = str(uuid.uuid4())
        query = """
        INSERT INTO skill_verification_tests (id, user_id, skill_id, resource_id, test_data, score, total_questions, passed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Handle NULL resource_id properly
        resource_id_param = resource_id if resource_id else None
        params = [test_id, user_id, skill_id, resource_id_param, json.dumps(test_data), str(score), str(total_questions), str(int(passed))]
        await db.execute_insert(query, params)
        return test_id

    async def get_test_by_id(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get test by ID"""
        query = """
        SELECT id, user_id, skill_id, resource_id, test_data, score, total_questions, passed, taken_at
        FROM skill_verification_tests
        WHERE id = %s
        """
        rows = await db.execute_query(query, (test_id,))
        if rows:
            # Parse JSON data
            test = rows[0]
            if isinstance(test['test_data'], str):
                test['test_data'] = json.loads(test['test_data'])
            return test
        return None

    async def get_user_tests(self, user_id: str, skill_id: Optional[str] = None, 
                           passed: Optional[bool] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all tests for a user"""
        query = """
        SELECT id, user_id, skill_id, resource_id, test_data, score, total_questions, passed, taken_at
        FROM skill_verification_tests
        WHERE user_id = %s
        """
        params = [user_id]
        
        if skill_id:
            query += " AND skill_id = %s"
            params.append(skill_id)
            
        if passed is not None:
            query += " AND passed = %s"
            params.append(str(int(passed)))
            
        query += " ORDER BY taken_at DESC"
        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        
        rows = await db.execute_query(query, params)
        # Parse JSON data for each test
        for row in rows:
            if isinstance(row['test_data'], str):
                row['test_data'] = json.loads(row['test_data'])
        return rows

    async def get_user_skill_tests(self, user_id: str, skill_id: str) -> List[Dict[str, Any]]:
        """Get all tests for a specific skill for a user"""
        query = """
        SELECT id, user_id, skill_id, resource_id, test_data, score, total_questions, passed, taken_at
        FROM skill_verification_tests
        WHERE user_id = %s AND skill_id = %s
        ORDER BY taken_at DESC
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        # Parse JSON data for each test
        for row in rows:
            if isinstance(row['test_data'], str):
                row['test_data'] = json.loads(row['test_data'])
        return rows

    async def get_test_count(self, user_id: str, skill_id: Optional[str] = None, passed: Optional[bool] = None) -> int:
        """Get total test count for a user"""
        query = "SELECT COUNT(*) as count FROM skill_verification_tests WHERE user_id = %s"
        params = [user_id]
        
        if skill_id:
            query += " AND skill_id = %s"
            params.append(skill_id)
            
        if passed is not None:
            query += " AND passed = %s"
            params.append(str(int(passed)))
            
        rows = await db.execute_query(query, params)
        return rows[0]['count'] if rows else 0

    async def get_user_skill_test_stats(self, user_id: str, skill_id: str) -> Dict[str, Any]:
        """Get test statistics for a specific skill for a user"""
        query = """
        SELECT 
            COUNT(*) as total_tests,
            SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) as passed_tests,
            AVG(score) as average_score,
            MAX(score) as highest_score,
            MAX(taken_at) as last_tested
        FROM skill_verification_tests
        WHERE user_id = %s AND skill_id = %s
        """
        rows = await db.execute_query(query, (user_id, skill_id))
        return rows[0] if rows else {
            "total_tests": 0,
            "passed_tests": 0,
            "average_score": 0,
            "highest_score": 0,
            "last_tested": None
        }

    async def delete_test(self, test_id: str) -> bool:
        """Delete a test by ID"""
        query = "DELETE FROM skill_verification_tests WHERE id = %s"
        await db.execute_query(query, (test_id,))
        return True