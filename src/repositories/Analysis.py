from src.core.database import db


class AnalysisRepository:

    async def User_Performance_Workload_Analysis(self):
        query = """
        SELECT 
    u.id as user_id,
    u.name as user_name,
    u.email,
    o.name as organization_name,
    COUNT(DISTINCT ia.issue_id) as assigned_issues,
    COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN ia.issue_id END) as completed_issues,
    COUNT(DISTINCT CASE WHEN i.status = 'open' THEN ia.issue_id END) as open_issues,
    SUM(i.story_points) as total_story_points_assigned,
    SUM(CASE WHEN i.status = 'completed' THEN i.story_points ELSE 0 END) as completed_story_points,
    AVG(i.story_points) as avg_story_points_per_issue,
    COUNT(DISTINCT ic.id) as comments_made,
    COUNT(DISTINCT ih.id) as activities_logged,
    uc.weekly_hours,
    SUM(uw.hours_spent) as total_hours_spent,
    CASE 
        WHEN COUNT(DISTINCT ia.issue_id) = 0 THEN 0
        ELSE (COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN ia.issue_id END) * 100.0 / COUNT(DISTINCT ia.issue_id))
    END as completion_rate,
    TIMESTAMPDIFF(DAY, u.created_at, NOW()) as days_since_joined
FROM users u
JOIN organization_users ou ON u.id = ou.user_id
JOIN organizations o ON ou.organization_id = o.id
LEFT JOIN issue_assignments ia ON u.id = ia.assigned_to
LEFT JOIN issues i ON ia.issue_id = i.id
LEFT JOIN issue_comments ic ON u.id = ic.user_id
LEFT JOIN issue_history ih ON u.id = ih.user_id
LEFT JOIN user_capacity uc ON u.id = uc.user_id AND o.id = uc.organization_id
LEFT JOIN user_workload uw ON ia.id = uw.issue_assignments_id
GROUP BY u.id, u.name, u.email, o.name, uc.weekly_hours, u.created_at
ORDER BY completion_rate DESC, total_story_points_assigned DESC;

        """
        return await db.execute_query(query)


  










