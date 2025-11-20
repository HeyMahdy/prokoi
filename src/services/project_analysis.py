from src.repositories.Analysis import AnalysisRepository
from src.schemas.project_analysis import ProjectAnalysisDepthResponse, ProjectUser, ProjectTeam
from typing import Optional
import json
from src.core.logger import setup_logger

logger = setup_logger(__name__)

class ProjectAnalysisService:
    def __init__(self):
        self.analysis_repo = AnalysisRepository()

    async def get_project_analysis_depth(self, project_id: int) -> Optional[ProjectAnalysisDepthResponse]:
        """Get detailed project analysis with depth metrics"""
        try:
            # Get raw data from repository
            raw_data = await self.analysis_repo.project_analysis_depth(project_id)
            
            if not raw_data or len(raw_data) == 0:
                return None
            
            # Get the first (and only) result
            data = raw_data[0]
            
            # Parse JSON strings for users and teams
            project_users = []
            if data.get('project_users_json'):
                try:
                    users_json = data['project_users_json']
                    # Handle multiple JSON objects separated by commas
                    if users_json:
                        # Split by '},{' and fix JSON format
                        users_str = users_json.replace('}{', '},{')
                        users_list = json.loads(f'[{users_str}]')
                        project_users = [ProjectUser(**user) for user in users_list]
                except (json.JSONDecodeError, TypeError):
                    project_users = []
            
            project_teams = []
            if data.get('project_teams_json'):
                try:
                    teams_json = data['project_teams_json']
                    # Handle multiple JSON objects separated by commas
                    if teams_json:
                        # Split by '},{' and fix JSON format
                        teams_str = teams_json.replace('}{', '},{')
                        teams_list = json.loads(f'[{teams_str}]')
                        project_teams = [ProjectTeam(**team) for team in teams_list]
                except (json.JSONDecodeError, TypeError):
                    project_teams = []
            
            # Create response object
            response = ProjectAnalysisDepthResponse(
                project_id=int(data['project_id']),
                project_name=str(data['project_name']),
                project_status=str(data['project_status']),
                workspace_name=str(data['workspace_name']),
                organization_name=str(data['organization_name']),
                
                # User and Team metrics
                total_users=int(data['total_users']) if data['total_users'] else 0,
                total_teams=int(data['total_teams']) if data['total_teams'] else 0,
                project_users=project_users,
                project_teams=project_teams,
                
                # Issue metrics
                total_issues=int(data['total_issues']) if data['total_issues'] else 0,
                open_issues=int(data['open_issues']) if data['open_issues'] else 0,
                in_progress_issues=int(data['in_progress_issues']) if data['in_progress_issues'] else 0,
                completed_issues=int(data['completed_issues']) if data['completed_issues'] else 0,
                high_priority_issues=int(data['high_priority_issues']) if data['high_priority_issues'] else 0,
                critical_issues=int(data['critical_issues']) if data['critical_issues'] else 0,
                
                # Sprint metrics
                total_sprints=int(data['total_sprints']) if data['total_sprints'] else 0,
                active_sprints=int(data['active_sprints']) if data['active_sprints'] else 0,
                
                # Time tracking metrics
                total_hours_logged=float(data['total_hours_logged']) if data['total_hours_logged'] else 0.0,
                avg_hours_per_log=float(data['avg_hours_per_log']) if data['avg_hours_per_log'] else 0.0,
                avg_team_velocity=float(data['avg_team_velocity']) if data['avg_team_velocity'] else 0.0,
                
                # Activity metrics
                total_comments=int(data['total_comments']) if data['total_comments'] else 0,
                total_attachments=int(data['total_attachments']) if data['total_attachments'] else 0,
                recent_activity=int(data['recent_activity']) if data['recent_activity'] else 0,
                
                # Story points metrics
                total_story_points=int(data['total_story_points']) if data['total_story_points'] else 0,
                avg_story_points=float(data['avg_story_points']) if data['avg_story_points'] else 0.0
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get project analysis depth: {e}")
            raise Exception(f"Failed to fetch project analysis: {str(e)}")
