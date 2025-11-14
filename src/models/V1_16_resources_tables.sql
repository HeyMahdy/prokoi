-- ============================================================
-- 8. RESOURCES TABLE
-- ============================================================
CREATE TABLE resources (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    platform ENUM(
        'YouTube',
        'Udemy',
        'Coursera',
        'edX',
        'LinkedIn Learning',
        'Other'
    ) NOT NULL,
    url VARCHAR(500) NOT NULL,
    cost ENUM('Free', 'Paid', 'Freemium') NOT NULL,
    description TEXT,
    duration_hours DECIMAL(5, 2),
    difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    rating DECIMAL(2, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_platform (platform),
    INDEX idx_cost (cost),
    INDEX idx_difficulty_level (difficulty_level),
    INDEX idx_rating (rating)
);
-- ============================================================
-- 9. RESOURCE SKILLS TABLE
-- ============================================================
CREATE TABLE resource_skills (
    id VARCHAR(36) PRIMARY KEY,
    resource_id VARCHAR(36) NOT NULL,
    skill_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE KEY unique_resource_skill (resource_id, skill_id),
    INDEX idx_resource_id (resource_id),
    INDEX idx_skill_id (skill_id)
);
-- ============================================================
-- 10. USER RESOURCE PROGRESS TABLE
-- ============================================================
CREATE TABLE user_resource_progress (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    resource_id VARCHAR(36) NOT NULL,
    status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
    progress_percentage INT DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    test_taken BOOLEAN DEFAULT FALSE,
    test_score INT,
    test_passed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_resource (user_id, resource_id),
    INDEX idx_user_id (user_id),
    INDEX idx_resource_id (resource_id),
    INDEX idx_status (status)
);