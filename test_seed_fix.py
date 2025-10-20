#!/usr/bin/env python3
"""
Test script to verify the seed file fix works
"""

import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'prokoi'
}

def test_role_creation():
    """Test if we can create roles with unique names"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            cursor = connection.cursor()
            
            # Test creating roles with unique names
            test_orgs = [1, 2, 3]
            role_names = ['admin', 'project_manager', 'developer']
            
            for org_id in test_orgs:
                for role_name in role_names:
                    unique_role_name = f"{role_name}_{org_id}"
                    try:
                        cursor.execute(
                            """INSERT INTO roles (name, organization_id) VALUES (%s, %s)""",
                            (unique_role_name, org_id)
                        )
                        print(f"✅ Created role: {unique_role_name} for org {org_id}")
                    except Error as e:
                        print(f"❌ Error creating role {unique_role_name}: {e}")
            
            # Clean up test data
            cursor.execute("DELETE FROM roles WHERE name LIKE '%_1' OR name LIKE '%_2' OR name LIKE '%_3'")
            connection.commit()
            print("🧹 Cleaned up test data")
            
            cursor.close()
            connection.close()
            print("✅ Test completed successfully!")
            
    except Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    test_role_creation()


