-- ============================================================
-- 13. SKILL VERIFICATION TESTS TABLE
-- ============================================================
CREATE TABLE skill_verification_tests (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    skill_id VARCHAR(36) NOT NULL,
    resource_id VARCHAR(36),
    test_data JSON NOT NULL,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    passed BOOLEAN NOT NULL,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE
    SET NULL,
        INDEX idx_user_id (user_id),
        INDEX idx_skill_id (skill_id),
        INDEX idx_passed (passed)
);