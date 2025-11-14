-- ============================================================
-- UPDATE ISSUES TABLE TO USE UUIDs
-- ============================================================
ALTER TABLE issues
MODIFY COLUMN id VARCHAR(36) NOT NULL;
-- ============================================================
-- UPDATE OTHER RELATED TABLES TO USE UUIDs
-- ============================================================
-- Update issues table references
ALTER TABLE issue_comments
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36);
ALTER TABLE issue_history
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36);
ALTER TABLE issue_labels
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN label_id VARCHAR(36) NOT NULL;
ALTER TABLE issue_assignments
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN assigned_to VARCHAR(36),
    MODIFY COLUMN assigned_by VARCHAR(36);
ALTER TABLE issue_sprints
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN sprint_id VARCHAR(36) NOT NULL;
ALTER TABLE issue_skill_requirements
MODIFY COLUMN issue_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN skill_id VARCHAR(36) NOT NULL;
-- Update foreign key constraints
ALTER TABLE issue_comments DROP FOREIGN KEY issue_comments_ibfk_1,
    DROP FOREIGN KEY issue_comments_ibfk_2;
ALTER TABLE issue_comments
ADD CONSTRAINT fk_issue_comments_issue_id FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issue_comments_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
SET NULL;
ALTER TABLE issue_history DROP FOREIGN KEY issue_history_ibfk_1,
    DROP FOREIGN KEY issue_history_ibfk_2;
ALTER TABLE issue_history
ADD CONSTRAINT fk_issue_history_issue_id FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issue_history_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
SET NULL;
ALTER TABLE issue_labels DROP FOREIGN KEY issue_labels_ibfk_1,
    DROP FOREIGN KEY issue_labels_ibfk_2;
ALTER TABLE issue_labels
ADD CONSTRAINT fk_issue_labels_issue_id FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issue_labels_label_id FOREIGN KEY (label_id) REFERENCES labels(id) ON DELETE CASCADE;
ALTER TABLE issue_assignments DROP FOREIGN KEY issue_assignments_ibfk_1,
    DROP FOREIGN KEY issue_assignments_ibfk_2,
    DROP FOREIGN KEY issue_assignments_ibfk_3;
ALTER TABLE issue_assignments
ADD CONSTRAINT fk_issue_assignments_issue_id FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issue_assignments_assigned_to FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE
SET NULL,
    ADD CONSTRAINT fk_issue_assignments_assigned_by FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE
SET NULL;
ALTER TABLE issue_sprints DROP FOREIGN KEY issue_sprints_ibfk_1,
    DROP FOREIGN KEY issue_sprints_ibfk_2;
ALTER TABLE issue_sprints
ADD CONSTRAINT fk_issue_sprints_issue_id FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_issue_sprints_sprint_id FOREIGN KEY (sprint_id) REFERENCES sprints(id) ON DELETE CASCADE;