-- =======================
-- Time Tracking
-- =======================

-- Work logs table
CREATE TABLE work_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    user_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Story points table
CREATE TABLE story_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    points DECIMAL(5,2) NOT NULL,
    
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    UNIQUE KEY unique_issue_points (issue_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
