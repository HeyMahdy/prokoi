-- Rename the 'name' column to 'full_name' to match the new schema
ALTER TABLE users CHANGE COLUMN name full_name VARCHAR(255) NOT NULL;
-- Change the id column from INT AUTO_INCREMENT to VARCHAR(36) to support UUIDs
ALTER TABLE users
MODIFY COLUMN id VARCHAR(36) NOT NULL;
-- Add the new columns to match your schema
ALTER TABLE users
ADD COLUMN role ENUM('jobseeker', 'recruiter') NOT NULL DEFAULT 'jobseeker',
    ADD COLUMN education_level VARCHAR(100),
    ADD COLUMN department VARCHAR(100),
    ADD COLUMN experience_level ENUM('Fresher', 'Junior', 'Mid', 'Senior'),
    ADD COLUMN preferred_track VARCHAR(100),
    ADD COLUMN is_new_to_job_market BOOLEAN DEFAULT FALSE,
    ADD COLUMN last_login TIMESTAMP NULL,
    ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
-- Update existing indexes and add new ones
ALTER TABLE users DROP INDEX idx_users_email,
    ADD UNIQUE INDEX idx_email (email),
    ADD INDEX idx_role (role),
    ADD INDEX idx_created_at (created_at),
    ADD INDEX idx_experience_level (experience_level),
    ADD INDEX idx_is_active (is_active);