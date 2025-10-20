# Prokoi - Project Management & Issue Tracking API

A comprehensive FastAPI-based project management and issue tracking system designed for teams and organizations. Prokoi provides a robust backend API for managing projects, issues, sprints, team performance, and organizational workflows.

## 🚀 Features

### Core Functionality
- **User Management**: Authentication, authorization, and user profiles
- **Organization Management**: Multi-tenant organization support with role-based access control
- **Team Management**: Team creation, member management, and team performance tracking
- **Project Management**: Project creation, organization, and analysis
- **Issue Tracking**: Comprehensive issue management with types, labels, and workflows
- **Sprint Planning**: Sprint creation, velocity tracking, and sprint management
- **Skills Management**: Skill tracking and assignment for team members
- **Analytics & Reporting**: Project analysis, team performance metrics, and user performance tracking

### Technical Features
- **RESTful API**: Clean, well-documented API endpoints
- **Authentication**: JWT-based authentication with role-based permissions
- **Database**: MySQL with connection pooling and migrations
- **Security**: Password hashing with Argon2, CORS support
- **Data Seeding**: Comprehensive test data generation for development
- **Middleware**: Custom authentication and role-based access control middleware

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.118+
- **Database**: MySQL with aiomysql connector
- **Authentication**: JWT with python-jose
- **Password Hashing**: Argon2 via passlib
- **Data Generation**: Faker for test data
- **AI Integration**: LangGraph for AI-powered features
- **Environment Management**: python-dotenv and pydantic-settings

## 📋 Prerequisites

- Python 3.13+
- MySQL 8.0+
- Poetry (for dependency management)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prokoi
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DB_HOST=your_database_host
   DB_PORT=3306
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_NAME=prokoi

   # Security Configuration
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Set up the database**
   - Create a MySQL database named `prokoi`
   - Run the SQL migration files in the `src/models/` directory in order:
     - `V1_01_core_organizations.sql`
     - `V1_02_teams_memberships.sql`
     - `V1_03_workspaces_projects.sql`
     - `V1_04_roles_permissions.sql`
     - `V1_05_issues_workflow.sql`
     - `V1_06_extra_tables.sql`
     - `v1_07_extra_tables_02.sql`

5. **Seed the database (optional)**
   ```bash
   python src/seed.py
   ```

6. **Run the application**
   ```bash
   poetry run python src/app.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🏗️ Project Structure

```
prokoi/
├── src/
│   ├── api/                    # API route handlers
│   │   ├── users.py           # User management endpoints
│   │   ├── organizations.py   # Organization management
│   │   ├── teams.py           # Team management
│   │   ├── projects.py        # Project management
│   │   ├── issues.py          # Issue tracking
│   │   ├── sprints.py         # Sprint management
│   │   └── ...                # Additional API modules
│   ├── core/                  # Core application configuration
│   │   ├── config.py          # Settings and configuration
│   │   ├── database.py        # Database connection management
│   │   └── security.py        # Security utilities
│   ├── models/                # Database schema migrations
│   │   ├── V1_01_core_organizations.sql
│   │   ├── V1_02_teams_memberships.sql
│   │   └── ...                # Additional migration files
│   ├── repositories/          # Data access layer
│   ├── schemas/               # Pydantic models for request/response
│   ├── services/              # Business logic layer
│   ├── middleware/            # Custom middleware
│   ├── dependencies/          # FastAPI dependencies
│   ├── app.py                 # Main FastAPI application
│   └── seed.py                # Database seeding script
├── tests/                     # Test files
├── pyproject.toml            # Project dependencies and configuration
└── README.md                 # This file
```

## 🔐 Authentication

The API uses JWT-based authentication. To access protected endpoints:

1. **Register a new user**:
   ```bash
   POST /users/signup
   ```

2. **Login**:
   ```bash
   POST /users/login
   ```

3. **Use the token** in subsequent requests:
   ```bash
   Authorization: Bearer <your_jwt_token>
   ```

## 🎯 Key API Endpoints

### Users
- `POST /users/signup` - User registration
- `POST /users/login` - User authentication
- `GET /users/me` - Get current user profile

### Organizations
- `POST /api/organizations/create` - Create organization
- `GET /api/organizations` - List organizations
- `POST /api/organizations/{org_id}/invite` - Invite users

### Projects
- `POST /api/projects` - Create project
- `GET /api/projects` - List projects
- `GET /api/projects/{project_id}` - Get project details

### Issues
- `POST /api/projects/{project_id}/issues` - Create issue
- `GET /api/projects/{project_id}/issues` - List project issues
- `PUT /api/issues/{issue_id}` - Update issue
- `POST /api/issues/{issue_id}/assign` - Assign issue

### Sprints
- `POST /api/sprints` - Create sprint
- `GET /api/sprints` - List sprints
- `GET /api/sprints/{sprint_id}/velocity` - Get sprint velocity

## 🧪 Testing

The project includes a comprehensive seeding script (`src/seed.py`) that generates test data including:
- Test users with various roles
- Sample organizations and teams
- Projects with issues and sprints
- Performance metrics and analytics data

To populate the database with test data:
```bash
python src/seed.py
```

## 🔧 Development

### Running in Development Mode
```bash
# Install dependencies
poetry install

# Run with auto-reload
poetry run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
When making database changes:
1. Create new SQL migration files in `src/models/`
2. Follow the naming convention: `V1_XX_description.sql`
3. Update the seeding script if needed

## 📊 Database Schema

The application uses a comprehensive MySQL schema with the following main entities:
- **Users**: User accounts and authentication
- **Organizations**: Multi-tenant organization support
- **Teams**: Team management and member assignments
- **Projects**: Project organization and management
- **Issues**: Issue tracking with types, labels, and workflows
- **Sprints**: Sprint planning and velocity tracking
- **Skills**: Skill management and assignment
- **Performance**: Analytics and reporting tables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please contact: heymahdymuzzammil@gmail.com

---

**Prokoi** - Streamlining project management and team collaboration through intelligent issue tracking and analytics.
