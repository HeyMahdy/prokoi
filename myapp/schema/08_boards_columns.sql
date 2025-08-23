-- =======================
-- Boards & Columns
-- =======================

-- Boards table
CREATE TABLE boards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    type ENUM('scrum','kanban') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Board columns table
CREATE TABLE board_columns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    board_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    column_order INT NOT NULL,
    
    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Board column issues table
CREATE TABLE board_column_issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    board_column_id INT NOT NULL,
    issue_id INT NOT NULL,
    rank INT DEFAULT 0,
    
    FOREIGN KEY (board_column_id) REFERENCES board_columns(id) ON DELETE CASCADE,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    UNIQUE KEY unique_column_issue (board_column_id, issue_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
