from src.repositories.Analysis import AnalysisRepository
from src.schemas.user_performance import UserPerformanceResponse
from typing import List

class UserPerformanceService:
    def __init__(self):
        self.analysis_repo = AnalysisRepository()

    async def get_user_performance_metrics(self) -> List[UserPerformanceResponse]:
        """Get user performance and workload analysis for all users"""
        try:
            # Get raw data from repository
            raw_data = await self.analysis_repo.User_Performance_Workload_Analysis()
            
            if not raw_data:
                return []
            
            # Process the data
            processed_users = []
            for user_data in raw_data:
                user = UserPerformanceResponse(
                    user_id=int(user_data['user_id']),
                    user_name=str(user_data['user_name']),
                    email=str(user_data['email']),
                    organization_name=str(user_data['organization_name']),
                    
                    # Issue assignment metrics
                    assigned_issues=int(user_data['assigned_issues']) if user_data['assigned_issues'] else 0,
                    completed_issues=int(user_data['completed_issues']) if user_data['completed_issues'] else 0,
                    open_issues=int(user_data['open_issues']) if user_data['open_issues'] else 0,
                    completion_rate=float(user_data['completion_rate']) if user_data['completion_rate'] else 0.0,
                    
                    # Story points metrics
                    total_story_points_assigned=int(user_data['total_story_points_assigned']) if user_data['total_story_points_assigned'] else 0,
                    completed_story_points=int(user_data['completed_story_points']) if user_data['completed_story_points'] else 0,
                    avg_story_points_per_issue=float(user_data['avg_story_points_per_issue']) if user_data['avg_story_points_per_issue'] else 0.0,
                    
                    # Activity metrics
                    comments_made=int(user_data['comments_made']) if user_data['comments_made'] else 0,
                    activities_logged=int(user_data['activities_logged']) if user_data['activities_logged'] else 0,
                    
                    # Workload metrics
                    weekly_hours=int(user_data['weekly_hours']) if user_data['weekly_hours'] else None,
                    total_hours_spent=float(user_data['total_hours_spent']) if user_data['total_hours_spent'] else None,
                    
                    # User tenure
                    days_since_joined=int(user_data['days_since_joined']) if user_data['days_since_joined'] else 0
                )
                processed_users.append(user)
            
            return processed_users
            
        except Exception as e:
            print(f"Failed to get user performance metrics: {e}")
            raise Exception(f"Failed to fetch user performance data: {str(e)}")
