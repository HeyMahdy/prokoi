-- Skills table
CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL, -- e.g., 'programming', 'design', 'testing'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User skills table (many-to-many)
CREATE TABLE user_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'advanced', 'expert') DEFAULT 'intermediate',
    years_experience DECIMAL(3,1) DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_skill (user_id, skill_id)
);

-- Issue skill requirements table
CREATE TABLE issue_skill_requirements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    skill_id INT NOT NULL,
    required_level ENUM('beginner', 'intermediate', 'advanced', 'expert') DEFAULT 'intermediate',
    is_mandatory BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE KEY unique_issue_skill (issue_id, skill_id)
);

-- User capacity table
CREATE TABLE user_capacity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    organization_id INT NOT NULL,
    weekly_hours DECIMAL(4,2) DEFAULT 40.0, -- standard weekly capacity
    current_utilization DECIMAL(5,2) DEFAULT 0.0, -- current workload percentage
    max_utilization DECIMAL(5,2) DEFAULT 100.0, -- maximum allowed workload
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_org_capacity (user_id, organization_id)
);

-- User availability table (for time off, holidays, etc.)
CREATE TABLE user_availability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date_from DATE NOT NULL,
    date_to DATE NOT NULL,
    availability_type ENUM('vacation', 'sick_leave', 'training', 'other') NOT NULL,
    hours_available DECIMAL(4,2) DEFAULT 0.0, -- 0 for full absence, partial for reduced hours
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Workload tracking table
CREATE TABLE user_workload (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    project_id INT NOT NULL,
    issue_id INT NULL, -- NULL for general project work
    hours_spent DECIMAL(5,2) DEFAULT 0.0,
    hours_estimated DECIMAL(5,2) DEFAULT 0.0,
    week_start_date DATE NOT NULL, -- start of work week
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE SET NULL
);

-- Assignment rules table
CREATE TABLE assignment_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    rule_name VARCHAR(200) NOT NULL,
    rule_type ENUM('workload_based', 'skill_based', 'availability_based', 'hybrid') NOT NULL,
    priority_order JSON NOT NULL, -- e.g., ["skills", "workload", "availability"]
    workload_threshold DECIMAL(5,2) DEFAULT 80.0, -- max workload percentage
    skill_match_threshold DECIMAL(3,2) DEFAULT 0.7, -- minimum skill match (0-1)
    auto_assign_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
);

-- User assignment preferences
CREATE TABLE user_assignment_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    preferred_workload_range_min DECIMAL(5,2) DEFAULT 60.0,
    preferred_workload_range_max DECIMAL(5,2) DEFAULT 90.0,
    preferred_issue_types JSON, -- e.g., ["bug", "feature"]
    preferred_project_domains JSON, -- e.g., ["frontend", "backend"]
    auto_assign_enabled BOOLEAN DEFAULT TRUE,
    max_concurrent_issues INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Assignment history table
CREATE TABLE issue_assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    assigned_to INT NULL,
    assigned_by INT NULL, -- NULL for auto-assignment
    assignment_type ENUM('manual', 'auto', 'suggested') NOT NULL,
    assignment_reason TEXT, -- explanation for auto-assignment
    assignment_score DECIMAL(3,2) DEFAULT 0.0, -- how well the assignment fits (0-1)
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Assignment analytics table
CREATE TABLE assignment_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    date DATE NOT NULL,
    total_issues INT DEFAULT 0,
    auto_assigned_issues INT DEFAULT 0,
    manual_assigned_issues INT DEFAULT 0,
    avg_assignment_score DECIMAL(3,2) DEFAULT 0.0,
    avg_workload_balance DECIMAL(3,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_org_date (organization_id, date)
);



