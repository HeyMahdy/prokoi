-- =======================
-- Issues & Workflow
-- =======================
-- Issue types table
CREATE TABLE issue_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Issues table
CREATE TABLE issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    type_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(50) DEFAULT 'medium',
    created_by INT NOT NULL,
    assigned_to INT NULL,
    parent_issue_id INT NULL,
    -- for subtasks
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES issue_types(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE
    SET NULL,
        FOREIGN KEY (parent_issue_id) REFERENCES issues(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Custom fields table
CREATE TABLE custom_fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    field_type VARCHAR(50) NOT NULL,
    project_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Issue custom values table
CREATE TABLE issue_custom_values (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    custom_field_id INT NOT NULL,
    value TEXT,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (custom_field_id) REFERENCES custom_fields(id) ON DELETE CASCADE,
    UNIQUE KEY unique_issue_field (issue_id, custom_field_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Issue watchers table
CREATE TABLE issue_watchers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_issue_watcher (issue_id, user_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Labels table
CREATE TABLE labels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    organization_id INT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_org_label (organization_id, name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Issue labels table
CREATE TABLE issue_labels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    label_id INT NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (label_id) REFERENCES labels(id) ON DELETE CASCADE,
    UNIQUE KEY unique_issue_label (issue_id, label_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Checklists table
CREATE TABLE checklists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Checklist items table
CREATE TABLE checklist_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checklist_id INT NOT NULL,
    description TEXT NOT NULL,
    is_done BOOLEAN DEFAULT FALSE,
    assigned_to INT NULL,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE
    SET NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Insert default issue types