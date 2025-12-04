from src.repositories.issues import IssueRepository
from src.repositories.users import UserRepository
from src.schemas.issues import IssueCreate, IssueUpdate, IssueResponse, IssueAssignmentCreate, IssueAssignmentResponse, IssueStatusUpdate, IssueWithAssignment
from typing import List, Optional
from datetime import datetime
from src.notification.streams import publish_message

class IssuesService:
    def __init__(self):
        self.issue_repo = IssueRepository()
        self.user_repo = UserRepository()

    async def create_issue(self, issue_data: IssueCreate, created_by: int) -> IssueResponse:
        """Create a new issue"""
        try:
            # Create the issue
            issue_id = await self.issue_repo.create_issue(
                project_id=issue_data.project_id,
                title=issue_data.title,
                created_by=created_by,
                type_id=issue_data.type_id,
                description=issue_data.description,
                story_points=issue_data.story_points,
                status=issue_data.status,
                priority=issue_data.priority,
                parent_issue_id=issue_data.parent_issue_id
            )
            
            if not issue_id:
                raise Exception("Failed to create issue")

            # Fetch the created issue
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found after creation")

            return IssueResponse(**issue)

        except Exception as e:
            raise Exception(f"Failed to create issue: {str(e)}")

    async def get_issues_by_project(self, project_id: int) -> List[IssueResponse]:
        """Get all issues for a specific project"""
        try:
            issues = await self.issue_repo.get_issues_by_project(project_id)
            return [IssueResponse(**issue) for issue in issues]
        except Exception as e:
            raise Exception(f"Failed to fetch issues: {str(e)}")

    async def get_issue_by_id(self, issue_id: int) -> Optional[IssueResponse]:
        """Get issue by ID"""
        try:
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                return None
            
            return IssueResponse(**issue)
        except Exception as e:
            raise Exception(f"Failed to fetch issue: {str(e)}")

    async def update_issue(self, issue_id: int, issue_data: IssueUpdate) -> IssueResponse:
        """Update an existing issue"""
        try:
            # Check if issue exists
            existing = await self.issue_repo.get_issue_by_id(issue_id)
            if not existing:
                raise ValueError("Issue not found")

            # Prepare update data (only include non-None values)
            update_data = {}
            for field, value in issue_data.dict(exclude_unset=True).items():
                if value is not None:
                    update_data[field] = value

            if not update_data:
                # No fields to update, return existing issue
                return IssueResponse(**existing)

            # Update the issue
            await self.issue_repo.update_issue(issue_id, **update_data)

            # Fetch the updated issue
            updated_issue = await self.issue_repo.get_issue_by_id(issue_id)
            return IssueResponse(**updated_issue)

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to update issue: {str(e)}")

    async def delete_issue(self, issue_id: int) -> bool:
        """Delete an issue"""
        try:
            # Check if issue exists
            existing = await self.issue_repo.get_issue_by_id(issue_id)
            if not existing:
                raise ValueError("Issue not found")

            # Delete the issue
            await self.issue_repo.delete_issue(issue_id)
            return True

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to delete issue: {str(e)}")

    async def get_issues_by_status(self, project_id: int, status: str) -> List[IssueResponse]:
        """Get all issues with a specific status for a project"""
        try:
            issues = await self.issue_repo.get_issues_by_status(project_id, status)
            return [IssueResponse(**issue) for issue in issues]
        except Exception as e:
            raise Exception(f"Failed to fetch issues by status: {str(e)}")

    async def get_issues_by_priority(self, project_id: int, priority: str) -> List[IssueResponse]:
        """Get all issues with a specific priority for a project"""
        try:
            issues = await self.issue_repo.get_issues_by_priority(project_id, priority)
            return [IssueResponse(**issue) for issue in issues]
        except Exception as e:
            raise Exception(f"Failed to fetch issues by priority: {str(e)}")

    async def get_sub_issues(self, parent_issue_id: int) -> List[IssueResponse]:
        """Get all sub-issues (children) of a parent issue"""
        try:
            # Check if parent issue exists
            parent_issue = await self.issue_repo.get_issue_by_id(parent_issue_id)
            if not parent_issue:
                raise ValueError("Parent issue not found")

            issues = await self.issue_repo.get_sub_issues(parent_issue_id)
            return [IssueResponse(**issue) for issue in issues]
        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to fetch sub-issues: {str(e)}")

    async def get_issues_with_filters(self, project_id: int, status: Optional[str] = None, 
                                    priority: Optional[str] = None, 
                                    type_id: Optional[int] = None) -> List[IssueResponse]:
        """Get issues with optional filters"""
        try:
            # Get all issues for the project first
            all_issues = await self.issue_repo.get_issues_by_project(project_id)
            
            # Apply filters
            filtered_issues = all_issues
            
            if status:
                filtered_issues = [issue for issue in filtered_issues if issue['status'] == status]
            
            if priority:
                filtered_issues = [issue for issue in filtered_issues if issue['priority'] == priority]
            
            if type_id:
                filtered_issues = [issue for issue in filtered_issues if issue['type_id'] == type_id]
            
            return [IssueResponse(**issue) for issue in filtered_issues]
            
        except Exception as e:
            raise Exception(f"Failed to fetch filtered issues: {str(e)}")

    # Issue Assignment methods
    async def assign_issue(self, issue_id: int, assignment_data: IssueAssignmentCreate, assigned_by: int) -> IssueAssignmentResponse:
        """Assign an issue to a user"""
        try:
            # Check if issue exists
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                raise ValueError("Issue not found")

            # Check if assigned user exists
            assigned_user = await self.user_repo.find_user_by_id(assignment_data.assigned_to)
            if not assigned_user:
                raise ValueError("Assigned user not found")

            # Check if issue is already assigned
            is_assigned = await self.issue_repo.is_issue_assigned(issue_id)
            if is_assigned:
                # Update existing assignment
                await self.issue_repo.update_assignment(issue_id, assignment_data.assigned_to, assigned_by)
            else:
                # Create new assignment
                await self.issue_repo.assign_issue(issue_id, assignment_data.assigned_to, assigned_by)

            # Get the assignment details
            assignment = await self.issue_repo.get_issue_assignment(issue_id)
            print(assignment)

            if not assignment:
                raise Exception("Assignment not found after creation")
            await publish_message(
    user_id=assignment_data.assigned_to,
    message=f"task {assignment['title']}"
)
            return IssueAssignmentResponse(**assignment)

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to assign issue: {str(e)}")

    async def unassign_issue(self, issue_id: int) -> bool:
        """Remove assignment from an issue"""
        try:
            # Check if issue exists
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                raise ValueError("Issue not found")

            # Check if issue is assigned
            is_assigned = await self.issue_repo.is_issue_assigned(issue_id)
            if not is_assigned:
                raise ValueError("Issue is not currently assigned")

            # Remove assignment
            await self.issue_repo.unassign_issue(issue_id)
            return True

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to unassign issue: {str(e)}")

    async def get_issue_assignment(self, issue_id: int) -> Optional[IssueAssignmentResponse]:
        """Get assignment details for an issue"""
        try:
            assignment = await self.issue_repo.get_issue_assignment(issue_id)
            if not assignment:
                return None
            
            return IssueAssignmentResponse(**assignment)

        except Exception as e:
            raise Exception(f"Failed to fetch assignment: {str(e)}")

    async def get_issue_with_assignment(self, issue_id: int) -> Optional[IssueWithAssignment]:
        """Get issue with assignment details"""
        try:
            # Get issue details
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                return None

            # Get assignment details
            assignment = await self.issue_repo.get_issue_assignment(issue_id)
            
            # Create response
            issue_response = IssueResponse(**issue)
            assignment_response = IssueAssignmentResponse(**assignment) if assignment else None
            
            return IssueWithAssignment(
                **issue_response.dict(),
                assignment=assignment_response
            )

        except Exception as e:
            raise Exception(f"Failed to fetch issue with assignment: {str(e)}")

    async def get_user_assigned_issues(self, user_id: int, project_id: int = None) -> List[IssueResponse]:
        """Get all issues assigned to a user"""
        try:
            issues = await self.issue_repo.get_user_assigned_issues(user_id, project_id)
            return [IssueResponse(**issue) for issue in issues]

        except Exception as e:
            raise Exception(f"Failed to fetch assigned issues: {str(e)}")

    async def update_issue_status(self, issue_id: int, status_data: IssueStatusUpdate) -> IssueResponse:
        """Update issue status"""
        try:
            # Check if issue exists
            existing = await self.issue_repo.get_issue_by_id(issue_id)
            if not existing:
                raise ValueError("Issue not found")

            # Update the issue status
            await self.issue_repo.update_issue(issue_id, status=status_data.status)


            # Fetch the updated issue
            updated_issue = await self.issue_repo.get_issue_by_id(issue_id)

            return IssueResponse(**updated_issue)

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to update issue status: {str(e)}")
