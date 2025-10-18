from src.repositories.issues import IssueRepository
from typing import List, Dict, Any
from datetime import datetime


class AnalyticsService:
    def __init__(self):
        self.issue_repo = IssueRepository()

    async def get_project_analytics_dashboard(self) -> List[Dict[str, Any]]:
        """Get project analytics dashboard data"""
        try:
            analytics_data = await self.issue_repo.project_analytics_dashboard()
            
            # Process the data to ensure proper types and formatting
            processed_data = []
            for item in analytics_data:
                processed_item = {
                    "project_id": int(item["project_id"]),
                    "project_name": str(item["project_name"]),
                    "workspace_name": str(item["workspace_name"]),
                    "organization_name": str(item["organization_name"]),
                    "total_issues": int(item["total_issues"]) if item["total_issues"] else 0,
                    "open_issues": int(item["open_issues"]) if item["open_issues"] else 0,
                    "in_progress_issues": int(item["in_progress_issues"]) if item["in_progress_issues"] else 0,
                    "completed_issues": int(item["completed_issues"]) if item["completed_issues"] else 0,
                    "avg_story_points": float(item["avg_story_points"]) if item["avg_story_points"] else 0.0,
                    "total_story_points": int(item["total_story_points"]) if item["total_story_points"] else 0,
                    "contributors": int(item["contributors"]) if item["contributors"] else 0,
                    "total_comments": int(item["total_comments"]) if item["total_comments"] else 0,
                    "project_age_days": int(item["project_age_days"]) if item["project_age_days"] else 0,
                    "completion_percentage": float(item["completion_percentage"]) if item["completion_percentage"] else 0.0
                }
                processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            raise Exception(f"Failed to fetch project analytics: {str(e)}")

    async def get_project_analytics_summary(self) -> Dict[str, Any]:
        """Get overall analytics summary across all projects"""
        try:
            dashboard_data = await self.get_project_analytics_dashboard()
            
            if not dashboard_data:
                return {
                    "total_projects": 0,
                    "total_issues": 0,
                    "total_completed_issues": 0,
                    "overall_completion_percentage": 0.0,
                    "total_story_points": 0,
                    "total_contributors": 0,
                    "avg_project_age_days": 0.0
                }
            
            # Calculate summary statistics
            total_projects = len(dashboard_data)
            total_issues = sum(item["total_issues"] for item in dashboard_data)
            total_completed_issues = sum(item["completed_issues"] for item in dashboard_data)
            total_story_points = sum(item["total_story_points"] for item in dashboard_data)
            total_contributors = sum(item["contributors"] for item in dashboard_data)
            avg_project_age = sum(item["project_age_days"] for item in dashboard_data) / total_projects if total_projects > 0 else 0
            
            overall_completion = (total_completed_issues * 100.0 / total_issues) if total_issues > 0 else 0.0
            
            return {
                "total_projects": total_projects,
                "total_issues": total_issues,
                "total_completed_issues": total_completed_issues,
                "overall_completion_percentage": round(overall_completion, 2),
                "total_story_points": total_story_points,
                "total_contributors": total_contributors,
                "avg_project_age_days": round(avg_project_age, 1)
            }
            
        except Exception as e:
            raise Exception(f"Failed to fetch analytics summary: {str(e)}")

    async def get_top_performing_projects(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing projects by completion percentage"""
        try:
            dashboard_data = await self.get_project_analytics_dashboard()
            
            # Sort by completion percentage and total issues
            sorted_projects = sorted(
                dashboard_data, 
                key=lambda x: (x["completion_percentage"], x["total_issues"]), 
                reverse=True
            )
            
            return sorted_projects[:limit]
            
        except Exception as e:
            raise Exception(f"Failed to fetch top performing projects: {str(e)}")

    async def get_project_health_metrics(self) -> Dict[str, Any]:
        """Get project health metrics and insights"""
        try:
            dashboard_data = await self.get_project_analytics_dashboard()
            
            if not dashboard_data:
                return {
                    "healthy_projects": 0,
                    "at_risk_projects": 0,
                    "stalled_projects": 0,
                    "total_projects": 0
                }
            
            healthy_projects = 0
            at_risk_projects = 0
            stalled_projects = 0
            
            for project in dashboard_data:
                completion_pct = project["completion_percentage"]
                project_age = project["project_age_days"]
                
                if completion_pct >= 70:
                    healthy_projects += 1
                elif completion_pct >= 30 or project_age < 30:
                    at_risk_projects += 1
                else:
                    stalled_projects += 1
            
            return {
                "healthy_projects": healthy_projects,
                "at_risk_projects": at_risk_projects,
                "stalled_projects": stalled_projects,
                "total_projects": len(dashboard_data),
                "health_percentage": round((healthy_projects * 100.0 / len(dashboard_data)), 2) if dashboard_data else 0
            }
            
        except Exception as e:
            raise Exception(f"Failed to fetch project health metrics: {str(e)}")

    async def get_user_performance_workload_analysis(self) -> List[Dict[str, Any]]:
        """Get user performance and workload analysis data"""
        try:
            user_data = await self.issue_repo.user_performance_workload_analysis()
            
            # Process the data to ensure proper types and formatting
            processed_data = []
            for item in user_data:
                processed_item = {
                    "user_id": int(item["user_id"]),
                    "user_name": str(item["user_name"]),
                    "email": str(item["email"]),
                    "organization_name": str(item["organization_name"]),
                    "assigned_issues": int(item["assigned_issues"]) if item["assigned_issues"] else 0,
                    "completed_issues": int(item["completed_issues"]) if item["completed_issues"] else 0,
                    "open_issues": int(item["open_issues"]) if item["open_issues"] else 0,
                    "total_story_points_assigned": int(item["total_story_points_assigned"]) if item["total_story_points_assigned"] else 0,
                    "completed_story_points": int(item["completed_story_points"]) if item["completed_story_points"] else 0,
                    "avg_story_points_per_issue": float(item["avg_story_points_per_issue"]) if item["avg_story_points_per_issue"] else 0.0,
                    "comments_made": int(item["comments_made"]) if item["comments_made"] else 0,
                    "activities_logged": int(item["activities_logged"]) if item["activities_logged"] else 0,
                    "weekly_hours": float(item["weekly_hours"]) if item["weekly_hours"] else 0.0,
                    "total_hours_spent": float(item["total_hours_spent"]) if item["total_hours_spent"] else 0.0,
                    "completion_rate": float(item["completion_rate"]) if item["completion_rate"] else 0.0,
                    "days_since_joined": int(item["days_since_joined"]) if item["days_since_joined"] else 0
                }
                processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            raise Exception(f"Failed to fetch user performance analysis: {str(e)}")

    async def get_sprint_velocity_analysis(self) -> List[Dict[str, Any]]:
        """Get sprint velocity analysis data"""
        try:
            sprint_data = await self.issue_repo.sprint_velocity_analysis()
            
            # Process the data to ensure proper types and formatting
            processed_data = []
            for item in sprint_data:
                processed_item = {
                    "sprint_id": int(item["sprint_id"]),
                    "sprint_name": str(item["sprint_name"]),
                    "project_name": str(item["project_name"]),
                    "start_date": str(item["start_date"]) if item["start_date"] else None,
                    "end_date": str(item["end_date"]) if item["end_date"] else None,
                    "status": str(item["status"]),
                    "velocity_target": int(item["velocity_target"]) if item["velocity_target"] else 0,
                    "issues_in_sprint": int(item["issues_in_sprint"]) if item["issues_in_sprint"] else 0,
                    "total_story_points": int(item["total_story_points"]) if item["total_story_points"] else 0,
                    "completed_issues": int(item["completed_issues"]) if item["completed_issues"] else 0,
                    "completed_story_points": int(item["completed_story_points"]) if item["completed_story_points"] else 0,
                    "avg_hours_per_point": float(item["avg_hours_per_point"]) if item["avg_hours_per_point"] else 0.0,
                    "velocity_achievement_percentage": float(item["velocity_achievement_percentage"]) if item["velocity_achievement_percentage"] else 0.0,
                    "sprint_duration_days": int(item["sprint_duration_days"]) if item["sprint_duration_days"] else 0,
                    "sprint_status": str(item["sprint_status"])
                }
                processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            raise Exception(f"Failed to fetch sprint velocity analysis: {str(e)}")

    async def get_team_performance_collaboration_metrics(self) -> List[Dict[str, Any]]:
        """Get team performance and collaboration metrics data"""
        try:
            team_data = await self.issue_repo.team_performance_collaboration_metrics()
            
            # Process the data to ensure proper types and formatting
            processed_data = []
            for item in team_data:
                processed_item = {
                    "team_id": int(item["team_id"]),
                    "team_name": str(item["team_name"]),
                    "organization_name": str(item["organization_name"]),
                    "team_members": int(item["team_members"]) if item["team_members"] else 0,
                    "workspaces_assigned": int(item["workspaces_assigned"]) if item["workspaces_assigned"] else 0,
                    "projects_assigned": int(item["projects_assigned"]) if item["projects_assigned"] else 0,
                    "total_issues_worked": int(item["total_issues_worked"]) if item["total_issues_worked"] else 0,
                    "total_story_points_worked": int(item["total_story_points_worked"]) if item["total_story_points_worked"] else 0,
                    "team_velocity": float(item["team_velocity"]) if item["team_velocity"] else 0.0,
                    "team_comments": int(item["team_comments"]) if item["team_comments"] else 0,
                    "team_activities": int(item["team_activities"]) if item["team_activities"] else 0,
                    "avg_issue_resolution_time": float(item["avg_issue_resolution_time"]) if item["avg_issue_resolution_time"] else 0.0,
                    "completed_issues": int(item["completed_issues"]) if item["completed_issues"] else 0,
                    "team_completion_rate": float(item["team_completion_rate"]) if item["team_completion_rate"] else 0.0
                }
                processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            raise Exception(f"Failed to fetch team performance metrics: {str(e)}")
