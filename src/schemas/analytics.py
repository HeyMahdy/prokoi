from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date

# Team Performance & Velocity Analysis Schemas
class TeamVelocityMetrics(BaseModel):
    team_name: str
    project_name: str
    avg_velocity: float
    velocity_stddev: float
    sprint_count: int
    target_achievement_percentage: float
    velocity_consistency: str

# Skill Gap Analysis Schemas
class SkillGapAnalysis(BaseModel):
    skill_name: str
    required_level: str
    required_count: int
    total_story_points: int
    available_users: int
    avg_user_skill_level: float
    skill_gap: float
    gap_severity: str

# Workload Distribution Schemas
class UserWorkloadAnalysis(BaseModel):
    user_id: int
    user_name: str
    capacity: float
    current_workload: float
    utilization_rate: float
    active_assignments: int
    active_projects: int

class TeamWorkloadSummary(BaseModel):
    team_name: str
    team_size: int
    avg_utilization_percent: float
    utilization_variance: float
    total_workload_hours: float
    total_capacity_hours: float
    overloaded_members: int
    underutilized_members: int
    team_status: str

# Issue Lifecycle & Bottleneck Analysis Schemas
class IssueLifecycleMetrics(BaseModel):
    issue_id: int
    title: str
    status: str
    priority: str
    story_points: int
    days_in_system: int
    project_name: str
    issue_type: Optional[str]
    created_by: Optional[str]
    assigned_to: Optional[str]
    status_changes: int
    comment_count: int

class StatusAnalysis(BaseModel):
    status: str
    issue_count: int
    avg_days_in_status: float
    avg_story_points: float
    high_priority_count: int
    critical_count: int

class BottleneckAnalysis(BaseModel):
    project_name: str
    status: str
    issue_count: int
    avg_days_in_status: float
    max_days: int
    stale_issues: int
    stale_percentage: float
    status_performance: str

# Cross-Project Resource Allocation Schemas
class ProjectResourceUsage(BaseModel):
    project_id: int
    project_name: str
    project_status: str
    workspace_name: str
    organization_name: str
    unique_assignees: int
    total_issues: int
    total_story_points: int
    completed_issues: int
    completed_story_points: int
    avg_issue_lifetime: float

class SharedResource(BaseModel):
    user_id: int
    user_name: str
    project_count: int
    projects: str
    total_assigned_story_points: int
    total_assigned_issues: int

class OrganizationMetrics(BaseModel):
    org_name: str
    total_projects: int
    total_workspaces: int
    total_teams: int
    total_users: int
    avg_story_points_per_project: float
    total_org_story_points: int
    shared_resource_count: int
    avg_projects_per_shared_resource: float

# Sprint Planning & Predictive Analytics Schemas
class HistoricalSprintData(BaseModel):
    sprint_id: int
    sprint_name: str
    project_id: int
    start_date: date
    end_date: date
    velocity_target: int
    sprint_duration: int
    planned_issues: int
    planned_story_points: int
    completed_issues: int
    completed_story_points: int
    avg_issue_completion_time: float

class TeamVelocityTrends(BaseModel):
    project_id: int
    project_name: str
    team_id: int
    team_name: str
    historical_velocity: float
    velocity_volatility: float
    sprint_count: int
    avg_achievement_rate: float
    avg_issue_completion_days: float

class UpcomingSprintAnalysis(BaseModel):
    sprint_id: int
    sprint_name: str
    project_id: int
    project_name: str
    team_name: str
    start_date: date
    end_date: date
    velocity_target: int
    planned_issues: int
    planned_story_points: int
    historical_velocity: float
    velocity_volatility: float
    avg_achievement_percentage: float
    predicted_velocity: float
    commitment_status: str
    risk_percentage: float

# Response schemas for API endpoints
class TeamPerformanceResponse(BaseModel):
    teams: List[TeamVelocityMetrics]

class SkillGapResponse(BaseModel):
    skill_gaps: List[SkillGapAnalysis]

class WorkloadDistributionResponse(BaseModel):
    team_summaries: List[TeamWorkloadSummary]
    user_analyses: List[UserWorkloadAnalysis]

class IssueLifecycleResponse(BaseModel):
    lifecycle_metrics: List[IssueLifecycleMetrics]
    status_analysis: List[StatusAnalysis]
    bottleneck_analysis: List[BottleneckAnalysis]

class ResourceAllocationResponse(BaseModel):
    project_usage: List[ProjectResourceUsage]
    shared_resources: List[SharedResource]
    organization_metrics: List[OrganizationMetrics]

class SprintPlanningResponse(BaseModel):
    historical_data: List[HistoricalSprintData]
    velocity_trends: List[TeamVelocityTrends]
    upcoming_analysis: List[UpcomingSprintAnalysis]

# Filter schemas for query parameters
class AnalyticsFilters(BaseModel):
    organization_id: Optional[int] = None
    project_id: Optional[int] = None
    team_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    priority: Optional[str] = None
