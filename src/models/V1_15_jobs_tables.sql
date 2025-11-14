-- ============================================================
-- 5. JOBS TABLE
-- ============================================================
CREATE TABLE jobs (
    id VARCHAR(36) PRIMARY KEY,
    recruiter_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    is_remote BOOLEAN DEFAULT FALSE,
    recommended_experience ENUM('Fresher', 'Junior', 'Mid', 'Senior') NOT NULL,
    job_type ENUM(
        'Full-time',
        'Part-time',
        'Internship',
        'Freelance',
        'Contract'
    ) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    responsibilities TEXT,
    salary_range VARCHAR(100),
    application_deadline DATE,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (recruiter_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_recruiter_id (recruiter_id),
    INDEX idx_location (location),
    INDEX idx_job_type (job_type),
    INDEX idx_is_active (is_active),
    INDEX idx_posted_date (posted_date)
);
-- ============================================================
-- 6. JOB SKILLS TABLE
-- ============================================================
CREATE TABLE job_skills (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL,
    skill_id VARCHAR(36) NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    priority ENUM('Must-have', 'Nice-to-have') DEFAULT 'Must-have',
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE KEY unique_job_skill (job_id, skill_id),
    INDEX idx_job_id (job_id),
    INDEX idx_skill_id (skill_id)
);
-- ============================================================
-- 7. JOB APPLICATIONS TABLE
-- ============================================================
CREATE TABLE job_applications (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    cover_letter TEXT,
    resume_url VARCHAR(500),
    status ENUM(
        'pending',
        'reviewed',
        'shortlisted',
        'rejected',
        'accepted'
    ) DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_application (job_id, user_id),
    INDEX idx_job_id (job_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_applied_at (applied_at)
);