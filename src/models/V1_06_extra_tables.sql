CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    INDEX idx_skills_name (name),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE user_skills (
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'advanced', 'expert') DEFAULT 'intermediate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_skills_user_id (user_id),
    INDEX idx_user_skills_skill_id (skill_id),
    PRIMARY KEY (user_id, skill_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);
CREATE TABLE issue_skill_requirements (
    issue_id INT NOT NULL,
    skill_id INT NOT NULL,
    required_level ENUM('beginner', 'intermediate', 'advanced', 'expert') DEFAULT 'intermediate',
    INDEX idx_issue_skill_requirements_issue_id (issue_id),
    INDEX idx_issue_skill_requirements_skill_id (skill_id),
    PRIMARY KEY (issue_id, skill_id),
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);
CREATE TABLE user_capacity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    organization_id INT NOT NULL,
    weekly_hours DECIMAL(4, 2) DEFAULT 40.0,
    INDEX idx_user_capacity_user_id (user_id),
    INDEX idx_user_capacity_organization_id (organization_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_org_capacity (user_id, organization_id)
);
-- Workload tracking table
CREATE TABLE user_workload (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_assignments_id INT NULL,
    -- NULL for general project work
    hours_spent DECIMAL(5, 2) DEFAULT 0.0,
    INDEX idx_user_workload_issue_assignments_id (issue_assignments_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_assignments_id) REFERENCES issue_assignments(id) ON DELETE
    SET NULL
);
CREATE TABLE issue_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    assigned_to INT NULL,
    assigned_by INT NULL,
    INDEX idx_issue_assignments_issue_id (issue_id),
    INDEX idx_issue_assignments_assigned_to (assigned_to),
    INDEX idx_issue_assignments_assigned_by (assigned_by),
    -- NULL for auto-assignment
    -- explanation for auto-assignment
    -- how well the assignment fits (0-1)
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE
    SET NULL,
        FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE
    SET NULL
);
CREATE TABLE team_velocity (
    team_id INT NOT NULL,
    project_id INT NOT NULL,
    -- e.g., 2-week sprint
    avg_hours_per_point DECIMAL(5, 2) DEFAULT NULL,
    INDEX idx_team_velocity_team_id (team_id),
    INDEX idx_team_velocity_project_id (project_id),
    -- optional, calculated based on history
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, project_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);