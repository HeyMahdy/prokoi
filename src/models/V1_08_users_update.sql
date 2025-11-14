ALTER TABLE users
ADD COLUMN role ENUM('jobseeker', 'recruiter') NOT NULL DEFAULT 'jobseeker',
    ADD COLUMN education_level VARCHAR(100),
    ADD COLUMN department VARCHAR(100),
    ADD COLUMN experience_level ENUM('Fresher', 'Junior', 'Mid', 'Senior'),
    ADD COLUMN preferred_track VARCHAR(100),
    ADD COLUMN is_new_to_job_market BOOLEAN DEFAULT FALSE,
    ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
-- Add indexes for the new columns
ALTER TABLE users
ADD INDEX idx_role (role),
    ADD INDEX idx_experience_level (experience_level),
    ADD INDEX idx_is_active (is_active);