from src.core.database import db
import aiomysql


class IssueRepository:

    async def create_issue_type(self, name: str):
        """Create a new issue type"""
        query = """
        INSERT INTO issue_types (name) 
        VALUES (%s)
        """
        return await db.execute_insert(query, [name])

    async def get_all_issue_types(self):
        """Get all issue types"""
        query = """
        SELECT id, name 
        FROM issue_types 
        ORDER BY name ASC
        """
        return await db.execute_query(query)

    async def get_issue_type_by_id(self, issue_type_id: int):
        """Get a specific issue type by ID"""
        query = """
        SELECT id, name 
        FROM issue_types 
        WHERE id = %s
        """
        result = await db.execute_query(query, [issue_type_id])
        return result[0] if result else None

    async def update_issue_type(self, issue_type_id: int, name: str):
        """Update an existing issue type"""
        query = """
        UPDATE issue_types 
        SET name = %s
        WHERE id = %s
        """
        return await db.execute_query(query, [name, issue_type_id])

    async def delete_issue_type(self, issue_type_id: int):
        """Delete an issue type"""
        query = """
        DELETE FROM issue_types 
        WHERE id = %s
        """
        return await db.execute_query(query, [issue_type_id])

    async def issue_type_exists(self, name: str):
        """Check if an issue type with the given name exists"""
        query = """
        SELECT COUNT(*) as count 
        FROM issue_types 
        WHERE name = %s
        """
        result = await db.execute_query(query, [name])
        return result[0]['count'] > 0 if result else False

    # Issues CRUD operations
    async def create_issue(self, project_id: int, title: str, created_by: int, 
                          type_id: int = None, description: str = None, 
                          story_points: int = None, status: str = "open", 
                          priority: str = "medium", parent_issue_id: int = None):
        """Create a new issue"""
        query = """
        INSERT INTO issues (project_id, type_id, title, description, story_points, 
                          status, priority, created_by, parent_issue_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
         return await db.execute_insert(query, [project_id, type_id, title, description,
                                              story_points, status, priority, created_by, parent_issue_id])
        except Exception as e:
            print("error in the query",e)

    async def get_issues_by_project(self, project_id: int):
        """Get all issues for a specific project"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.project_id = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id])

    async def get_issue_by_id(self, issue_id: int):
        """Get a specific issue by ID"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.id = %s
        """
        result = await db.execute_query(query, [issue_id])
        return result[0] if result else None

    async def update_issue(self, issue_id: int, **kwargs):
        """Update an existing issue"""
        # Build dynamic query based on provided fields
        set_clauses = []
        values = []

        for field, value in kwargs.items():
            if value is not None:
                set_clauses.append(f"{field} = %s")
                values.append(value)

        if not set_clauses:
            return None

        # Update the issue
        query = f"""
        UPDATE issues 
        SET {', '.join(set_clauses)}
        WHERE id = %s
        """
        values.append(issue_id)
        result = await db.execute_query(query, values)

        # Handle workload tracking after successful update
        print("this is status")
        print(kwargs.get('status'))
        if kwargs.get('status') == "done":
            await self._track_workload_on_completion(issue_id)

        return result

    async def _track_workload_on_completion(self, issue_id: int):
        """Track workload when issue is marked as done and remove the assignments"""
        conn = await db.get_connection()
        try:
            await conn.autocommit(False)
            await conn.begin()

            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 1️⃣ Insert workload
                insert_query = """
                               INSERT INTO user_workload (issue_assignments_id, hours_spent)
                               SELECT ia.id                               AS issue_assignments_id, \
                                      COALESCE(tv.avg_hours_per_point, 0) AS hours_spent
                               FROM user_team ut
                                        JOIN project_teams pt ON ut.team_id = pt.team_id
                                        JOIN issues i ON i.project_id = pt.project_id
                                        JOIN issue_assignments ia ON i.id = ia.issue_id
                                        JOIN team_velocity tv ON i.project_id = pt.project_id
                               WHERE i.id = %s
                                 AND ut.user_id = ia.assigned_to
                                 AND ia.assigned_to IS NOT NULL; \
                               """
                await cur.execute(insert_query, (issue_id,))

            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 2️⃣ Delete the assignments that were just inserted
                delete_query = """
                DELETE ia
                FROM issue_assignments ia
                         JOIN user_team ut ON ut.user_id = ia.assigned_to
                         JOIN issues i ON i.id = ia.issue_id
                         JOIN project_teams pt ON pt.project_id = i.project_id AND pt.team_id = ut.team_id
                WHERE i.id = %s
                  AND ia.assigned_to IS NOT NULL;
                """
                await cur.execute(delete_query, (issue_id,))

            # Commit the transaction
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            print("Error tracking workload:", e)
            raise
        finally:
            await conn.autocommit(True)
            await db.release_connection(conn)

    async def delete_issue(self, issue_id: int):
        """Delete an issue"""
        query = """
        DELETE FROM issues 
        WHERE id = %s
        """
        return await db.execute_query(query, [issue_id])

    async def get_issues_by_status(self, project_id: int, status: str):
        """Get all issues with a specific status for a project"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.project_id = %s AND i.status = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id, status])

    async def get_issues_by_priority(self, project_id: int, priority: str):
        """Get all issues with a specific priority for a project"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.project_id = %s AND i.priority = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id, priority])

    async def get_sub_issues(self, parent_issue_id: int):
        """Get all sub-issues (children) of a parent issue"""
        query = """
        SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        WHERE i.parent_issue_id = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [parent_issue_id])

    async def issue_exists(self, issue_id: int):
        """Check if an issue exists"""
        query = """
        SELECT COUNT(*) as count 
        FROM issues 
        WHERE id = %s
        """
        result = await db.execute_query(query, [issue_id])
        return result[0]['count'] > 0 if result else False

    # Analytics methods
    async def project_analytics_dashboard(self):
        """Get project analytics dashboard data"""
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
        ORDER BY completion_percentage DESC, total_issues DESC
        """
        return await db.execute_query(query)

    # Issue Assignment methods
    async def assign_issue(self, issue_id: int, assigned_to: int, assigned_by: int) -> int:
        """Assign an issue to a user"""
        query = """
        INSERT INTO issue_assignments (issue_id, assigned_to, assigned_by)
        VALUES (%s, %s, %s)
        """
        try:
            return await db.execute_insert(query, [issue_id, assigned_to, assigned_by])
        except Exception as e:
            print("Error assigning issue:", e)
            raise Exception("Failed to assign issue")

    async def unassign_issue(self, issue_id: int) -> bool:
        """Remove assignment from an issue"""
        query = """
        DELETE FROM issue_assignments 
        WHERE issue_id = %s
        """
        try:
            await db.execute_query(query, [issue_id])
            return True
        except Exception as e:
            print("Error unassigning issue:", e)
            raise Exception("Failed to unassign issue")

    async def get_issue_assignment(self, issue_id: int) -> dict | None:
        """Get current assignment for an issue"""
        query = """
        SELECT ia.id, ia.issue_id, ia.assigned_to, ia.assigned_by, ia.assigned_at,
               u.name as assigned_to_name, u.email as assigned_to_email,
               assigner.name as assigned_by_name, assigner.email as assigned_by_email
        FROM issue_assignments ia
        LEFT JOIN users u ON ia.assigned_to = u.id
        LEFT JOIN users assigner ON ia.assigned_by = assigner.id
        WHERE ia.issue_id = %s
        LIMIT 1
        """
        result = await db.execute_query(query, [issue_id])
        return result[0] if result else None

    async def is_issue_assigned(self, issue_id: int) -> bool:
        """Check if an issue is currently assigned"""
        query = """
        SELECT COUNT(*) as count 
        FROM issue_assignments 
        WHERE issue_id = %s
        """
        result = await db.execute_query(query, [issue_id])
        return result[0]['count'] > 0 if result else False

    async def get_user_assigned_issues(self, user_id: int, project_id: int = None) -> list[dict]:
        """Get all issues assigned to a user"""
        if project_id:
            query = """
            SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
                   i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
                   i.created_at, i.updated_at, ia.assigned_at, ia.assigned_by
            FROM issue_assignments ia
            JOIN issues i ON ia.issue_id = i.id
            WHERE ia.assigned_to = %s AND i.project_id = %s
            ORDER BY ia.assigned_at DESC
            """
            params = [user_id, project_id]
        else:
            query = """
            SELECT i.id, i.project_id, i.type_id, i.title, i.description, 
                   i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
                   i.created_at, i.updated_at, ia.assigned_at, ia.assigned_by
            FROM issue_assignments ia
            JOIN issues i ON ia.issue_id = i.id
            WHERE ia.assigned_to = %s
            ORDER BY ia.assigned_at DESC
            """
            params = [user_id]
        
        return await db.execute_query(query, params)

    async def update_assignment(self, issue_id: int, assigned_to: int, assigned_by: int) -> bool:
        """Update existing assignment"""
        query = """
        UPDATE issue_assignments 
        SET assigned_to = %s, assigned_by = %s, assigned_at = CURRENT_TIMESTAMP
        WHERE issue_id = %s
        """
        try:
            await db.execute_query(query, [assigned_to, assigned_by, issue_id])
            return True
        except Exception as e:
            print("Error updating assignment:", e)
            raise Exception("Failed to update assignment")

    async def user_performance_workload_analysis(self):
        """Get user performance and workload analysis data"""
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
        ORDER BY completion_rate DESC, total_story_points_assigned DESC
        """
        return await db.execute_query(query)

    async def sprint_velocity_analysis(self):
        """Get sprint velocity analysis data"""
        query = """
        SELECT 
            s.id as sprint_id,
            s.name as sprint_name,
            p.name as project_name,
            s.start_date,
            s.end_date,
            s.status,
            s.velocity_target,
            COUNT(DISTINCT iss.issue_id) as issues_in_sprint,
            SUM(i.story_points) as total_story_points,
            COUNT(DISTINCT CASE WHEN i.status = 'completed' THEN iss.issue_id END) as completed_issues,
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
        LEFT JOIN issue_sprints iss ON s.id = iss.sprint_id
        LEFT JOIN issues i ON iss.issue_id = i.id
        LEFT JOIN team_velocity tv ON s.project_id = tv.project_id
        GROUP BY s.id, s.name, p.name, s.start_date, s.end_date, s.status, s.velocity_target, tv.avg_hours_per_point
        ORDER BY s.start_date DESC
        """
        return await db.execute_query(query)

    async def team_performance_collaboration_metrics(self):
        """Get team performance and collaboration metrics data"""
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
        ORDER BY team_completion_rate DESC, total_story_points_worked DESC
        """
        return await db.execute_query(query)

    # Label management methods
    async def create_label(self, project_id: int, name: str, description: str = None, color: str = None):
        """Create a new label for a project"""
        query = """
        INSERT INTO labels (project_id, name, description, color) 
        VALUES (%s, %s, %s, %s)
        """
        return await db.execute_insert(query, [project_id, name, description, color])

    async def get_project_labels(self, project_id: int):
        """Get all labels for a specific project"""
        query = """
        SELECT id, project_id, name, description, color, created_at
        FROM labels 
        WHERE project_id = %s
        ORDER BY name ASC
        """
        return await db.execute_query(query, [project_id])

    async def get_label_by_id(self, label_id: int):
        """Get a specific label by ID"""
        query = """
        SELECT id, project_id, name, description, color, created_at
        FROM labels 
        WHERE id = %s
        """
        result = await db.execute_query(query, [label_id])
        return result[0] if result else None

    async def update_label(self, label_id: int, **kwargs):
        """Update an existing label"""
        # Build dynamic query based on provided fields
        set_clauses = []
        values = []
        
        for field, value in kwargs.items():
            if value is not None:
                set_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not set_clauses:
            return None
            
        query = f"""
        UPDATE labels 
        SET {', '.join(set_clauses)}
        WHERE id = %s
        """
        values.append(label_id)
        return await db.execute_query(query, values)

    async def delete_label(self, label_id: int):
        """Delete a label"""
        query = """
        DELETE FROM labels 
        WHERE id = %s
        """
        return await db.execute_query(query, [label_id])

    async def label_exists(self, label_id: int):
        """Check if a label exists"""
        query = """
        SELECT COUNT(*) as count 
        FROM labels 
        WHERE id = %s
        """
        result = await db.execute_query(query, [label_id])
        return result[0]['count'] > 0 if result else False

    async def label_name_exists_in_project(self, project_id: int, name: str, exclude_label_id: int = None):
        """Check if a label name already exists in a project"""
        if exclude_label_id:
            query = """
            SELECT COUNT(*) as count 
            FROM labels 
            WHERE project_id = %s AND name = %s AND id != %s
            """
            result = await db.execute_query(query, [project_id, name, exclude_label_id])
        else:
            query = """
            SELECT COUNT(*) as count 
            FROM labels 
            WHERE project_id = %s AND name = %s
            """
            result = await db.execute_query(query, [project_id, name])
        return result[0]['count'] > 0 if result else False

    # Issue label methods
    async def add_label_to_issue(self, issue_id: int, label_id: int):
        """Add a label to an issue"""
        query = """
        INSERT IGNORE INTO issue_labels (issue_id, label_id) 
        VALUES (%s, %s)
        """
        return await db.execute_query(query, [issue_id, label_id])

    async def remove_label_from_issue(self, issue_id: int, label_id: int):
        """Remove a label from an issue"""
        query = """
        DELETE FROM issue_labels 
        WHERE issue_id = %s AND label_id = %s
        """
        return await db.execute_query(query, [issue_id, label_id])

    async def get_issue_labels(self, issue_id: int):
        """Get all labels for a specific issue"""
        query = """
        SELECT il.issue_id, il.label_id, l.name as label_name, l.color as label_color
        FROM issue_labels il
        JOIN labels l ON il.label_id = l.id
        WHERE il.issue_id = %s
        ORDER BY l.name ASC
        """
        return await db.execute_query(query, [issue_id])

    async def get_issues_by_label(self, project_id: int, label_id: int):
        """Get all issues with a specific label in a project"""
        query = """
        SELECT DISTINCT i.id, i.project_id, i.type_id, i.title, i.description, 
               i.story_points, i.status, i.priority, i.created_by, i.parent_issue_id,
               i.created_at, i.updated_at
        FROM issues i
        JOIN issue_labels il ON i.id = il.issue_id
        WHERE i.project_id = %s AND il.label_id = %s
        ORDER BY i.created_at DESC
        """
        return await db.execute_query(query, [project_id, label_id])

    async def issue_has_label(self, issue_id: int, label_id: int):
        """Check if an issue has a specific label"""
        query = """
        SELECT COUNT(*) as count 
        FROM issue_labels 
        WHERE issue_id = %s AND label_id = %s
        """
        result = await db.execute_query(query, [issue_id, label_id])
        return result[0]['count'] > 0 if result else False

    async def get_label_usage_count(self, label_id: int):
        """Get the number of issues using a specific label"""
        query = """
        SELECT COUNT(*) as count 
        FROM issue_labels 
        WHERE label_id = %s
        """
        result = await db.execute_query(query, [label_id])
        return result[0]['count'] if result else 0




