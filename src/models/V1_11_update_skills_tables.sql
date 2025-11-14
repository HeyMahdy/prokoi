-- ============================================================
-- UPDATE SKILLS TABLE TO USE UUIDs
-- ============================================================
ALTER TABLE skills
MODIFY COLUMN id VARCHAR(36) NOT NULL;
-- ============================================================
-- UPDATE USER SKILLS TABLE TO USE UUIDs
-- ============================================================
ALTER TABLE user_skills
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN skill_id VARCHAR(36) NOT NULL,
    MODIFY COLUMN proficiency ENUM('Beginner', 'Intermediate', 'Advanced', 'Expert') NOT NULL;
-- ============================================================
-- UPDATE USER EXPERIENCES TABLE TO USE UUIDs
-- ============================================================
ALTER TABLE user_experiences
MODIFY COLUMN id VARCHAR(36) NOT NULL,
    MODIFY COLUMN user_id VARCHAR(36) NOT NULL;
-- Make sure foreign key constraints are properly set
ALTER TABLE user_skills DROP FOREIGN KEY user_skills_ibfk_1,
    DROP FOREIGN KEY user_skills_ibfk_2;
ALTER TABLE user_skills
ADD CONSTRAINT fk_user_skills_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_user_skills_skill_id FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE;
ALTER TABLE user_experiences DROP FOREIGN KEY user_experience_ibfk_1;
ALTER TABLE user_experiences
ADD CONSTRAINT fk_user_experiences_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;