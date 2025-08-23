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
    type_id INT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(50) DEFAULT 'medium',
    created_by INT NULL,
    assigned_to INT NULL,
    parent_issue_id INT NULL,
    /* for subtasks */
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES issue_types(id) ON DELETE
    SET NULL,
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE
    SET NULL,
        FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE
    SET NULL,
        FOREIGN KEY (parent_issue_id) REFERENCES issues(id) ON DELETE CASCADE
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
INSERT INTO issue_types (name, description)
VALUES ('Story', 'User story or feature request'),
    ('Task', 'General task or work item'),
    ('Bug', 'Software defect or issue'),
    ('Epic', 'Large body of work'),
    ('Subtask', 'Smaller part of a larger issue');