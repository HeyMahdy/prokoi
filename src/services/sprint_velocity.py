from src.repositories.Analysis import AnalysisRepository
from src.schemas.sprint_velocity import SprintVelocityResponse
from typing import List

class SprintVelocityService:
    def __init__(self):
        self.analysis_repo = AnalysisRepository()

    async def get_sprint_velocity_analysis(self) -> List[SprintVelocityResponse]:
        """Get sprint velocity analysis for all sprints"""
        try:
            # Get raw data from repository
            raw_data = await self.analysis_repo.Sprint_Velocity_Analysis()
            
            if not raw_data:
                return []
            
            # Process the data
            processed_sprints = []
            for sprint_data in raw_data:
                sprint = SprintVelocityResponse(
                    sprint_id=int(sprint_data['sprint_id']),
                    sprint_name=str(sprint_data['sprint_name']),
                    project_name=str(sprint_data['project_name']),
                    start_date=sprint_data['start_date'],
                    end_date=sprint_data['end_date'],
                    status=str(sprint_data['status']),
                    velocity_target=int(sprint_data['velocity_target']) if sprint_data['velocity_target'] else None,
                    
                    # Sprint content metrics
                    issues_in_sprint=int(sprint_data['issues_in_sprint']) if sprint_data['issues_in_sprint'] else 0,
                    total_story_points=int(sprint_data['total_story_points']) if sprint_data['total_story_points'] else 0,
                    completed_issues=int(sprint_data['completed_issues']) if sprint_data['completed_issues'] else 0,
                    completed_story_points=int(sprint_data['completed_story_points']) if sprint_data['completed_story_points'] else 0,
                    
                    # Velocity metrics
                    avg_hours_per_point=float(sprint_data['avg_hours_per_point']) if sprint_data['avg_hours_per_point'] else None,
                    velocity_achievement_percentage=float(sprint_data['velocity_achievement_percentage']) if sprint_data['velocity_achievement_percentage'] else 0.0,
                    
                    # Sprint timing
                    sprint_duration_days=int(sprint_data['sprint_duration_days']) if sprint_data['sprint_duration_days'] else 0,
                    sprint_status=str(sprint_data['sprint_status'])
                )
                processed_sprints.append(sprint)
            
            return processed_sprints
            
        except Exception as e:
            print(f"Failed to get sprint velocity analysis: {e}")
            raise Exception(f"Failed to fetch sprint velocity data: {str(e)}")
