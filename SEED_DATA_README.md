# Prokoi Seed Data

This directory contains scripts to populate the Prokoi database with sample data for testing and development purposes.

## Available Seed Scripts

1. **[seed_data.py](file:///home/mahdy/PycharmProjects/prokoi/seed_data.py)** - Python script that uses the application's database connection to insert sample data
2. **[seed_data.sql](file:///home/mahdy/PycharmProjects/prokoi/seed_data.sql)** - SQL script that can be executed directly against the database

## Data Model Overview

The seed data includes:

- 3 Organizations
- 6 Users
- 6 Teams
- 6 Workspaces
- 6 Projects
- 5 Issue Types
- 8 Skills
- 5 Issues
- Associated roles, permissions, labels, sprints, comments, and checklists

## How to Use

### Method 1: Using the Python Script

1. Make sure your database is running and accessible
2. Update your [.env](file:///home/mahdy/PycharmProjects/prokoi/.env) file with correct database credentials
3. Run the seed script:
   ```bash
   poetry run python seed_data.py
   ```

### Method 2: Using the SQL Script

1. Make sure your database is running and accessible
2. Execute the SQL script using your preferred MySQL client:
   ```bash
   mysql -u your_username -p prokoi < seed_data.sql
   ```
   
   Or in MySQL shell:
   ```sql
   SOURCE seed_data.sql;
   ```

## Data Structure

### Organizations
- TechCorp
- InnovateX
- Global Solutions

### Users
1. Alice Johnson (alice@techcorp.com) - Admin at TechCorp
2. Bob Smith (bob@techcorp.com) - Developer at TechCorp
3. Carol Williams (carol@innovatex.com) - Project Manager at InnovateX
4. David Brown (david@innovatex.com) - Developer at InnovateX
5. Eve Davis (eve@globalsolutions.com) - Admin at Global Solutions
6. Frank Miller (frank@globalsolutions.com) - Developer at Global Solutions

### Teams
- Frontend Team (TechCorp)
- Backend Team (TechCorp)
- QA Team (TechCorp)
- Design Team (InnovateX)
- DevOps Team (InnovateX)
- Analytics Team (Global Solutions)

### Skills
- Python
- JavaScript
- React
- Node.js
- SQL
- UI/UX Design
- Testing
- DevOps

## Notes

- Password for all users is `password123` (hashed in the database)
- The seed scripts will clear existing data before inserting new records
- The SQL script disables foreign key checks during data clearing for simplicity
- Both scripts create the same dataset, so you only need to use one method

## Troubleshooting

If you encounter issues:

1. Ensure your database connection settings in [.env](file:///home/mahdy/PycharmProjects/prokoi/.env) are correct
2. Verify the database `prokoi` exists and is accessible
3. Check that all required tables have been created by running the migration scripts first
4. Make sure you have the necessary permissions to insert data into the database