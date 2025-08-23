-- =======================
-- Master Setup File
-- =======================
-- Run this file to set up the entire database

-- Create database
CREATE DATABASE IF NOT EXISTS prokoi_pm;
USE prokoi_pm;

-- Note: Run the individual SQL files in this order:
-- 1. 01_core_organizations.sql
-- 2. 02_teams_memberships.sql  
-- 3. 03_workspaces_projects.sql
-- 4. 04_roles_permissions.sql
-- 5. 05_issues_workflow.sql
-- 6. 06_time_tracking.sql
-- 7. 07_agile_scrum.sql
-- 8. 08_boards_columns.sql
-- 9. 09_reporting_analytics.sql
-- 10. 10_attachments_notifications.sql
-- 11. 11_audit_logs.sql

-- Or run them all at once by concatenating the files
