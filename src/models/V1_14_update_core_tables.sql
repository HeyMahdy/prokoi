-- ============================================================
-- UPDATE CORE TABLES TO USE UUIDs
-- ============================================================
-- Update organizations table
ALTER TABLE organizations
MODIFY COLUMN id VARCHAR(36) NOT NULL;
-- Update teams table
ALTER TABLE teams
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN organization_id VARCHAR(36) NOT NULL;
-- Update users table (already updated in previous migration)
-- Update workspaces table
ALTER TABLE workspaces
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN organization_id VARCHAR(36) NOT NULL;
-- Update projects table
ALTER TABLE projects
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN workspace_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN created_by VARCHAR(36);
-- Update sprints table
ALTER TABLE sprints
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN project_id VARCHAR(36) NOT NULL;
-- Update labels table
ALTER TABLE labels
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN project_id VARCHAR(36) NOT NULL;
-- Update join tables
ALTER TABLE organization_users
MODIFY COLUMN organization_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36) NOT NULL;
ALTER TABLE user_team
MODIFY COLUMN team_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36);
ALTER TABLE project_teams
MODIFY COLUMN project_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN team_id VARCHAR(36);
ALTER TABLE project_users
MODIFY COLUMN project_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36);
ALTER TABLE team_workspaces
MODIFY COLUMN team_id VARCHAR(36),
    MODIFY COLUMN workspace_id VARCHAR(36) NOT NULL;
-- Update foreign key constraints for core tables
ALTER TABLE teams DROP FOREIGN KEY teams_ibfk_1;
ALTER TABLE teams
ADD CONSTRAINT fk_teams_organization_id FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE;
ALTER TABLE workspaces DROP FOREIGN KEY workspaces_ibfk_1,
    DROP FOREIGN KEY workspaces_ibfk_2;
ALTER TABLE workspaces
ADD CONSTRAINT fk_workspaces_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_workspaces_organization_id FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE;
ALTER TABLE projects DROP FOREIGN KEY projects_ibfk_1,
    DROP FOREIGN KEY projects_ibfk_2;
ALTER TABLE projects
ADD CONSTRAINT fk_projects_workspace_id FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_projects_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE
SET NULL;
ALTER TABLE sprints DROP FOREIGN KEY sprints_ibfk_1;
ALTER TABLE sprints
ADD CONSTRAINT fk_sprints_project_id FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;
ALTER TABLE labels DROP FOREIGN KEY labels_ibfk_1;
ALTER TABLE labels
ADD CONSTRAINT fk_labels_project_id FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;
ALTER TABLE organization_users DROP FOREIGN KEY organization_users_ibfk_1,
    DROP FOREIGN KEY organization_users_ibfk_2;
ALTER TABLE organization_users
ADD CONSTRAINT fk_organization_users_organization_id FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_organization_users_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_team DROP FOREIGN KEY user_team_ibfk_1,
    DROP FOREIGN KEY user_team_ibfk_2;
ALTER TABLE user_team
ADD CONSTRAINT fk_user_team_team_id FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_user_team_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
SET NULL;
ALTER TABLE project_teams DROP FOREIGN KEY project_teams_ibfk_1,
    DROP FOREIGN KEY project_teams_ibfk_2;
ALTER TABLE project_teams
ADD CONSTRAINT fk_project_teams_project_id FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_project_teams_team_id FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE
SET NULL;
ALTER TABLE project_users DROP FOREIGN KEY project_users_ibfk_1,
    DROP FOREIGN KEY project_users_ibfk_2;
ALTER TABLE project_users
ADD CONSTRAINT fk_project_users_project_id FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_project_users_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
SET NULL;
ALTER TABLE team_workspaces DROP FOREIGN KEY team_workspaces_ibfk_1,
    DROP FOREIGN KEY team_workspaces_ibfk_2;
ALTER TABLE team_workspaces
ADD CONSTRAINT fk_team_workspaces_team_id FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE
SET NULL,
    ADD CONSTRAINT fk_team_workspaces_workspace_id FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE;