from src.repositories.Analysis import AnalysisRepository
from src.schemas.team_performance import TeamPerformanceResponse
from typing import List

class TeamPerformanceService:
    def __init__(self):
        self.analysis_repo = AnalysisRepository()

    async def get_team_performance_metrics(self) -> List[TeamPerformanceResponse]:
        """Get team performance and collaboration metrics for all teams"""
        try:
            # Get raw data from repository
            raw_data = await self.analysis_repo.Team_Performance_Collaboration_Metrics()
            
            if not raw_data:
                return []
            
            # Process the data
            processed_teams = []
            for team_data in raw_data:
                team = TeamPerformanceResponse(
                    team_id=int(team_data['team_id']),
                    team_name=str(team_data['team_name']),
                    organization_name=str(team_data['organization_name']),
                    
                    # Team composition metrics
                    team_members=int(team_data['team_members']) if team_data['team_members'] else 0,
                    workspaces_assigned=int(team_data['workspaces_assigned']) if team_data['workspaces_assigned'] else 0,
                    projects_assigned=int(team_data['projects_assigned']) if team_data['projects_assigned'] else 0,
                    
                    # Work metrics
                    total_issues_worked=int(team_data['total_issues_worked']) if team_data['total_issues_worked'] else 0,
                    total_story_points_worked=int(team_data['total_story_points_worked']) if team_data['total_story_points_worked'] else 0,
                    completed_issues=int(team_data['completed_issues']) if team_data['completed_issues'] else 0,
                    team_completion_rate=float(team_data['team_completion_rate']) if team_data['team_completion_rate'] else 0.0,
                    
                    # Performance metrics
                    team_velocity=float(team_data['team_velocity']) if team_data['team_velocity'] else None,
                    avg_issue_resolution_time=float(team_data['avg_issue_resolution_time']) if team_data['avg_issue_resolution_time'] else None,
                    
                    # Collaboration metrics
                    team_comments=int(team_data['team_comments']) if team_data['team_comments'] else 0,
                    team_activities=int(team_data['team_activities']) if team_data['team_activities'] else 0
                )
                processed_teams.append(team)
            
            return processed_teams
            
        except Exception as e:
            print(f"Failed to get team performance metrics: {e}")
            raise Exception(f"Failed to fetch team performance data: {str(e)}")
