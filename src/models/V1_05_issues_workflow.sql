CREATE TABLE issue_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    INDEX idx_issue_types_name (name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Issues table
CREATE TABLE issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    type_id INT NULL,
    title VARCHAR(255) NOT NULL,
    story_points INT DEFAULT NULL;
description TEXT,
status VARCHAR(50) DEFAULT 'open',
priority VARCHAR(50) DEFAULT 'medium',
created_by INT NULL,
parent_issue_id INT NULL,
INDEX idx_issues_project_id (project_id),
INDEX idx_issues_type_id (type_id),
INDEX idx_issues_created_by (created_by),
INDEX idx_issues_id (id),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
FOREIGN KEY (type_id) REFERENCES issue_types(id) ON DELETE
SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE
SET NULL,
    FOREIGN KEY (parent_issue_id) REFERENCES issues(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Checklists table
CREATE TABLE checklists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    INDEX idx_checklists_issue_id (issue_id),
    INDEX idx_checklists_id (id),
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Checklist items table
CREATE TABLE checklist_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    checklist_id INT NOT NULL,
    description TEXT NOT NULL,
    assigned_to INT NULL,
    INDEX idx_checklist_items_checklist_id (checklist_id),
    INDEX idx_checklist_items_assigned_to (assigned_to),
    INDEX idx_checklist_items_id (id),
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
CREATE TABLE issue_watchers (
    issue_id INT NOT NULL,
    user_id INT NOT NULL,
    INDEX idx_issue_watchers_issue_id (issue_id, user_id),
    PRIMARY KEY (issue_id, user_id),
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;