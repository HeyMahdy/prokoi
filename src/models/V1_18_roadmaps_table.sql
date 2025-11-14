-- ============================================================
-- 12. ROADMAPS TABLE
-- ============================================================
CREATE TABLE roadmaps (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    target_role VARCHAR(255) NOT NULL,
    time_frame INT NOT NULL,
    hours_per_week INT NOT NULL,
    summary TEXT,
    roadmap_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);