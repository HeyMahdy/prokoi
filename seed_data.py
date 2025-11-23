#!/usr/bin/env python3
"""
Seed data script for Prokoi project management system.
This script populates the database with sample data for testing and development.
"""

import asyncio
import hashlib
from src.core.database import db
from src.core.config import settings

# Sample data
ORGANIZATIONS = [
    {"name": "TechCorp"},
    {"name": "InnovateX"},
    {"name": "Global Solutions"}
]

USERS = [
    {"name": "Alice Johnson", "email": "alice@techcorp.com", "password": "password123"},
    {"name": "Bob Smith", "email": "bob@techcorp.com", "password": "password123"},
    {"name": "Carol Williams", "email": "carol@innovatex.com", "password": "password123"},
    {"name": "David Brown", "email": "david@innovatex.com", "password": "password123"},
    {"name": "Eve Davis", "email": "eve@globalsolutions.com", "password": "password123"},
    {"name": "Frank Miller", "email": "frank@globalsolutions.com", "password": "password123"}
]

ROLES = [
    {"name": "admin"},
    {"name": "project_manager"},
    {"name": "developer"},
    {"name": "designer"},
    {"name": "tester"}
]

SKILLS = [
    {"name": "Python"},
    {"name": "JavaScript"},
    {"name": "React"},
    {"name": "Node.js"},
    {"name": "SQL"},
    {"name": "UI/UX Design"},
    {"name": "Testing"},
    {"name": "DevOps"}
]

ISSUE_TYPES = [
    {"name": "Bug"},
    {"name": "Feature"},
    {"name": "Task"},
    {"name": "Story"},
    {"name": "Epic"}
]

async def hash_password(password: str) -> str:
    """Hash password using SHA-256 (in production, use proper password hashing)"""
    return hashlib.sha256(password.encode()).hexdigest()

async def clear_existing_data():
    """Clear existing data from all tables to prevent duplicates"""
    print("Clearing existing data...")
    tables = [
        'issue_labels', 'labels', 'issue_history', 'issue_comments', 
        'issue_sprints', 'sprints', 'team_velocity', 'issue_assignments', 
        'user_workload', 'user_capacity', 'issue_skill_requirements', 
        'user_skills', 'skills', 'checklist_items', 'checklists', 
        'issues', 'issue_types', 'project_users', 'project_teams', 
        'team_workspaces', 'projects', 'workspaces', 'user_team', 
        'teams', 'user_role', 'role_permissions', 'roles', 
        'permissions', 'organization_outgoing_requests', 
        'organization_invitations', 'organization_users', 'users', 'organizations'
    ]
    
    # Disable foreign key checks temporarily
    await db.execute_query("SET FOREIGN_KEY_CHECKS = 0")
    
    for table in tables:
        try:
            await db.execute_query(f"DELETE FROM {table}")
            print(f"  Cleared {table}")
        except Exception as e:
            print(f"  Warning: Could not clear {table} - {e}")
    
    # Re-enable foreign key checks
    await db.execute_query("SET FOREIGN_KEY_CHECKS = 1")
    print("Finished clearing existing data.")

async def seed_organizations():
    """Seed organizations table"""
    print("Seeding organizations...")
    org_ids = []
    for org in ORGANIZATIONS:
        query = "INSERT INTO organizations (name) VALUES (%s)"
        org_id = await db.execute_insert(query, (org["name"],))
        org_ids.append(org_id)
        print(f"  Created organization: {org['name']} (ID: {org_id})")
    return org_ids

async def seed_users(org_ids):
    """Seed users table and connect them to organizations"""
    print("Seeding users...")
    user_ids = []
    
    # Create users
    for i, user in enumerate(USERS):
        hashed_password = await hash_password(user["password"])
        query = "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)"
        user_id = await db.execute_insert(query, (user["name"], user["email"], hashed_password))
        user_ids.append(user_id)
        print(f"  Created user: {user['name']} (ID: {user_id})")
        
        # Connect user to organization (round-robin assignment)
        org_id = org_ids[i % len(org_ids)]
        query = "INSERT INTO organization_users (organization_id, user_id) VALUES (%s, %s)"
        await db.execute_insert(query, (org_id, user_id))
        print(f"    Assigned to organization ID: {org_id}")
    
    return user_ids

async def seed_roles(org_ids):
    """Seed roles table"""
    print("Seeding roles...")
    role_ids = []
    
    for org_id in org_ids:
        for role in ROLES:
            unique_role_name = f"{role['name']}_{org_id}"
            query = "INSERT INTO roles (name, organization_id) VALUES (%s, %s)"
            role_id = await db.execute_insert(query, (unique_role_name, org_id))
            role_ids.append(role_id)
            print(f"  Created role: {unique_role_name} (ID: {role_id}) for org {org_id}")
    
    return role_ids

async def seed_skills():
    """Seed skills table"""
    print("Seeding skills...")
    skill_ids = []
    
    for skill in SKILLS:
        query = "INSERT INTO skills (name) VALUES (%s)"
        skill_id = await db.execute_insert(query, (skill["name"],))
        skill_ids.append(skill_id)
        print(f"  Created skill: {skill['name']} (ID: {skill_id})")
    
    return skill_ids

async def seed_issue_types():
    """Seed issue_types table"""
    print("Seeding issue types...")
    type_ids = []
    
    for issue_type in ISSUE_TYPES:
        query = "INSERT INTO issue_types (name) VALUES (%s)"
        type_id = await db.execute_insert(query, (issue_type["name"],))
        type_ids.append(type_id)
        print(f"  Created issue type: {issue_type['name']} (ID: {type_id})")
    
    return type_ids

async def seed_workspaces(org_ids, user_ids):
    """Seed workspaces table"""
    print("Seeding workspaces...")
    workspace_ids = []
    
    workspaces = [
        {"name": "Web App Development", "org_index": 0, "user_index": 0},
        {"name": "Mobile App Project", "org_index": 0, "user_index": 1},
        {"name": "Marketing Campaign", "org_index": 1, "user_index": 2},
        {"name": "Internal Tools", "org_index": 1, "user_index": 3},
        {"name": "Research Initiative", "org_index": 2, "user_index": 4},
        {"name": "Client Portal", "org_index": 2, "user_index": 5}
    ]
    
    for ws in workspaces:
        org_id = org_ids[ws["org_index"]]
        user_id = user_ids[ws["user_index"]]
        query = "INSERT INTO workspaces (name, user_id, organization_id) VALUES (%s, %s, %s)"
        ws_id = await db.execute_insert(query, (ws["name"], user_id, org_id))
        workspace_ids.append(ws_id)
        print(f"  Created workspace: {ws['name']} (ID: {ws_id})")
    
    return workspace_ids

async def seed_teams(org_ids):
    """Seed teams table"""
    print("Seeding teams...")
    team_ids = []
    
    teams = [
        {"name": "Frontend Team", "org_index": 0},
        {"name": "Backend Team", "org_index": 0},
        {"name": "QA Team", "org_index": 0},
        {"name": "Design Team", "org_index": 1},
        {"name": "DevOps Team", "org_index": 1},
        {"name": "Analytics Team", "org_index": 2}
    ]
    
    for team in teams:
        org_id = org_ids[team["org_index"]]
        query = "INSERT INTO teams (name, organization_id) VALUES (%s, %s)"
        team_id = await db.execute_insert(query, (team["name"], org_id))
        team_ids.append(team_id)
        print(f"  Created team: {team['name']} (ID: {team_id})")
    
    return team_ids

async def seed_projects(workspace_ids):
    """Seed projects table"""
    print("Seeding projects...")
    project_ids = []
    
    projects = [
        {"name": "User Dashboard", "ws_index": 0, "status": "active"},
        {"name": "API Development", "ws_index": 0, "status": "active"},
        {"name": "Authentication System", "ws_index": 1, "status": "pending"},
        {"name": "Mobile UI", "ws_index": 1, "status": "active"},
        {"name": "Campaign Landing Page", "ws_index": 2, "status": "completed"},
        {"name": "SEO Optimization", "ws_index": 2, "status": "active"}
    ]
    
    for proj in projects:
        ws_id = workspace_ids[proj["ws_index"]]
        query = "INSERT INTO projects (name, workspace_id, status) VALUES (%s, %s, %s)"
        proj_id = await db.execute_insert(query, (proj["name"], ws_id, proj["status"]))
        project_ids.append(proj_id)
        print(f"  Created project: {proj['name']} (ID: {proj_id})")
    
    return project_ids

async def seed_issues(project_ids, user_ids, type_ids):
    """Seed issues table"""
    print("Seeding issues...")
    issue_ids = []
    
    issues = [
        {"title": "Fix login button alignment", "project_index": 0, "type_index": 0, "user_index": 0, "status": "open", "priority": "high"},
        {"title": "Implement user profile page", "project_index": 0, "type_index": 3, "user_index": 1, "status": "in_progress", "priority": "medium"},
        {"title": "Database connection timeout", "project_index": 1, "type_index": 0, "user_index": 1, "status": "open", "priority": "critical"},
        {"title": "Add password reset functionality", "project_index": 2, "type_index": 3, "user_index": 0, "status": "todo", "priority": "high"},
        {"title": "Optimize API response times", "project_index": 1, "type_index": 2, "user_index": 1, "status": "in_progress", "priority": "medium"}
    ]
    
    for issue in issues:
        project_id = project_ids[issue["project_index"]]
        type_id = type_ids[issue["type_index"]]
        user_id = user_ids[issue["user_index"]] if issue["user_index"] < len(user_ids) else None
        
        query = """
            INSERT INTO issues (project_id, type_id, title, status, priority, created_by) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        issue_id = await db.execute_insert(query, (
            project_id, type_id, issue["title"], 
            issue["status"], issue["priority"], user_id
        ))
        issue_ids.append(issue_id)
        print(f"  Created issue: {issue['title']} (ID: {issue_id})")
    
    return issue_ids

async def seed_user_roles(user_ids, role_ids):
    """Seed user_role table"""
    print("Seeding user roles...")
    
    # Assign roles to users (simple round-robin)
    for i, user_id in enumerate(user_ids):
        role_id = role_ids[i % len(role_ids)]
        query = "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)"
        await db.execute_insert(query, (user_id, role_id))
        print(f"  Assigned role ID {role_id} to user ID {user_id}")

async def seed_user_skills(user_ids, skill_ids):
    """Seed user_skills table"""
    print("Seeding user skills...")
    
    # Assign skills to users
    skill_assignments = [
        (0, 0, "expert"),  # Alice - Python - expert
        (0, 1, "intermediate"),  # Alice - JavaScript - intermediate
        (1, 0, "advanced"),  # Bob - Python - advanced
        (1, 3, "intermediate"),  # Bob - Node.js - intermediate
        (2, 2, "expert"),  # Carol - React - expert
        (2, 1, "advanced"),  # Carol - JavaScript - advanced
        (3, 6, "expert"),  # David - Testing - expert
        (4, 5, "expert"),  # Eve - UI/UX Design - expert
        (5, 7, "advanced")  # Frank - DevOps - advanced
    ]
    
    for user_idx, skill_idx, proficiency in skill_assignments:
        if user_idx < len(user_ids) and skill_idx < len(skill_ids):
            user_id = user_ids[user_idx]
            skill_id = skill_ids[skill_idx]
            query = "INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES (%s, %s, %s)"
            await db.execute_insert(query, (user_id, skill_id, proficiency))
            print(f"  Assigned skill ID {skill_id} ({proficiency}) to user ID {user_id}")

async def seed_issue_skill_requirements(issue_ids, skill_ids):
    """Seed issue_skill_requirements table"""
    print("Seeding issue skill requirements...")
    
    # Assign skill requirements to issues
    requirements = [
        (0, 0, "intermediate"),  # Issue 0 requires Python (intermediate)
        (0, 1, "beginner"),  # Issue 0 requires JavaScript (beginner)
        (1, 2, "advanced"),  # Issue 1 requires React (advanced)
        (2, 0, "expert"),  # Issue 2 requires Python (expert)
        (3, 3, "intermediate"),  # Issue 3 requires Node.js (intermediate)
        (4, 4, "advanced")  # Issue 4 requires SQL (advanced)
    ]
    
    for issue_idx, skill_idx, level in requirements:
        if issue_idx < len(issue_ids) and skill_idx < len(skill_ids):
            issue_id = issue_ids[issue_idx]
            skill_id = skill_ids[skill_idx]
            query = "INSERT INTO issue_skill_requirements (issue_id, skill_id, required_level) VALUES (%s, %s, %s)"
            await db.execute_insert(query, (issue_id, skill_id, level))
            print(f"  Issue {issue_id} requires skill {skill_id} ({level})")

async def seed_user_teams(user_ids, team_ids):
    """Seed user_team table"""
    print("Seeding user teams...")
    
    # Assign users to teams
    assignments = [
        (0, 0),  # Alice -> Frontend Team
        (1, 1),  # Bob -> Backend Team
        (2, 0),  # Carol -> Frontend Team
        (3, 2),  # David -> QA Team
        (4, 3),  # Eve -> Design Team
        (5, 4)   # Frank -> DevOps Team
    ]
    
    for user_idx, team_idx in assignments:
        if user_idx < len(user_ids) and team_idx < len(team_ids):
            user_id = user_ids[user_idx]
            team_id = team_ids[team_idx]
            query = "INSERT INTO user_team (user_id, team_id) VALUES (%s, %s)"
            await db.execute_insert(query, (user_id, team_id))
            print(f"  Assigned user {user_id} to team {team_id}")

async def main():
    """Main seeding function"""
    print("Starting database seeding...")
    
    # Initialize database connection pool
    await db.create_pool()
    
    try:
        # Clear existing data first to prevent duplicates
        await clear_existing_data()
        
        # Seed data in proper order (respecting foreign key constraints)
        org_ids = await seed_organizations()
        user_ids = await seed_users(org_ids)
        role_ids = await seed_roles(org_ids)
        skill_ids = await seed_skills()
        type_ids = await seed_issue_types()
        workspace_ids = await seed_workspaces(org_ids, user_ids)
        team_ids = await seed_teams(org_ids)
        project_ids = await seed_projects(workspace_ids)
        issue_ids = await seed_issues(project_ids, user_ids, type_ids)
        
        # Seed relationship tables
        await seed_user_roles(user_ids, role_ids)
        await seed_user_skills(user_ids, skill_ids)
        await seed_issue_skill_requirements(issue_ids, skill_ids)
        await seed_user_teams(user_ids, team_ids)
        
        print("\n✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        raise
    finally:
        # Close database connections
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())