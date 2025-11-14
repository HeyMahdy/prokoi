-- First, rename the existing 'name' column to 'full_name' if it exists
SET @column_exists = (
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'users'
            AND COLUMN_NAME = 'name'
    );
SET @sql = IF(
        @column_exists > 0,
        'ALTER TABLE users CHANGE COLUMN name full_name VARCHAR(255) NOT NULL;',
        'SELECT ''Column rename not needed'';'
    );
PREPARE stmt
FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
-- Add the new columns if they don't exist
ALTER TABLE users
ADD COLUMN IF NOT EXISTS role ENUM('jobseeker', 'recruiter') NOT NULL DEFAULT 'jobseeker',
    ADD COLUMN IF NOT EXISTS education_level VARCHAR(100),
    ADD COLUMN IF NOT EXISTS department VARCHAR(100),
    ADD COLUMN IF NOT EXISTS experience_level ENUM('Fresher', 'Junior', 'Mid', 'Senior'),
    ADD COLUMN IF NOT EXISTS preferred_track VARCHAR(100),
    ADD COLUMN IF NOT EXISTS is_new_to_job_market BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE,
    ADD COLUMN IF NOT EXISTS last_login TIMESTAMP NULL;
-- Add indexes for the new columns
ALTER TABLE users
ADD INDEX IF NOT EXISTS idx_email (email),
    ADD INDEX IF NOT EXISTS idx_role (role),
    ADD INDEX IF NOT EXISTS idx_created_at (created_at),
    ADD INDEX IF NOT EXISTS idx_experience_level (experience_level),
    ADD INDEX IF NOT EXISTS idx_is_active (is_active);