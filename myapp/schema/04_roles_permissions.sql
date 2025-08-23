-- =======================
-- Roles & Permissions
-- =======================
-- Roles table
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    scope ENUM('global', 'project') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_org_role (organization_id, scope, name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Permissions table
CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Role permissions table
CREATE TABLE role_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_permission (role_id, permission_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- User roles table
CREATE TABLE user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_role (user_id, role_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Insert default permissions
INSERT INTO permissions (name, description)
VALUES ('project:create', 'Create new projects'),
    ('project:read', 'View project information'),
    ('project:update', 'Modify project settings'),
    ('project:delete', 'Delete projects'),
    ('issue:create', 'Create new issues'),
    ('issue:read', 'View issue information'),
    ('issue:update', 'Modify issues'),
    ('issue:delete', 'Delete issues'),
    ('user:manage', 'Manage users and permissions');
-- Insert default roles
INSERT INTO roles (organization_id, name, scope)
VALUES (1, 'Super Admin', 'global'),
    (1, 'Project Admin', 'project'),
    (1, 'Developer', 'project'),
    (1, 'Viewer', 'project');