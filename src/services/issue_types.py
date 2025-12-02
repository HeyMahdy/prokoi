from src.repositories.issues import IssueRepository
from src.schemas.issue_types import IssueTypeCreate, IssueTypeResponse
from typing import List, Optional


class IssueTypesService:
    def __init__(self):
        self.issue_repo = IssueRepository()

    async def get_all_issue_types(self) -> List[IssueTypeResponse]:
        """Get all issue types"""
        try:
            issue_types = await self.issue_repo.get_all_issue_types()
            return [IssueTypeResponse(id=it['id'], name=it['name']) for it in issue_types]
        except Exception as e:
            raise Exception(f"Failed to fetch issue types: {str(e)}")

    async def create_issue_type(self, issue_type_data: IssueTypeCreate) -> IssueTypeResponse:
        """Create a new issue type"""
        try:
            # Check if issue type with same name already exists
            exists = await self.issue_repo.issue_type_exists(issue_type_data.name)
            if exists:
                raise ValueError(f"Issue type '{issue_type_data.name}' already exists")

            # Create the issue type
            issue_type_id = await self.issue_repo.create_issue_type(issue_type_data.name)
            print(issue_type_id)
            if not issue_type_id:
                raise Exception("Failed to create issue type")

            # Fetch the created issue type
            issue_type = await self.issue_repo.get_issue_type_by_id(issue_type_id)
            if not issue_type:
                raise Exception("Issue type not found after creation")

            return IssueTypeResponse(id=issue_type['id'], name=issue_type['name'])

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to create issue type: {str(e)}")

    async def get_issue_type_by_id(self, issue_type_id: int) -> Optional[IssueTypeResponse]:
        """Get issue type by ID"""
        try:
            issue_type = await self.issue_repo.get_issue_type_by_id(issue_type_id)
            if not issue_type:
                return None
            
            return IssueTypeResponse(id=issue_type['id'], name=issue_type['name'])
        except Exception as e:
            raise Exception(f"Failed to fetch issue type: {str(e)}")

    async def update_issue_type(self, issue_type_id: int, issue_type_data: IssueTypeCreate) -> IssueTypeResponse:
        """Update an existing issue type"""
        try:
            # Check if issue type exists
            existing = await self.issue_repo.get_issue_type_by_id(issue_type_id)
            if not existing:
                raise ValueError("Issue type not found")

            # Check if another issue type with same name exists
            exists = await self.issue_repo.issue_type_exists(issue_type_data.name)
            if exists and existing['name'] != issue_type_data.name:
                raise ValueError(f"Issue type '{issue_type_data.name}' already exists")

            # Update the issue type
            await self.issue_repo.update_issue_type(issue_type_id, issue_type_data.name)

            # Fetch the updated issue type
            updated_issue_type = await self.issue_repo.get_issue_type_by_id(issue_type_id)
            return IssueTypeResponse(id=updated_issue_type['id'], name=updated_issue_type['name'])

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to update issue type: {str(e)}")

    async def delete_issue_type(self, issue_type_id: int) -> bool:
        """Delete an issue type"""
        try:
            # Check if issue type exists
            existing = await self.issue_repo.get_issue_type_by_id(issue_type_id)
            if not existing:
                raise ValueError("Issue type not found")

            # Delete the issue type
            await self.issue_repo.delete_issue_type(issue_type_id)
            return True

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to delete issue type: {str(e)}")
