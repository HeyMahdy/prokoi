CREATE TABLE sprints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('planning', 'active', 'completed', 'cancelled') DEFAULT 'planning',
    goal TEXT,
    velocity_target INT DEFAULT NULL,
    INDEX idx_sprints_project_id (project_id),
    INDEX idx_sprints_id (id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- Link issues to sprints
CREATE TABLE issue_sprints (
    issue_id INT NOT NULL,
    sprint_id INT NOT NULL,
    INDEX idx_issue_sprints_issue_id (issue_id),
    INDEX idx_issue_sprints_sprint_id (sprint_id),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (issue_id, sprint_id),
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (sprint_id) REFERENCES sprints(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- 2. COMMENTS/ACTIVITY LOG (Essential for collaboration)
CREATE TABLE issue_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    user_id INT NULL,
    comment TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    INDEX idx_issue_comments_id (id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
    SET NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- 3. FILE ATTACHMENTS
CREATE TABLE attachments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NULL,
    project_id INT NULL,
    comment_id INT NULL,
    INDEX idx_attachments_issue_id (issue_id),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES issue_comments(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE
    SET NULL,
        CHECK (
            issue_id IS NOT NULL
            OR project_id IS NOT NULL
            OR comment_id IS NOT NULL
        )
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- 4. TIME TRACKING
CREATE TABLE time_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    user_id INT NOT NULL,
    hours_logged DECIMAL(5, 2) NOT NULL,
    INDEX idx_time_logs_issue_id (issue_id),
    INDEX idx_time_logs_user_id (user_id),
    INDEX idx_time_logs_id (id),
    description TEXT,
    log_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- 5. ISSUE HISTORY/AUDIT TRAIL
CREATE TABLE issue_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    user_id INT NULL,
    field_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    INDEX idx_issue_history_issue_id (issue_id),
    change_type ENUM(
        'created',
        'updated',
        'deleted',
        'assigned',
        'status_changed'
    ) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
    SET NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- 6. LABELS/TAGS
CREATE TABLE labels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    INDEX idx_labels_project_id (project_id),
    INDEX idx_labels_id (id),
    -- hex color
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_label (project_id, name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
CREATE TABLE issue_labels (
    issue_id INT NOT NULL,
    label_id INT NOT NULL,
    INDEX idx_issue_labels_issue_id (issue_id),
    INDEX idx_issue_labels_label_id (label_id),
    PRIMARY KEY (issue_id, label_id),
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (label_id) REFERENCES labels(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
-- =====================================
-- =====================================
-- REPORTING & ANALYTICS
-- =====================================
-- 8. BURNDOWN CHARTS DATA
-- 12. WEBHOOKS
CREATE TABLE webhooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    project_id INT NULL,
    url VARCHAR(500) NOT NULL,
    INDEX idx_webhooks_organization_id (organization_id),
    INDEX idx_webhooks_project_id (project_id),
    INDEX idx_webhooks_id (id),
    secret VARCHAR(255),
    events JSON NOT NULL,
    -- ["issue.created", "issue.updated", etc.]
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;