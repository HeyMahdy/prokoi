-- ============================================================
-- UPDATE ISSUE SKILL REQUIREMENTS TABLE TO USE UUIDs
-- ============================================================
ALTER TABLE issue_skill_requirements
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN skill_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN required_level ENUM('Beginner', 'Intermediate', 'Advanced', 'Expert') NOT NULL;
-- Make sure foreign key constraints are properly set
ALTER TABLE issue_skill_requirements DROP FOREIGN KEY issue_skill_requirements_ibfk_1,
    DROP FOREIGN KEY issue_skill_requirements_ibfk_2;
ALTER TABLE issue_skill_requirements
ADD CONSTRAINT fk_issue_skill_requirements_issue_id FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issue_skill_requirements_skill_id FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE;