-- ============================================================
-- 11. BOOKMARKS TABLE
-- ============================================================
CREATE TABLE bookmarks (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    bookmark_type ENUM('job', 'resource') NOT NULL,
    bookmark_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_bookmark (user_id, bookmark_type, bookmark_id),
    INDEX idx_user_id (user_id),
    INDEX idx_bookmark_type (bookmark_type)
);