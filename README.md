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
   Create a `.env` file in the root directory with your cloud service credentials:
   ```env
   # Database Configuration (PostgreSQL Cloud)
   DB_HOST=your-postgresql-cloud-host
   DB_PORT=5432
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_NAME=your-database-name

   # Security Configuration
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Redis Configuration (Redis Cloud)
   REDIS_HOST=your-redis-cloud-host
   REDIS_PORT=your-redis-port
   REDIS_PASSWORD=your-redis-password
   ```

4. **Set up the database**
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

### Running with Docker

If you prefer to run the application using Docker:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prokoi
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory with your cloud service credentials:
   ```env
   # Database Configuration (PostgreSQL Cloud)
   DB_HOST=your-postgresql-cloud-host
   DB_PORT=5432
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_NAME=your-database-name

   # Security Configuration
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Redis Configuration (Redis Cloud)
   REDIS_HOST=your-redis-cloud-host
   REDIS_PORT=your-redis-port
   REDIS_PASSWORD=your-redis-password
   ```

3. **Build and run with Docker**
   ```bash
   docker build -t prokoi .
   docker run -p 8000:8000 --env-file .env prokoi
   ```

The API will be available at `http://localhost:8000`