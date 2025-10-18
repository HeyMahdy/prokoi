from src.core.database import db


class AnalysisRepository:
    async def Project_Analytics_Dashboard(self):

        query = """
         SELECT 
         p.id as project_id,
         p.name as project_name,
         w.name as workspace_name,
         o.name as organization_name,
         COUNT(DISTINCT i.id) as total_issues,
         COUNT(DISTINCT CASE WHEN i.status = 'open' THEN i.id END) as open_issues,
         COUNT(DISTINCT CASE WHEN i.status = 'in-progress' THEN i.id END) as in_progress_issues,
         COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN i.id END) as completed_issues,
         AVG(i.story_points) as avg_story_points,
         SUM(i.story_points) as total_story_points,
         COUNT(DISTINCT i.created_by) as contributors,
         COUNT(DISTINCT ic.id) as total_comments,
         TIMESTAMPDIFF(DAY, p.created_at, NOW()) as project_age_days,
         CASE 
           WHEN COUNT(DISTINCT i.id) = 0 THEN 0
           ELSE (COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN i.id END) * 100.0 / COUNT(DISTINCT i.id))
         END as completion_percentage
         FROM projects p
         JOIN workspaces w ON p.workspace_id = w.id
         JOIN organizations o ON w.organization_id = o.id
         LEFT JOIN issues i ON p.id = i.project_id
         LEFT JOIN issue_comments ic ON i.id = ic.issue_id
         WHERE p.status = 'active'
         GROUP BY p.id, p.name, w.name, o.name, p.created_at
         ORDER BY completion_percentage DESC, total_issues DESC;
        """
        return await db.execute_query(query)



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


    async def Sprint_Velocity_Analysis(self):
        query=  """
            
            SELECT 
    s.id as sprint_id,
    s.name as sprint_name,
    p.name as project_name,
    s.start_date,
    s.end_date,
    s.status,
    s.velocity_target,
    COUNT(DISTINCT is.issue_id) as issues_in_sprint,
    SUM(i.story_points) as total_story_points,
    COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN is.issue_id END) as completed_issues,
    SUM(CASE WHEN i.status = 'completed' THEN i.story_points ELSE 0 END) as completed_story_points,
    tv.avg_hours_per_point,
    CASE 
        WHEN s.velocity_target > 0 THEN (SUM(CASE WHEN i.status = 'completed' THEN i.story_points ELSE 0 END) * 100.0 / s.velocity_target)
        ELSE 0
    END as velocity_achievement_percentage,
    TIMESTAMPDIFF(DAY, s.start_date, s.end_date) as sprint_duration_days,
    CASE 
        WHEN s.end_date < CURDATE() THEN 'completed'
        WHEN s.start_date <= CURDATE() AND s.end_date >= CURDATE() THEN 'active'
        ELSE 'upcoming'
    END as sprint_status
FROM sprints s
JOIN projects p ON s.project_id = p.id
LEFT JOIN issue_sprints is ON s.id = is.sprint_id
LEFT JOIN issues i ON is.issue_id = i.id
LEFT JOIN team_velocity tv ON s.project_id = tv.project_id
GROUP BY s.id, s.name, p.name, s.start_date, s.end_date, s.status, s.velocity_target, tv.avg_hours_per_point
ORDER BY s.start_date DESC;
            """
        return await db.execute_query(query)




    async def Team_Performance_Collaboration_Metrics(self):
            query = """
            SELECT 
    t.id as team_id,
    t.name as team_name,
    o.name as organization_name,
    COUNT(DISTINCT ut.user_id) as team_members,
    COUNT(DISTINCT tw.workspace_id) as workspaces_assigned,
    COUNT(DISTINCT pt.project_id) as projects_assigned,
    COUNT(DISTINCT i.id) as total_issues_worked,
    SUM(i.story_points) as total_story_points_worked,
    AVG(tv.avg_hours_per_point) as team_velocity,
    COUNT(DISTINCT ic.id) as team_comments,
    COUNT(DISTINCT ih.id) as team_activities,
    AVG(TIMESTAMPDIFF(HOUR, i.created_at, i.updated_at)) as avg_issue_resolution_time,
    COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN i.id END) as completed_issues,
    CASE 
        WHEN COUNT(DISTINCT i.id) = 0 THEN 0
        ELSE (COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN i.id END) * 100.0 / COUNT(DISTINCT i.id))
    END as team_completion_rate
FROM teams t
JOIN organizations o ON t.organization_id = o.id
LEFT JOIN user_team ut ON t.id = ut.team_id
LEFT JOIN team_workspaces tw ON t.id = tw.team_id
LEFT JOIN project_teams pt ON t.id = pt.team_id
LEFT JOIN issues i ON pt.project_id = i.project_id
LEFT JOIN team_velocity tv ON t.id = tv.team_id
LEFT JOIN issue_comments ic ON i.id = ic.issue_id
LEFT JOIN issue_history ih ON i.id = ih.issue_id
GROUP BY t.id, t.name, o.name
ORDER BY team_completion_rate DESC, total_story_points_worked DESC;
            """
            return await db.execute_query(query)






