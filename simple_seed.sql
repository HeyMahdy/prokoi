-- Simple seed data for Prokoi - creates organizations, teams, and team members only
-- Clear existing data and insert sample data for testing
-- Clear existing data (in reverse order of foreign key dependencies)
SET FOREIGN_KEY_CHECKS = 0;
DELETE FROM user_team;
DELETE FROM teams;
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
-- Team members (user_team)
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
SELECT '✅ Simple database seeding completed successfully!' AS result;