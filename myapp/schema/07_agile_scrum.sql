-- =======================
-- Agile & Scrum
-- =======================

-- Sprints table
CREATE TABLE sprints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('planned','active','completed') DEFAULT 'planned',
    goal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Epics table
CREATE TABLE epics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('todo','in_progress','done') DEFAULT 'todo',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Issue epic link table
CREATE TABLE issue_epic_link (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    epic_id INT NOT NULL,
    
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (epic_id) REFERENCES epics(id) ON DELETE CASCADE,
    UNIQUE KEY unique_issue_epic (issue_id, epic_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Backlog items table
CREATE TABLE backlog_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    issue_id INT NOT NULL,
    priority INT DEFAULT 0,
    rank INT DEFAULT 0,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_issue (project_id, issue_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sprint issues table
CREATE TABLE sprint_issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sprint_id INT NOT NULL,
    issue_id INT NOT NULL,
    rank INT DEFAULT 0,
    
    FOREIGN KEY (sprint_id) REFERENCES sprints(id) ON DELETE CASCADE,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    UNIQUE KEY unique_sprint_issue (sprint_id, issue_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
