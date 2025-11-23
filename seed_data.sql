-- Seed data for Prokoi project management system
-- This script populates the database with sample data for testing and development
-- Clear existing data (in reverse order of foreign key dependencies)
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM issue_labels;
DELETE FROM labels;
DELETE FROM issue_history;
DELETE FROM issue_comments;
DELETE FROM issue_sprints;
DELETE FROM sprints;
DELETE FROM team_velocity;
DELETE FROM issue_assignments;
DELETE FROM user_workload;
DELETE FROM user_capacity;
DELETE FROM issue_skill_requirements;
DELETE FROM user_skills;
DELETE FROM skills;
DELETE FROM checklist_items;
DELETE FROM checklists;
DELETE FROM issues;
DELETE FROM issue_types;
DELETE FROM project_users;
DELETE FROM project_teams;
DELETE FROM team_workspaces;
DELETE FROM projects;
DELETE FROM workspaces;
DELETE FROM user_team;
DELETE FROM teams;
DELETE FROM user_role;
DELETE FROM role_permissions;
DELETE FROM roles;
DELETE FROM permissions;
DELETE FROM organization_outgoing_requests;
DELETE FROM organization_invitations;
DELETE FROM organization_users;
DELETE FROM users;
DELETE FROM organizations;
SET FOREIGN_KEY_CHECKS = 1;
-- Organizations
INSERT INTO organizations (name)
VALUES ('TechCorp'),
    ('InnovateX'),
    ('Global Solutions');
-- Users (password is 'password123' hashed with SHA-256)
INSERT INTO users (name, email, password_hash)
VALUES (
        'Alice Johnson',
        'alice@techcorp.com',
        'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
    ),
    (
        'Bob Smith',
        'bob@techcorp.com',
        'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
    ),
    (
        'Carol Williams',
        'carol@innovatex.com',
        'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
    ),
    (
        'David Brown',
        'david@innovatex.com',
        'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
    ),
    (
        'Eve Davis',
        'eve@globalsolutions.com',
        'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
    ),
    (
        'Frank Miller',
        'frank@globalsolutions.com',
        'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
    );
-- Organization users (link users to organizations)
INSERT INTO organization_users (organization_id, user_id)
VALUES (1, 1),
    (1, 2),
    -- TechCorp users
    (2, 3),
    (2, 4),
    -- InnovateX users
    (3, 5),
    (3, 6);
-- Global Solutions users
-- Teams
INSERT INTO teams (organization_id, name)
VALUES (1, 'Frontend Team'),
    (1, 'Backend Team'),
    (1, 'QA Team'),
    (2, 'Design Team'),
    (2, 'DevOps Team'),
    (3, 'Analytics Team');
-- Workspaces
INSERT INTO workspaces (name, user_id, organization_id)
VALUES ('Web App Development', 1, 1),
    ('Mobile App Project', 2, 1),
    ('Marketing Campaign', 3, 2),
    ('Internal Tools', 4, 2),
    ('Research Initiative', 5, 3),
    ('Client Portal', 6, 3);
-- Projects
INSERT INTO projects (name, workspace_id, status)
VALUES ('User Dashboard', 1, 'active'),
    ('API Development', 1, 'active'),
    ('Authentication System', 2, 'pending'),
    ('Mobile UI', 2, 'active'),
    ('Campaign Landing Page', 3, 'completed'),
    ('SEO Optimization', 3, 'active');
-- Issue types
INSERT INTO issue_types (name)
VALUES ('Bug'),
    ('Feature'),
    ('Task'),
    ('Story'),
    ('Epic');
-- Skills
INSERT INTO skills (name)
VALUES ('Python'),
    ('JavaScript'),
    ('React'),
    ('Node.js'),
    ('SQL'),
    ('UI/UX Design'),
    ('Testing'),
    ('DevOps');
-- Issues
INSERT INTO issues (
        project_id,
        type_id,
        title,
        status,
        priority,
        created_by
    )
VALUES (
        1,
        1,
        'Fix login button alignment',
        'open',
        'high',
        1
    ),
    (
        1,
        4,
        'Implement user profile page',
        'in_progress',
        'medium',
        2
    ),
    (
        2,
        1,
        'Database connection timeout',
        'open',
        'critical',
        2
    ),
    (
        3,
        4,
        'Add password reset functionality',
        'todo',
        'high',
        1
    ),
    (
        2,
        3,
        'Optimize API response times',
        'in_progress',
        'medium',
        2
    );
-- Labels
INSERT INTO labels (project_id, name, description)
VALUES (1, 'frontend', 'Frontend related issues'),
    (1, 'bug', 'Bug fixes'),
    (2, 'backend', 'Backend related issues'),
    (2, 'performance', 'Performance improvements'),
    (3, 'security', 'Security related issues');
-- Issue labels
INSERT INTO issue_labels (issue_id, label_id)
VALUES (1, 1),
    (1, 2),
    -- Login button issue has frontend and bug labels
    (2, 1),
    -- Profile page has frontend label
    (3, 3),
    (3, 4),
    -- Database issue has backend and performance labels
    (4, 5);
-- Password reset has security label
-- Sprints
INSERT INTO sprints (
        project_id,
        name,
        description,
        start_date,
        end_date,
        status
    )
VALUES (
        1,
        'Sprint 1',
        'First development sprint',
        '2025-01-01',
        '2025-01-14',
        'completed'
    ),
    (
        1,
        'Sprint 2',
        'Second development sprint',
        '2025-01-15',
        '2025-01-28',
        'active'
    ),
    (
        2,
        'Sprint 1',
        'API development sprint',
        '2025-01-01',
        '2025-01-14',
        'active'
    );
-- Issue sprints
INSERT INTO issue_sprints (issue_id, sprint_id)
VALUES (1, 1),
    (2, 2),
    (3, 2),
    (4, 2);
-- User roles (organization-specific roles)
INSERT INTO roles (name, organization_id)
VALUES ('admin_1', 1),
    ('project_manager_1', 1),
    ('developer_1', 1),
    ('designer_1', 1),
    ('tester_1', 1),
    ('admin_2', 2),
    ('project_manager_2', 2),
    ('developer_2', 2),
    ('designer_2', 2),
    ('tester_2', 2),
    ('admin_3', 3),
    ('project_manager_3', 3),
    ('developer_3', 3),
    ('designer_3', 3),
    ('tester_3', 3);
-- Permissions (pre-populated in V1_04_roles_permissions.sql)
-- Already seeded in the schema file
-- User role assignments
INSERT INTO user_role (user_id, role_id)
VALUES (1, 1),
    -- Alice is admin in TechCorp
    (2, 3),
    -- Bob is developer in TechCorp
    (3, 7),
    -- Carol is project manager in InnovateX
    (4, 8),
    -- David is developer in InnovateX
    (5, 11),
    -- Eve is admin in Global Solutions
    (6, 13);
-- Frank is developer in Global Solutions
-- User skills
INSERT INTO user_skills (user_id, skill_id, proficiency_level)
VALUES (1, 1, 'expert'),
    -- Alice - Python - expert
    (1, 2, 'intermediate'),
    -- Alice - JavaScript - intermediate
    (2, 1, 'advanced'),
    -- Bob - Python - advanced
    (2, 4, 'intermediate'),
    -- Bob - Node.js - intermediate
    (3, 3, 'expert'),
    -- Carol - React - expert
    (3, 2, 'advanced'),
    -- Carol - JavaScript - advanced
    (4, 7, 'expert'),
    -- David - Testing - expert
    (5, 6, 'expert'),
    -- Eve - UI/UX Design - expert
    (6, 8, 'advanced');
-- Frank - DevOps - advanced
-- Issue skill requirements
INSERT INTO issue_skill_requirements (issue_id, skill_id, required_level)
VALUES (1, 2, 'beginner'),
    -- Login button requires JavaScript (beginner)
    (2, 3, 'advanced'),
    -- Profile page requires React (advanced)
    (3, 1, 'expert'),
    -- Database issue requires Python (expert)
    (4, 4, 'intermediate'),
    -- Password reset requires Node.js (intermediate)
    (5, 5, 'advanced');
-- API optimization requires SQL (advanced)
-- User team assignments
INSERT INTO user_team (user_id, team_id)
VALUES (1, 1),
    -- Alice -> Frontend Team
    (2, 2),
    -- Bob -> Backend Team
    (3, 1),
    -- Carol -> Frontend Team
    (4, 3),
    -- David -> QA Team
    (5, 4),
    -- Eve -> Design Team
    (6, 5);
-- Frank -> DevOps Team
-- Team velocity
INSERT INTO team_velocity (team_id, project_id, avg_hours_per_point)
VALUES (1, 1, 8.5),
    -- Frontend Team
    (2, 1, 10.2),
    -- Backend Team
    (2, 2, 9.7);
-- Backend Team on API project
-- Comments
INSERT INTO issue_comments (issue_id, user_id, comment, is_internal)
VALUES (
        1,
        2,
        'I can take care of this alignment issue.',
        FALSE
    ),
    (
        3,
        1,
        'This seems to be related to the recent database upgrade.',
        TRUE
    ),
    (
        2,
        3,
        'Will start working on the profile page design.',
        FALSE
    );
-- Checklists
INSERT INTO checklists (issue_id, name)
VALUES (2, 'Profile Page Implementation'),
    (4, 'Password Reset Features');
-- Checklist items
INSERT INTO checklist_items (checklist_id, description, assigned_to)
VALUES (1, 'Create user profile component', 1),
    (1, 'Implement edit functionality', 1),
    (1, 'Add profile picture upload', 3),
    (2, 'Create reset password form', 2),
    (2, 'Implement email verification', 2);
SELECT '✅ Database seeding completed successfully!' AS result;