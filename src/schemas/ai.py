from typing import List, Optional, TypedDict, Annotated
from pydantic import BaseModel, Field
import operator

class ProjectPlanRequest(BaseModel):
    goal: str = Field(..., description="High-level goal of the project")
    project_id: int = Field(..., description="ID of the project to add issues to")

class GeneratedIssue(BaseModel):
    title: str = Field(..., description="Title of the issue")
    description: str = Field(..., description="Detailed description of the issue")
    type: str = Field(..., description="Type of issue: 'story', 'task', or 'bug'")
    priority: str = Field(..., description="Priority: 'low', 'medium', 'high', 'critical'")
    story_points: int = Field(..., description="Estimated story points")
    acceptance_criteria: List[str] = Field(default_factory=list, description="List of acceptance criteria")

class ProjectPhase(BaseModel):
    name: str = Field(..., description="Name of the phase (e.g., 'Authentication')")
    description: str = Field(..., description="Description of what this phase entails")

class AgentState(TypedDict):
    goal: str
    project_id: int
    phases: List[ProjectPhase]
    generated_issues: Annotated[List[GeneratedIssue], operator.add]
    error: Optional[str]
