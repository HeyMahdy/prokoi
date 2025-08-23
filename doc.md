CORE & ORGANIZATIONS

// Organizations
GET    /api/organizations
POST   /api/organizations
GET    /api/organizations/:id
PUT    /api/organizations/:id
DELETE /api/organizations/:id
GET    /api/organizations/:id/settings
PUT    /api/organizations/:id/settings

// Users
GET    /api/users
POST   /api/users
GET    /api/users/:id
PUT    /api/users/:id
DELETE /api/users/:id
POST   /api/users/:id/activate
POST   /api/users/:id/suspend
GET    /api/users/:id/activity
PUT    /api/users/:id/profile

// Authentication
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh-token
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
POST   /api/auth/verify-email
GET    /api/auth/me

TEAMS & MEMBERSHIPS

// Teams
GET    /api/teams
POST   /api/teams
GET    /api/teams/:id
PUT    /api/teams/:id
DELETE /api/teams/:id
GET    /api/teams/:id/members
GET    /api/teams/:id/projects

// Team Members
POST   /api/teams/:id/members
DELETE /api/teams/:id/members/:userId
PUT    /api/teams/:id/members/:userId/role
GET    /api/teams/:id/members/:userId


WORKSPACES & PROJECTS

// Workspaces
GET    /api/workspaces
POST   /api/workspaces
GET    /api/workspaces/:id
PUT    /api/workspaces/:id
DELETE /api/workspaces/:id
GET    /api/workspaces/:id/projects
GET    /api/workspaces/:id/members

// Projects
GET    /api/projects
POST   /api/projects
GET    /api/projects/:id
PUT    /api/projects/:id
DELETE /api/projects/:id
GET    /api/projects/:id/issues
GET    /api/projects/:id/boards
GET    /api/projects/:id/sprints
GET    /api/projects/:id/statistics
GET    /api/projects/:id/permissions
PUT    /api/projects/:id/permissions

ROLES & PERMISSIONS

// Roles
GET    /api/roles
POST   /api/roles
GET    /api/roles/:id
PUT    /api/roles/:id
DELETE /api/roles/:id
GET    /api/roles/:id/permissions
PUT    /api/roles/:id/permissions

// Permissions
GET    /api/permissions
POST   /api/permissions
GET    /api/permissions/:id
PUT    /api/permissions/:id
DELETE /api/permissions/:id

// Role Permissions
POST   /api/roles/:id/permissions/:permissionId
DELETE /api/roles/:id/permissions/:permissionId
GET    /api/roles/:id/permissions

// User Roles
GET    /api/users/:id/roles
POST   /api/users/:id/roles
DELETE /api/users/:id/roles/:roleId
PUT    /api/users/:id/roles/:roleId


ISSUES & WORKFLOW

// Issue Types
GET    /api/issue-types
POST   /api/issue-types
GET    /api/issue-types/:id
PUT    /api/issue-types/:id
DELETE /api/issue-types/:id

// Issues
GET    /api/issues
POST   /api/issues
GET    /api/issues/:id
PUT    /api/issues/:id
DELETE /api/issues/:id
GET    /api/issues/:id/history
GET    /api/issues/:id/transitions
POST   /api/issues/:id/transitions
GET    /api/issues/:id/links
POST   /api/issues/:id/links
DELETE /api/issues/:id/links/:linkId

// Custom Fields
GET    /api/custom-fields
POST   /api/custom-fields
GET    /api/custom-fields/:id
PUT    /api/custom-fields/:id
DELETE /api/custom-fields/:id
GET    /api/custom-fields/:id/values

// Issue Custom Values
GET    /api/issues/:id/custom-fields
PUT    /api/issues/:id/custom-fields
POST   /api/issues/:id/custom-fields/:fieldId
DELETE /api/issues/:id/custom-fields/:fieldId

// Issue Watchers
GET    /api/issues/:id/watchers
POST   /api/issues/:id/watchers
DELETE /api/issues/:id/watchers/:userId

// Labels
GET    /api/labels
POST   /api/labels
GET    /api/labels/:id
PUT    /api/labels/:id
DELETE /api/labels/:id
GET    /api/labels/:id/issues

// Issue Labels
GET    /api/issues/:id/labels
POST   /api/issues/:id/labels
DELETE /api/issues/:id/labels/:labelId

// Checklists
GET    /api/issues/:id/checklists
POST   /api/issues/:id/checklists
GET    /api/checklists/:id
PUT    /api/checklists/:id
DELETE /api/checklists/:id

// Checklist Items
GET    /api/checklists/:id/items
POST   /api/checklists/:id/items
PUT    /api/checklist-items/:id
DELETE /api/checklist-items/:id

TIME TRACKING

// Work Logs
GET    /api/issues/:id/work-logs
POST   /api/issues/:id/work-logs
GET    /api/work-logs/:id
PUT    /api/work-logs/:id
DELETE /api/work-logs/:id
GET    /api/users/:id/work-logs
GET    /api/projects/:id/work-logs

// Story Points
GET    /api/issues/:id/story-points
PUT    /api/issues/:id/story-points
DELETE /api/issues/:id/story-points

AGILE & SCRUM

// Sprints
GET    /api/sprints
POST   /api/sprints
GET    /api/sprints/:id
PUT    /api/sprints/:id
DELETE /api/sprints/:id
POST   /api/sprints/:id/start
POST   /api/sprints/:id/complete
GET    /api/sprints/:id/issues
GET    /api/sprints/:id/statistics

// Sprint Issues
POST   /api/sprints/:id/issues
DELETE /api/sprints/:id/issues/:issueId
PUT    /api/sprints/:id/issues/rank

// Epics
GET    /api/epics
POST   /api/epics
GET    /api/epics/:id
PUT    /api/epics/:id
DELETE /api/epics/:id
GET    /api/epics/:id/issues
POST   /api/epics/:id/issues

// Issue Epic Links
GET    /api/issues/:id/epic
PUT    /api/issues/:id/epic
DELETE /api/issues/:id/epic

// Backlog Items
GET    /api/backlog
POST   /api/backlog/rank
PUT    /api/backlog/:id/priority
PUT    /api/backlog/:id/rank
DELETE /api/backlog/:id

BOARDS & COLUMNS

// Boards
GET    /api/boards
POST   /api/boards
GET    /api/boards/:id
PUT    /api/boards/:id
DELETE /api/boards/:id
GET    /api/boards/:id/columns
GET    /api/boards/:id/issues

// Board Columns
POST   /api/boards/:id/columns
PUT    /api/board-columns/:id
DELETE /api/board-columns/:id
PUT    /api/board-columns/:id/order

// Board Column Issues
GET    /api/board-columns/:id/issues
POST   /api/board-columns/:id/issues
PUT    /api/board-columns/:id/issues/rank
DELETE /api/board-columns/:id/issues/:issueId

REPORTING & ANALYTICS

// Reports
GET    /api/reports
POST   /api/reports
GET    /api/reports/:id
PUT    /api/reports/:id
DELETE /api/reports/:id
POST   /api/reports/:id/execute
GET    /api/reports/:id/export

// Report Results
GET    /api/reports/:id/results
POST   /api/reports/:id/results
DELETE /api/report-results/:id

// Dashboards
GET    /api/dashboards
POST   /api/dashboards
GET    /api/dashboards/:id
PUT    /api/dashboards/:id
DELETE /api/dashboards/:id
GET    /api/dashboards/:id/widgets

// Dashboard Widgets
POST   /api/dashboards/:id/widgets
PUT    /api/dashboard-widgets/:id
DELETE /api/dashboard-widgets/:id
PUT    /api/dashboard-widgets/:id/config

ATTACHMENTS & NOTIFICATIONS

// Attachments
GET    /api/issues/:id/attachments
POST   /api/issues/:id/attachments
GET    /api/attachments/:id
DELETE /api/attachments/:id
GET    /api/attachments/:id/download

// Notifications
GET    /api/notifications
POST   /api/notifications
GET    /api/notifications/:id
PUT    /api/notifications/:id
DELETE /api/notifications/:id
PUT    /api/notifications/:id/read
PUT    /api/notifications/read-all
GET    /api/notifications/unread


AUDIT LOGS

// Audit Logs
GET    /api/audit-logs
GET    /api/audit-logs/:id
GET    /api/audit-logs/by-user/:userId
GET    /api/audit-logs/by-target/:targetType/:targetId
GET    /api/audit-logs/by-action/:action
POST   /api/audit-logs/export


TABLES I MISSED

// Issue Links
GET    /api/issues/:id/links
POST   /api/issues/:id/links
DELETE /api/issue-links/:id

// Issue History
GET    /api/issues/:id/history
GET    /api/issue-history/:id

// Issue Transitions
GET    /api/issues/:id/transitions
POST   /api/issues/:id/transitions/:transitionId

// Workflow Schemes
GET    /api/workflow-schemes
POST   /api/workflow-schemes
GET    /api/workflow-schemes/:id
PUT    /api/workflow-schemes/:id
DELETE /api/workflow-schemes/:id

// Screen Schemes
GET    /api/screen-schemes
POST   /api/screen-schemes
GET    /api/screen-schemes/:id
PUT    /api/screen-schemes/:id
DELETE /api/screen-schemes/:id

// Permission Schemes
GET    /api/permission-schemes
POST   /api/permission-schemes
GET    /api/permission-schemes/:id
PUT    /api/permission-schemes/:id
DELETE /api/permission-schemes/:id

// Notification Schemes
GET    /api/notification-schemes
POST   /api/notification-schemes
GET    /api/notification-schemes/:id
PUT    /api/notification-schemes/:id
DELETE /api/notification-schemes/:id

// Issue Type Schemes
GET    /api/issue-type-schemes
POST   /api/issue-type-schemes
GET    /api/issue-type-schemes/:id
PUT    /api/issue-type-schemes/:id
DELETE /api/issue-type-schemes/:id




























