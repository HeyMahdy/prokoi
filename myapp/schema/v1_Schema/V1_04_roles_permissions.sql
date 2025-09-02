-- =======================
-- Roles & Permissions
-- =======================
-- Roles table
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
-- Role permissions table
CREATE TABLE role_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_permission (role_id, permission_id)
);
-- User roles table
CREATE TABLE user_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    organization_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_org_role (user_id, organization_id, role_id)
);
INSERT INTO permissions (name)
VALUES ('all'),
    -- super_admin full access
    ('view_project'),
    ('edit_project'),
    ('delete_project'),
    ('create_task'),
    ('view_task'),
    ('edit_task'),
    ('delete_task'),
    ('assign_task'),
    ('manage_users'),
    ('create_issue'),
    ('view_issue'),
    ('edit_issue'),
    ('delete_issue'),
    ('assign_issue'),
    ('create_checklist'),
    ('view_checklist'),
    ('edit_checklist'),
    ('delete_checklist'),
    ('assign_checklist_item'),
    ('complete_checklist_item');
INSERT INTO roles (name)
VALUES ('super_admin'),
    -- has all permissions
    ('admin'),
    -- manages projects and users
    ('project_manager'),
    ('developer'),
    ('viewer');
-- read-only access
-- Insert default roles