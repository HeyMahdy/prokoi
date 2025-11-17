# Prokoi API Documentation

## Overview
Prokoi is a comprehensive career development platform that helps users build skills, find jobs, and create personalized learning roadmaps. This documentation provides detailed information about all available API endpoints.

## Authentication
Most endpoints require authentication using a Bearer token. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Base URL
```
http://localhost:8000
```

## API Endpoints

### 1. User Management

#### Sign Up
- **Endpoint**: `POST /users/signup`
- **Description**: Create a new user account
- **Request Body**:
  ```json
  {
    "full_name": "string",
    "email": "string",
    "password_hash": "string",
    "role": "jobseeker|recruiter"
  }
  ```
- **Response**: User object

#### Login
- **Endpoint**: `POST /users/login`
- **Description**: Authenticate user and get access token
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**: Token object with access token

### 2. Skills Management

#### Get All Skills
- **Endpoint**: `GET /api/skills`
- **Description**: Get all global skills
- **Response**: Array of skill objects

#### Get Skill by ID
- **Endpoint**: `GET /api/skills/{skill_id}`
- **Description**: Get a specific skill by ID
- **Response**: Skill object

#### Create Skill
- **Endpoint**: `POST /api/skills`
- **Description**: Create a new skill (admin only)
- **Request Body**:
  ```json
  {
    "name": "string",
    "category": "Technical|Soft Skill|Design|Business",
    "description": "string"
  }
  ```
- **Response**: Created skill object

#### Get User Skills
- **Endpoint**: `GET /api/users/{user_id}/skills`
- **Description**: Get all skills for a specific user
- **Response**: User skills list response

#### Add Skill to User
- **Endpoint**: `POST /api/users/{user_id}/skills/{skill_id}`
- **Description**: Add a skill to a user's profile
- **Request Body**:
  ```json
  {
    "proficiency_level": "Beginner|Intermediate|Advanced|Expert"
  }
  ```
- **Response**: User skill object

#### Update User Skill
- **Endpoint**: `PUT /api/users/{user_id}/skills/{skill_id}`
- **Description**: Update proficiency level for a user's skill
- **Request Body**:
  ```json
  {
    "proficiency_level": "Beginner|Intermediate|Advanced|Expert"
  }
  ```
- **Response**: Updated user skill object

#### Remove User Skill
- **Endpoint**: `DELETE /api/users/{user_id}/skills/{skill_id}`
- **Description**: Remove a skill from a user's profile
- **Response**: Success message

#### Get User Experiences
- **Endpoint**: `GET /api/users/{user_id}/experiences`
- **Description**: Get all experiences for a user
- **Response**: User experiences list response

#### Create User Experience
- **Endpoint**: `POST /api/users/{user_id}/experiences`
- **Description**: Add a new experience to user's profile
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "type": "Project|Work|Internship|Freelance|Volunteer",
    "company": "string",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "is_current": true
  }
  ```
- **Response**: Created experience object

#### Update User Experience
- **Endpoint**: `PUT /api/experiences/{experience_id}`
- **Description**: Update a user experience
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "type": "Project|Work|Internship|Freelance|Volunteer",
    "company": "string",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "is_current": true
  }
  ```
- **Response**: Updated experience object

#### Delete User Experience
- **Endpoint**: `DELETE /api/experiences/{experience_id}`
- **Description**: Remove an experience from user's profile
- **Response**: Success message

### 3. Jobs Management

#### Create Job
- **Endpoint**: `POST /api/`
- **Description**: Create a new job posting (recruiters only)
- **Request Body**:
  ```json
  {
    "title": "string",
    "company": "string",
    "location": "string",
    "is_remote": true,
    "recommended_experience": "Fresher|Junior|Mid|Senior",
    "job_type": "Full-time|Part-time|Internship|Freelance|Contract",
    "description": "string",
    "requirements": "string",
    "responsibilities": "string",
    "salary_range": "string",
    "application_deadline": "2023-12-31T00:00:00"
  }
  ```
- **Response**: Created job object

#### Get Job by ID
- **Endpoint**: `GET /api/search/{job_id}`
- **Description**: Get a specific job by ID
- **Response**: Job object

#### Update Job
- **Endpoint**: `PUT /api/update/{job_id}`
- **Description**: Update a job posting (recruiters only)
- **Request Body**:
  ```json
  {
    "title": "string",
    "company": "string",
    "location": "string",
    "is_remote": true,
    "recommended_experience": "Fresher|Junior|Mid|Senior",
    "job_type": "Full-time|Part-time|Internship|Freelance|Contract",
    "description": "string",
    "requirements": "string",
    "responsibilities": "string",
    "salary_range": "string",
    "application_deadline": "2023-12-31T00:00:00",
    "is_active": true
  }
  ```
- **Response**: Updated job object

#### Delete Job
- **Endpoint**: `DELETE /api/put/{job_id}`
- **Description**: Delete a job posting (recruiters only)
- **Response**: Success message

#### Search Jobs
- **Endpoint**: `GET /api/get`
- **Description**: Search jobs with filters
- **Query Parameters**:
  - `search_term`: string (optional)
  - `location`: string (optional)
  - `job_type`: string (optional)
  - `is_remote`: boolean (optional)
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of jobs

#### Add Skill to Job
- **Endpoint**: `POST /api/{job_id}/skills/{skill_id}`
- **Description**: Add a skill requirement to a job (recruiters only)
- **Response**: Success message

#### Remove Skill from Job
- **Endpoint**: `DELETE /api/{job_id}/skills/{skill_id}`
- **Description**: Remove a skill requirement from a job (recruiters only)
- **Response**: Success message

#### Get Job Skills
- **Endpoint**: `GET /api/{job_id}/skills`
- **Description**: Get all skills required for a job
- **Response**: List of skills

#### Apply for Job
- **Endpoint**: `POST /api/{job_id}/apply`
- **Description**: Apply for a job (jobseekers only)
- **Request Body**:
  ```json
  {
    "cover_letter": "string",
    "resume_url": "string"
  }
  ```
- **Response**: Job application object

#### Get My Applications
- **Endpoint**: `GET /api/applications/my`
- **Description**: Get all job applications for the current user (jobseekers only)
- **Response**: List of job applications

#### Get Job Applications
- **Endpoint**: `GET /api/{job_id}/applications`
- **Description**: Get all applications for a job (recruiters only)
- **Response**: List of job applications

#### Update Application Status
- **Endpoint**: `PUT /api/applications/{application_id}/status`
- **Description**: Update job application status (recruiters only)
- **Query Parameters**:
  - `status`: string (pending, reviewed, shortlisted, rejected, accepted)
  - `notes`: string (optional)
- **Response**: Updated job application object

### 4. Resources Management

#### Create Resource
- **Endpoint**: `POST /api/resources/create`
- **Description**: Create a new learning resource
- **Request Body**:
  ```json
  {
    "title": "string",
    "platform": "YouTube|Udemy|Coursera|edX|LinkedIn Learning|Other",
    "url": "string",
    "cost": "Free|Paid|Freemium",
    "description": "string",
    "duration_hours": 5.5,
    "difficulty_level": "Beginner|Intermediate|Advanced",
    "rating": 4.5
  }
  ```
- **Response**: Created resource object

#### Get Resource by ID
- **Endpoint**: `GET /api/resources/get/{resource_id}`
- **Description**: Get a specific resource by ID
- **Response**: Resource object

#### Update Resource
- **Endpoint**: `PUT /api/resources/put/{resource_id}`
- **Description**: Update a resource
- **Request Body**:
  ```json
  {
    "title": "string",
    "platform": "YouTube|Udemy|Coursera|edX|LinkedIn Learning|Other",
    "url": "string",
    "cost": "Free|Paid|Freemium",
    "description": "string",
    "duration_hours": 5.5,
    "difficulty_level": "Beginner|Intermediate|Advanced",
    "rating": 4.5,
    "is_active": true
  }
  ```
- **Response**: Updated resource object

#### Delete Resource
- **Endpoint**: `DELETE /api/resources/del/{resource_id}`
- **Description**: Delete a resource
- **Response**: Success message

#### Get All Resources
- **Endpoint**: `GET /api/resources/getall`
- **Description**: Get all resources with optional filters
- **Query Parameters**:
  - `platform`: string (optional)
  - `cost`: string (optional)
  - `difficulty_level`: string (optional)
  - `min_rating`: number (optional)
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of resources

#### Add Skill to Resource
- **Endpoint**: `POST /api/resources/{resource_id}/skills/{skill_id}`
- **Description**: Add a skill to a resource
- **Response**: Success message

#### Remove Skill from Resource
- **Endpoint**: `DELETE /api/resources/{resource_id}/skills/{skill_id}`
- **Description**: Remove a skill from a resource
- **Response**: Success message

#### Get Resource Skills
- **Endpoint**: `GET /api/resources/{resource_id}/skills`
- **Description**: Get all skills for a resource
- **Response**: List of skills

#### Start Resource Progress
- **Endpoint**: `POST /api/resources/{resource_id}/progress/start`
- **Description**: Start tracking progress for a resource
- **Response**: Progress object

#### Update Resource Progress
- **Endpoint**: `PUT /api/resources/{resource_id}/progress`
- **Description**: Update user progress for a resource
- **Request Body**:
  ```json
  {
    "status": "not_started|in_progress|completed",
    "progress_percentage": 0,
    "test_taken": true,
    "test_score": 85,
    "test_passed": true
  }
  ```
- **Response**: Updated progress object

#### Get User Resource Progress
- **Endpoint**: `GET /api/resources/{resource_id}/progress`
- **Description**: Get user progress for a specific resource
- **Response**: Progress object

#### Get My Resources Progress
- **Endpoint**: `GET /api/resources/progress/my`
- **Description**: Get all resources progress for the current user
- **Query Parameters**:
  - `status`: string (optional)
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of progress objects

### 5. Bookmarks Management

#### Create Bookmark
- **Endpoint**: `POST /api/bookmarks/`
- **Description**: Create a new bookmark
- **Request Body**:
  ```json
  {
    "bookmark_type": "job|resource",
    "bookmark_id": "string"
  }
  ```
- **Response**: Created bookmark object

#### Get Bookmark by ID
- **Endpoint**: `GET /api/bookmarks/{bookmark_id}`
- **Description**: Get a specific bookmark by ID
- **Response**: Bookmark object

#### Delete Bookmark
- **Endpoint**: `DELETE /api/bookmarks/{bookmark_id}`
- **Description**: Delete a bookmark by ID
- **Response**: Success message

#### Get User Bookmarks
- **Endpoint**: `GET /api/bookmarks/`
- **Description**: Get all bookmarks for the current user
- **Query Parameters**:
  - `bookmark_type`: string (job|resource) (optional)
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of bookmarks

#### Check if Bookmarked
- **Endpoint**: `POST /api/bookmarks/check`
- **Description**: Check if a specific item is bookmarked by the current user
- **Request Body**:
  ```json
  {
    "bookmark_type": "job|resource",
    "bookmark_id": "string"
  }
  ```
- **Response**: Bookmark check response

#### Delete User Bookmark
- **Endpoint**: `DELETE /api/bookmarks/user/{bookmark_type}/{bookmark_id}`
- **Description**: Delete a specific bookmark for the current user
- **Response**: Success message

### 6. Roadmaps Management

#### Create Roadmap
- **Endpoint**: `POST /api/roadmaps/`
- **Description**: Create a new career roadmap
- **Request Body**:
  ```json
  {
    "target_role": "string",
    "time_frame": 0,
    "hours_per_week": 0,
    "summary": "string",
    "roadmap_data": {}
  }
  ```
- **Response**: Created roadmap object

#### Get Roadmap by ID
- **Endpoint**: `GET /api/roadmaps/{roadmap_id}`
- **Description**: Get a specific roadmap by ID
- **Response**: Roadmap object

#### Update Roadmap
- **Endpoint**: `PUT /api/roadmaps/{roadmap_id}`
- **Description**: Update a roadmap
- **Request Body**:
  ```json
  {
    "target_role": "string",
    "time_frame": 0,
    "hours_per_week": 0,
    "summary": "string",
    "roadmap_data": {}
  }
  ```
- **Response**: Updated roadmap object

#### Delete Roadmap
- **Endpoint**: `DELETE /api/roadmaps/{roadmap_id}`
- **Description**: Delete a roadmap
- **Response**: Success message

#### Get User Roadmaps
- **Endpoint**: `GET /api/roadmaps/`
- **Description**: Get all roadmaps for the current user
- **Query Parameters**:
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of roadmaps

### 7. Skill Verification Tests

#### Create Test
- **Endpoint**: `POST /api/skill-tests/`
- **Description**: Create a new skill verification test result
- **Request Body**:
  ```json
  {
    "skill_id": "string",
    "resource_id": "string",
    "test_data": {},
    "score": 0,
    "total_questions": 0,
    "passed": true
  }
  ```
- **Response**: Created test object

#### Get Test by ID
- **Endpoint**: `GET /api/skill-tests/{test_id}`
- **Description**: Get a specific test by ID
- **Response**: Test object

#### Delete Test
- **Endpoint**: `DELETE /api/skill-tests/{test_id}`
- **Description**: Delete a test by ID
- **Response**: Success message

#### Get User Tests
- **Endpoint**: `GET /api/skill-tests/`
- **Description**: Get all tests for the current user
- **Query Parameters**:
  - `skill_id`: string (optional)
  - `passed`: boolean (optional)
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of tests

#### Get User Skill Tests
- **Endpoint**: `GET /api/skill-tests/skill/{skill_id}`
- **Description**: Get all tests for a specific skill for the current user
- **Response**: List of tests for the skill

### 8. CV Management

#### Create CV Upload
- **Endpoint**: `POST /api/cv-uploads/`
- **Description**: Create a new CV upload record
- **Request Body**:
  ```json
  {
    "file_name": "string",
    "file_url": "string",
    "file_type": "string",
    "extracted_data": {}
  }
  ```
- **Response**: Created CV upload object

#### Get CV Upload by ID
- **Endpoint**: `GET /api/cv-uploads/{upload_id}`
- **Description**: Get a specific CV upload by ID
- **Response**: CV upload object

#### Delete CV Upload
- **Endpoint**: `DELETE /api/cv-uploads/{upload_id}`
- **Description**: Delete a CV upload by ID
- **Response**: Success message

#### Get User CV Uploads
- **Endpoint**: `GET /api/cv-uploads/`
- **Description**: Get all CV uploads for the current user
- **Query Parameters**:
  - `limit`: integer (default: 20)
  - `offset`: integer (default: 0)
- **Response**: List of CV uploads

#### Create or Update CV Notes
- **Endpoint**: `POST /api/cv-notes/`
- **Description**: Create or update CV notes for the current user
- **Request Body**:
  ```json
  {
    "notes": "string"
  }
  ```
- **Response**: CV notes object

#### Get User CV Notes
- **Endpoint**: `GET /api/cv-notes/`
- **Description**: Get CV notes for the current user
- **Response**: CV notes object

#### Update CV Notes
- **Endpoint**: `PUT /api/cv-notes/{note_id}`
- **Description**: Update CV notes by ID
- **Request Body**:
  ```json
  {
    "notes": "string"
  }
  ```
- **Response**: Updated CV notes object

#### Delete CV Notes
- **Endpoint**: `DELETE /api/cv-notes/{note_id}`
- **Description**: Delete CV notes by ID
- **Response**: Success message

### 9. AI Learning Recommendations

#### Generate Learning Recommendations
- **Endpoint**: `POST /run-learning-recommendations`
- **Description**: Generate personalized learning recommendations using AI
- **Request Body**:
  ```json
  {
    "input": "string",
    "user_id": "string"
  }
  ```
- **Response**: AI-generated recommendations

## Error Responses
All endpoints follow standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting
The API implements rate limiting to prevent abuse. Exceeding the limit will result in a 429 (Too Many Requests) response.

## Support
For API support, contact the development team or refer to the project documentation.