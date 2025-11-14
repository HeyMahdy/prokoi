from fastapi import APIRouter, HTTPException, Request,Depends, status as fastapi_status
from src.services.skill_verification_tests import SkillVerificationTestsService
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi.security import HTTPBearer

# Pydantic models for request/response
class TestCreate(BaseModel):
    skill_id: str
    resource_id: Optional[str] = None
    test_data: Dict[str, Any]
    score: int
    total_questions: int
    passed: bool

class TestResponse(BaseModel):
    id: str
    user_id: str
    skill_id: str
    resource_id: Optional[str] = None
    test_data: Dict[str, Any]
    score: int
    total_questions: int
    passed: bool
    taken_at: datetime
bearer = HTTPBearer()

# Initialize service
tests_service = SkillVerificationTestsService()

# Create router
router = APIRouter(prefix="/api/skill-tests", tags=["skill-tests"],dependencies=[Depends(bearer)])

# Test endpoints
@router.post("/", status_code=fastapi_status.HTTP_201_CREATED)
async def create_test(test_data: TestCreate, request: Request):
    """Create a new skill verification test"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Validate that skill_id is provided
        if not test_data.skill_id:
            raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail="Skill ID is required")
        
        # If resource_id is provided, validate it (you might want to add actual validation here)
        # For now, we'll just pass it through and let the database handle the foreign key constraint
        
        test = await tests_service.create_test(
            user_id=user["id"],
            skill_id=test_data.skill_id,
            resource_id=test_data.resource_id if test_data.resource_id else None,
            test_data=test_data.test_data,
            score=test_data.score,
            total_questions=test_data.total_questions,
            passed=test_data.passed
        )
        return test
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{test_id}")
async def get_test(test_id: str, request: Request):
    """Get test by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        test = await tests_service.get_test_by_id(
            test_id=test_id,
            user_id=user["id"]
        )
        return test
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{test_id}")
async def delete_test(test_id: str, request: Request):
    """Delete test by ID"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        result = await tests_service.delete_test(
            test_id=test_id,
            user_id=user["id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/")
async def get_user_tests(
    request: Request,
    skill_id: Optional[str] = None,
    passed: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0
):
    """Get all tests for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        tests = await tests_service.get_user_tests(
            user_id=user["id"],
            skill_id=skill_id,
            passed=passed,
            limit=limit,
            offset=offset
        )
        return tests
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/skill/{skill_id}")
async def get_user_skill_tests(skill_id: str, request: Request):
    """Get all tests for a specific skill for the current user"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=fastapi_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        tests = await tests_service.get_user_skill_tests(
            user_id=user["id"],
            skill_id=skill_id
        )
        return tests
    except Exception as e:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail=str(e))