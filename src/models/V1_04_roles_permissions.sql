CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    organization_id INT NOT NULL,
    UNIQUE KEY uniq_roles_org_name (organization_id, name),
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
);
CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    INDEX idx_permissions_name (name)
);
-- Role permissions table
 CREATE TABLE role_permissions(
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    INDEX idx_role_permissions_role_id (role_id),
    INDEX idx_role_permissions_permission_id (permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_permission (role_id, permission_id)
);
-- User roles table
CREATE TABLE user_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    INDEX idx_user_role_user_id (user_id),
    INDEX idx_user_role_role_id (role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_org_role (user_id, role_id)
);
INSERT INTO permissions (name)
VALUES ('all'),
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
    ('complete_checklist_item'),
    ('view_workspace'),
    ('edit_workspace'),
    ('create_workspace'),
    ('delete_workspace');
INSERT INTO roles (name)

