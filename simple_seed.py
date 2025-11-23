#!/usr/bin/env python3
"""
Simple seed data script for Prokoi - creates organizations, teams, and team members only.
"""

import asyncio
import hashlib
from src.core.database import db

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

TEAMS = [
    {"name": "Frontend Team"},
    {"name": "Backend Team"},
    {"name": "QA Team"},
    {"name": "Design Team"},
    {"name": "DevOps Team"},
    {"name": "Analytics Team"}
]

async def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

async def clear_existing_data():
    """Clear existing data from the tables we'll be seeding"""
    print("Clearing existing data...")
    tables = ['user_team', 'teams', 'organization_users', 'users', 'organizations']
    
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

async def seed_teams(org_ids):
    """Seed teams table"""
    print("Seeding teams...")
    team_ids = []
    
    for i, team in enumerate(TEAMS):
        # Assign teams to organizations (round-robin)
        org_id = org_ids[i % len(org_ids)]
        query = "INSERT INTO teams (name, organization_id) VALUES (%s, %s)"
        team_id = await db.execute_insert(query, (team["name"], org_id))
        team_ids.append(team_id)
        print(f"  Created team: {team['name']} (ID: {team_id}) in org {org_id}")
    
    return team_ids

async def seed_team_members(user_ids, team_ids):
    """Seed user_team table (team memberships)"""
    print("Seeding team members...")
    
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
            try:
                await db.execute_insert(query, (user_id, team_id))
                print(f"  Assigned user {user_id} to team {team_id}")
            except Exception as e:
                print(f"  Warning: Could not assign user {user_id} to team {team_id} - {e}")

async def main():
    """Main seeding function"""
    print("Starting simple database seeding (orgs, teams, members)...")
    
    # Initialize database connection pool
    await db.create_pool()
    
    try:
        # Clear existing data first
        await clear_existing_data()
        
        # Seed data in proper order (respecting foreign key constraints)
        org_ids = await seed_organizations()
        user_ids = await seed_users(org_ids)
        team_ids = await seed_teams(org_ids)
        await seed_team_members(user_ids, team_ids)
        
        print("\n✅ Simple database seeding completed successfully!")
        print(f"  Organizations: {len(org_ids)}")
        print(f"  Users: {len(user_ids)}")
        print(f"  Teams: {len(team_ids)}")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        raise
    finally:
        # Close database connections
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())