from src.repositories.issues import IssueRepository
from src.schemas.labels import LabelCreate, LabelUpdate, LabelResponse, IssueLabelAssignment, IssueLabelResponse
from typing import List, Optional
from datetime import datetime


class LabelsService:
    def __init__(self):
        self.issue_repo = IssueRepository()

    # Project label methods
    async def create_label(self, project_id: int, label_data: LabelCreate) -> LabelResponse:
        """Create a new label for a project"""
        try:
            # Check if label name already exists in project
            exists = await self.issue_repo.label_name_exists_in_project(project_id, label_data.name)
            if exists:
                raise ValueError(f"Label '{label_data.name}' already exists in this project")

            # Create the label
            label_id = await self.issue_repo.create_label(
                project_id=project_id,
                name=label_data.name,
                description=label_data.description,
                color=label_data.color
            )
            
            if not label_id:
                raise Exception("Failed to create label")

            # Fetch the created label
            label = await self.issue_repo.get_label_by_id(label_id)
            if not label:
                raise Exception("Label not found after creation")

            return LabelResponse(**label)

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to create label: {str(e)}")

    async def get_project_labels(self, project_id: int) -> List[LabelResponse]:
        """Get all labels for a specific project"""
        try:
            labels = await self.issue_repo.get_project_labels(project_id)
            return [LabelResponse(**label) for label in labels]
        except Exception as e:
            raise Exception(f"Failed to fetch project labels: {str(e)}")

    async def get_label_by_id(self, label_id: int) -> Optional[LabelResponse]:
        """Get label by ID"""
        try:
            label = await self.issue_repo.get_label_by_id(label_id)
            if not label:
                return None
            
            return LabelResponse(**label)
        except Exception as e:
            raise Exception(f"Failed to fetch label: {str(e)}")

    async def update_label(self, label_id: int, label_data: LabelUpdate) -> LabelResponse:
        """Update an existing label"""
        try:
            # Check if label exists
            existing = await self.issue_repo.get_label_by_id(label_id)
            if not existing:
                raise ValueError("Label not found")

            # Check if new name conflicts with existing labels in the same project
            if label_data.name and label_data.name != existing['name']:
                exists = await self.issue_repo.label_name_exists_in_project(
                    existing['project_id'], label_data.name, label_id
                )
                if exists:
                    raise ValueError(f"Label '{label_data.name}' already exists in this project")

            # Prepare update data (only include non-None values)
            update_data = {}
            for field, value in label_data.dict(exclude_unset=True).items():
                if value is not None:
                    update_data[field] = value

            if not update_data:
                # No fields to update, return existing label
                return LabelResponse(**existing)

            # Update the label
            await self.issue_repo.update_label(label_id, **update_data)

            # Fetch the updated label
            updated_label = await self.issue_repo.get_label_by_id(label_id)
            return LabelResponse(**updated_label)

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to update label: {str(e)}")

    async def delete_label(self, label_id: int) -> bool:
        """Delete a label"""
        try:
            # Check if label exists
            existing = await self.issue_repo.get_label_by_id(label_id)
            if not existing:
                raise ValueError("Label not found")

            # Check if label is being used by any issues
            usage_count = await self.issue_repo.get_label_usage_count(label_id)
            if usage_count > 0:
                raise ValueError(f"Cannot delete label. It is currently used by {usage_count} issue(s)")

            # Delete the label
            await self.issue_repo.delete_label(label_id)
            return True

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to delete label: {str(e)}")

    # Issue label methods
    async def add_label_to_issue(self, issue_id: int, label_id: int) -> bool:
        """Add a label to an issue"""
        try:
            # Check if issue exists
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                raise ValueError("Issue not found")

            # Check if label exists
            label = await self.issue_repo.get_label_by_id(label_id)
            if not label:
                raise ValueError("Label not found")

            # Check if label belongs to the same project as the issue
            if label['project_id'] != issue['project_id']:
                raise ValueError("Label does not belong to the same project as the issue")

            # Check if label is already assigned to the issue
            already_assigned = await self.issue_repo.issue_has_label(issue_id, label_id)
            if already_assigned:
                raise ValueError("Label is already assigned to this issue")

            # Add the label to the issue
            await self.issue_repo.add_label_to_issue(issue_id, label_id)
            return True

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to add label to issue: {str(e)}")

    async def remove_label_from_issue(self, issue_id: int, label_id: int) -> bool:
        """Remove a label from an issue"""
        try:
            # Check if the label is assigned to the issue
            has_label = await self.issue_repo.issue_has_label(issue_id, label_id)
            if not has_label:
                raise ValueError("Label is not assigned to this issue")

            # Remove the label from the issue
            await self.issue_repo.remove_label_from_issue(issue_id, label_id)
            return True

        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to remove label from issue: {str(e)}")

    async def get_issue_labels(self, issue_id: int) -> List[IssueLabelResponse]:
        """Get all labels for a specific issue"""
        try:
            # Check if issue exists
            issue = await self.issue_repo.get_issue_by_id(issue_id)
            if not issue:
                raise ValueError("Issue not found")

            labels = await self.issue_repo.get_issue_labels(issue_id)
            return [IssueLabelResponse(**label) for label in labels]
        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to fetch issue labels: {str(e)}")

    async def get_issues_by_label(self, project_id: int, label_id: int) -> List[dict]:
        """Get all issues with a specific label in a project"""
        try:
            # Check if label exists and belongs to the project
            label = await self.issue_repo.get_label_by_id(label_id)
            if not label:
                raise ValueError("Label not found")
            
            if label['project_id'] != project_id:
                raise ValueError("Label does not belong to this project")

            issues = await self.issue_repo.get_issues_by_label(project_id, label_id)
            return issues
        except ValueError:
            raise  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Failed to fetch issues by label: {str(e)}")
