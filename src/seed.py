import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta
from faker import Faker
from passlib.context import CryptContext

fake = Faker()

# Password context matching your application
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Default password for all test users
DEFAULT_PASSWORD = "Test@1234"

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'prokoi'
}

def create_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def get_password_hash(password: str) -> str:
    """Hash a password using argon2"""
    return pwd_context.hash(password)

def clear_existing_data(cursor):
    """Clear existing test data"""
    print("Clearing existing test data...")
    
    # Disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    
    # Clear tables in reverse dependency order
    tables_to_clear = [
        'user_workload', 'issue_assignments', 'issue_sprints', 'time_logs',
        'issue_history', 'issue_labels', 'checklist_items', 'checklists',
        'attachments', 'issue_comments', 'issues', 'sprints', 'projects',
        'workspaces', 'user_team', 'teams', 'organization_users', 'users',
        'organizations', 'issue_types'
    ]
    
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared {table}")
        except Error as e:
            print(f"Could not clear {table}: {e}")
    
    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")

def seed_organizations(cursor, main_user_id):
    """Seed organizations table - all created by main user"""
    print("Seeding organizations...")
    org_ids = []
    
    # Create 3 test organizations all owned by main user
    organizations = [
        "TechCorp Solutions",
        "Innovation Labs", 
        "Digital Ventures"
    ]
    
    for name in organizations:
        cursor.execute(
            "INSERT INTO organizations (name) VALUES (%s)",
            (name,)
        )
        org_id = cursor.lastrowid
        org_ids.append(org_id)
        
        # Add main user as the creator/owner of this organization
        cursor.execute(
            "INSERT INTO organization_users (organization_id, user_id) VALUES (%s, %s)",
            (org_id, main_user_id)
        )
    
    print(f"Created {len(org_ids)} organizations (all owned by main user)")
    return org_ids

def seed_test_users(cursor):
    """Seed test users - main user first, then others"""
    print("Seeding test users...")
    user_ids = []
    user_credentials = []
    
    # Hash the default password once
    password_hash = get_password_hash(DEFAULT_PASSWORD)
    
    # Create main user first (the one who owns all organizations)
    main_name = "Mahdy Ahmed"
    main_email = "mahdy@gmail.com"
    
    cursor.execute(
        """INSERT INTO users (name, email, password_hash, last_login_at)
           VALUES (%s, %s, %s, %s)""",
        (main_name, main_email, password_hash, datetime.now())
    )
    main_user_id = cursor.lastrowid
    user_ids.append(main_user_id)
    user_credentials.append({'email': main_email, 'password': DEFAULT_PASSWORD, 'role': 'main_owner'})
    
    # Create 9 additional users
    for i in range(1, 10):
        name = f"Team Member {i}"
        email = f"member{i}@gmail.com"
        
        cursor.execute(
            """INSERT INTO users (name, email, password_hash, last_login_at)
               VALUES (%s, %s, %s, %s)""",
            (name, email, password_hash, datetime.now())
        )
        user_ids.append(cursor.lastrowid)
        user_credentials.append({'email': email, 'password': DEFAULT_PASSWORD, 'role': 'member'})
    
    print(f"Created {len(user_ids)} test users (1 main owner + 9 members)")
    return user_ids, user_credentials, main_user_id

def seed_organization_users(cursor, org_ids, user_ids, main_user_id):
    """Assign other users to organizations (main user already assigned)"""
    print("Assigning other users to organizations...")
    count = 0
    
    # Get other users (exclude main user)
    other_users = [uid for uid in user_ids if uid != main_user_id]
    
    for org_id in org_ids:
        # Assign 3-5 random users to each organization
        num_users = min(random.randint(3, 5), len(other_users))
        selected_users = random.sample(other_users, num_users)
        
        for user_id in selected_users:
            cursor.execute(
                """INSERT IGNORE INTO organization_users (organization_id, user_id) 
                   VALUES (%s, %s)""",
                (org_id, user_id)
            )
            count += 1
    
    print(f"Created {count} additional organization-user relationships")

def seed_teams(cursor, org_ids):
    """Seed teams for each organization"""
    print("Seeding teams...")
    team_ids = []
    team_org_map = {}
    
    team_names = [
        "Frontend Team", "Backend Team", "DevOps Team", "QA Team", "Design Team"
    ]
    
    for org_id in org_ids:
        # Create 3-4 teams per organization
        org_teams = random.sample(team_names, random.randint(3, 4))
        for team_name in org_teams:
            cursor.execute(
                """INSERT INTO teams (organization_id, name)
                   VALUES (%s, %s)""",
                (org_id, team_name)
            )
            team_id = cursor.lastrowid
            team_ids.append(team_id)
            team_org_map[team_id] = org_id
    
    print(f"Created {len(team_ids)} teams")
    return team_ids, team_org_map

def seed_user_team(cursor, team_ids, user_ids, team_org_map):
    """Assign users to teams"""
    print("Assigning users to teams...")
    count = 0
    
    # Get org-user mapping
    cursor.execute("SELECT organization_id, user_id FROM organization_users")
    org_users = {}
    for org_id, user_id in cursor.fetchall():
        if org_id not in org_users:
            org_users[org_id] = []
        org_users[org_id].append(user_id)
    
    for team_id in team_ids:
        org_id = team_org_map[team_id]
        available_users = org_users.get(org_id, [])
        
        if available_users:
            # Each team has 4-6 members
            team_size = min(random.randint(4, 6), len(available_users))
            selected_users = random.sample(available_users, team_size)
            
            for user_id in selected_users:
                cursor.execute(
                    """INSERT INTO user_team (team_id, user_id)
                       VALUES (%s, %s)""",
                    (team_id, user_id)
                )
                count += 1
    
    print(f"Created {count} user-team assignments")

def seed_workspaces(cursor, org_ids, user_ids, team_ids, team_org_map):
    """Seed workspaces"""
    print("Seeding workspaces...")
    workspace_ids = []
    workspace_org_map = {}
    
    workspace_names = [
        "Development Workspace", "Testing Workspace", "Production Workspace",
        "Staging Workspace", "Research Workspace"
    ]
    
    for org_id in org_ids:
        # Get users in this org
        cursor.execute(
            "SELECT user_id FROM organization_users WHERE organization_id = %s",
            (org_id,)
        )
        org_user_ids = [row[0] for row in cursor.fetchall()]
        
        if not org_user_ids:
            continue
        
        # Create 2-3 workspaces per org
        org_workspaces = random.sample(workspace_names, random.randint(2, 3))
        for workspace_name in org_workspaces:
            creator_id = random.choice(org_user_ids)
            
            # Assign a team from same org
            org_teams = [tid for tid, oid in team_org_map.items() if oid == org_id]
            team_id = random.choice(org_teams) if org_teams else None
            
            cursor.execute(
                """INSERT INTO workspaces (name, user_id, organization_id)
                   VALUES (%s, %s, %s)""",
                (workspace_name, creator_id, org_id)
            )
            workspace_id = cursor.lastrowid
            workspace_ids.append(workspace_id)
            workspace_org_map[workspace_id] = org_id
    
    print(f"Created {len(workspace_ids)} workspaces")
    return workspace_ids, workspace_org_map

def seed_projects(cursor, workspace_ids, user_ids):
    """Seed projects"""
    print("Seeding projects...")
    project_ids = []
    statuses = ['pending', 'active', 'inactive', 'completed']
    
    project_names = [
        "E-commerce Platform", "Mobile App", "API Gateway", "Data Analytics",
        "User Management", "Payment System", "Notification Service", "File Storage"
    ]
    
    for workspace_id in workspace_ids:
        # 2-4 projects per workspace
        workspace_projects = random.sample(project_names, random.randint(2, 4))
        for project_name in workspace_projects:
            creator_id = random.choice(user_ids)
            status = random.choice(statuses)
            
            cursor.execute(
                """INSERT INTO projects (name, workspace_id, created_by, status)
                   VALUES (%s, %s, %s, %s)""",
                (project_name, workspace_id, creator_id, status)
            )
            project_ids.append(cursor.lastrowid)
    
    print(f"Created {len(project_ids)} projects")
    return project_ids

def seed_project_teams(cursor, project_ids, team_ids, team_org_map):
    """Link projects to teams"""
    print("Linking projects to teams...")
    count = 0
    
    # Get project-org mapping through workspaces
    cursor.execute("""
        SELECT p.id, w.organization_id 
        FROM projects p 
        JOIN workspaces w ON p.workspace_id = w.id
    """)
    project_orgs = {row[0]: row[1] for row in cursor.fetchall()}
    
    for project_id in project_ids:
        org_id = project_orgs.get(project_id)
        if not org_id:
            continue
        
        # Get teams from same org
        org_teams = [tid for tid, oid in team_org_map.items() if oid == org_id]
        
        # Assign 1-2 teams to each project
        selected_teams = random.sample(org_teams, min(random.randint(1, 2), len(org_teams)))
        
        for team_id in selected_teams:
            cursor.execute(
                """INSERT INTO project_teams (project_id, team_id)
                   VALUES (%s, %s)""",
                (project_id, team_id)
            )
            count += 1
    
    print(f"Created {count} project-team relationships")

def seed_sprints(cursor, project_ids):
    """Seed sprints"""
    print("Seeding sprints...")
    sprint_ids = []
    statuses = ['planning', 'active', 'completed', 'cancelled']
    
    for project_id in project_ids:
        # 2-4 sprints per project
        for i in range(random.randint(2, 4)):
            name = f"Sprint {i + 1}"
            description = f"Development sprint for project {project_id}"
            start_date = fake.date_between(start_date='-60d', end_date='today')
            end_date = start_date + timedelta(days=14)
            status = random.choice(statuses)
            goal = f"Complete features for sprint {i + 1}"
            velocity_target = random.randint(20, 50)
            
            cursor.execute(
                """INSERT INTO sprints (project_id, name, description, start_date,
                                        end_date, status, goal, velocity_target)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (project_id, name, description, start_date, end_date,
                 status, goal, velocity_target)
            )
            sprint_ids.append(cursor.lastrowid)
    
    print(f"Created {len(sprint_ids)} sprints")
    return sprint_ids


def seed_issues(cursor, project_ids, user_ids):
    """Seed issues"""
    print("Seeding issues...")
    issue_ids = []
    statuses = ['open', 'in_progress', 'review', 'done', 'closed']
    priorities = ['low', 'medium', 'high', 'critical']

    # Get issue types
    cursor.execute("SELECT id FROM issue_types")
    type_ids = [row[0] for row in cursor.fetchall()]

    base_issue_titles = [
        "Implement user authentication", "Fix login bug", "Add email notifications",
        "Create dashboard UI", "Optimize database queries", "Add file upload feature",
        "Implement search functionality", "Fix responsive design", "Add data validation",
        "Create API documentation", "Implement caching", "Add error handling"
    ]

    for project_id in project_ids:
        # 8-15 issues per project
        num_issues = random.randint(8, 15)

        for i in range(num_issues):
            # Use base titles and add variation
            if i < len(base_issue_titles):
                title = base_issue_titles[i]
            else:
                # Generate additional titles
                title = f"Task {i + 1} for project {project_id}"

            description = f"Description for {title}"
            type_id = random.choice(type_ids)
            status = random.choice(statuses)
            priority = random.choice(priorities)
            story_points = random.choice([1, 2, 3, 5, 8, 13, None])
            creator_id = random.choice(user_ids)

            cursor.execute(
                """INSERT INTO issues (project_id, type_id, title, description,
                                       status, priority, story_points, created_by)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (project_id, type_id, title, description, status,
                 priority, story_points, creator_id)
            )
            issue_ids.append(cursor.lastrowid)

    print(f"Created {len(issue_ids)} issues")
    return issue_ids
def seed_issue_assignments(cursor, issue_ids, user_ids):
    """Seed issue assignments"""
    print("Seeding issue assignments...")
    count = 0
    
    for issue_id in issue_ids:
        # 70% of issues are assigned
        if random.random() < 0.7:
            assigned_to = random.choice(user_ids)
            assigned_by = random.choice(user_ids)
            
            cursor.execute(
                """INSERT INTO issue_assignments (issue_id, assigned_to, assigned_by)
                   VALUES (%s, %s, %s)""",
                (issue_id, assigned_to, assigned_by)
            )
            count += 1
    
    print(f"Created {count} issue assignments")

def seed_issue_sprints(cursor, issue_ids, sprint_ids):
    """Link issues to sprints"""
    print("Linking issues to sprints...")
    count = 0
    
    # Group sprints by project
    cursor.execute("SELECT s.id, s.project_id FROM sprints s")
    sprint_projects = {row[0]: row[1] for row in cursor.fetchall()}
    
    for issue_id in issue_ids:
        # Get project for this issue
        cursor.execute("SELECT project_id FROM issues WHERE id = %s", (issue_id,))
        result = cursor.fetchone()
        if not result:
            continue
        
        project_id = result[0]
        
        # Get sprints for this project
        project_sprints = [sid for sid, pid in sprint_projects.items() if pid == project_id]
        
        if project_sprints and random.random() < 0.8:  # 80% of issues in sprints
            sprint_id = random.choice(project_sprints)
            cursor.execute(
                """INSERT INTO issue_sprints (issue_id, sprint_id)
                   VALUES (%s, %s)""",
                (issue_id, sprint_id)
            )
            count += 1
    
    print(f"Created {count} issue-sprint links")

def seed_team_velocity(cursor, team_ids, project_ids):
    """Seed team velocity data"""
    print("Seeding team velocity...")
    count = 0
    
    for team_id in team_ids:
        # Get projects for this team
        cursor.execute("SELECT project_id FROM project_teams WHERE team_id = %s", (team_id,))
        team_projects = [row[0] for row in cursor.fetchall()]
        
        for project_id in team_projects:
            avg_hours = round(random.uniform(2.0, 6.0), 2)
            cursor.execute(
                """INSERT INTO team_velocity (team_id, project_id, avg_hours_per_point)
                   VALUES (%s, %s, %s)""",
                (team_id, project_id, avg_hours)
            )
            count += 1
    
    print(f"Created {count} team velocity records")

def seed_issue_types(cursor):
    """Seed issue types if not exists"""
    print("Seeding issue types...")
    
    issue_types = [
        "Story",
        "Task", 
        "Bug",
        "Epic",
        "Subtask"
    ]
    
    for name in issue_types:
        cursor.execute(
            """INSERT IGNORE INTO issue_types (name) VALUES (%s)""",
            (name,)
        )
    
    print(f"Seeded {len(issue_types)} issue types")

def seed_skills(cursor):
    """Seed skills if not exists"""
    print("Seeding skills...")
    
    skills = [
        "Python", "JavaScript", "React", "Node.js", "SQL", "Docker",
        "AWS", "Git", "FastAPI", "MySQL", "HTML/CSS", "TypeScript"
    ]
    
    for skill in skills:
        cursor.execute(
            """INSERT IGNORE INTO skills (name) VALUES (%s)""",
            (skill,)
        )
    
    print(f"Seeded {len(skills)} skills")

def main():
    """Main seeder function"""
    connection = create_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Clear existing data
        clear_existing_data(cursor)
        
        # Seed data in order
        seed_issue_types(cursor)  # Seed issue types first
        seed_skills(cursor)       # Seed skills
        
        # Create users first (main user + others)
        user_ids, user_credentials, main_user_id = seed_test_users(cursor)
        
        # Create organizations (all owned by main user)
        org_ids = seed_organizations(cursor, main_user_id)
        
        # Assign other users to organizations
        seed_organization_users(cursor, org_ids, user_ids, main_user_id)
        
        team_ids, team_org_map = seed_teams(cursor, org_ids)
        seed_user_team(cursor, team_ids, user_ids, team_org_map)
        
        workspace_ids, workspace_org_map = seed_workspaces(cursor, org_ids, user_ids, team_ids, team_org_map)
        project_ids = seed_projects(cursor, workspace_ids, user_ids)
        seed_project_teams(cursor, project_ids, team_ids, team_org_map)
        
        sprint_ids = seed_sprints(cursor, project_ids)
        issue_ids = seed_issues(cursor, project_ids, user_ids)
        seed_issue_assignments(cursor, issue_ids, user_ids)
        seed_issue_sprints(cursor, issue_ids, sprint_ids)
        
        seed_team_velocity(cursor, team_ids, project_ids)
        
        # Commit all changes
        connection.commit()
        print("\n✅ Database seeding completed successfully!")
        
        # Print test credentials
        print("\n" + "=" * 60)
        print("TEST USER CREDENTIALS:")
        print("=" * 60)
        
        # Show main user first
        main_cred = next(cred for cred in user_credentials if cred.get('role') == 'main_owner')
        print("🏢 MAIN ACCOUNT (Owns all organizations):")
        print(f"   Email: {main_cred['email']}")
        print(f"   Password: {main_cred['password']}")
        print()
        
        # Show other users
        other_creds = [cred for cred in user_credentials if cred.get('role') == 'member']
        print("👥 TEAM MEMBERS (Assigned to organizations):")
        for i, cred in enumerate(other_creds, 1):
            print(f"{i:2d}. Email: {cred['email']}")
            print(f"    Password: {cred['password']}")
        print("=" * 60)
        
        # Print summary
        print(f"\n📊 SEEDING SUMMARY:")
        print(f"   • Organizations: {len(org_ids)} (all owned by main user)")
        print(f"   • Users: {len(user_ids)} (1 main owner + {len(user_ids)-1} members)")
        print(f"   • Teams: {len(team_ids)}")
        print(f"   • Workspaces: {len(workspace_ids)}")
        print(f"   • Projects: {len(project_ids)}")
        print(f"   • Sprints: {len(sprint_ids)}")
        print(f"   • Issues: {len(issue_ids)}")
        print("\n💡 LOGIN TIP:")
        print("   Use the main account to see all organizations from a single perspective!")
        print("=" * 60)
        
    except Error as e:
        print(f"\n❌ Error during seeding: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
        print("Database connection closed")

if __name__ == "__main__":
    main()
