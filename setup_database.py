#!/usr/bin/env python3
"""
Database setup script for the rent agreement checker application.
This script creates the database and required tables.
"""

import mysql.connector
from mysql.connector import Error

def setup_database():
    """Create the database and tables if they don't exist."""
    
    # Database connection parameters
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Jay@2005'  # Update this to match your MySQL password
    }
    
    try:
        # Connect to MySQL server (without specifying database)
        print("Connecting to MySQL server...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        print("Creating database 'rent_agreements_db'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS rent_agreements_db")
        print("✅ Database created successfully!")
        
        # Use the database
        cursor.execute("USE rent_agreements_db")
        
        # Create users table
        print("Creating 'users' table...")
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(users_table)
        print("✅ Users table created successfully!")
        
        # Create analysis_history table
        print("Creating 'analysis_history' table...")
        history_table = """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            analysis_result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(history_table)
        print("✅ Analysis history table created successfully!")
        
        # Commit changes
        connection.commit()
        print("\n🎉 Database setup completed successfully!")
        print("You can now run your Flask application.")
        
    except Error as e:
        print(f"❌ Error setting up database: {e}")
        print("\nPossible solutions:")
        print("1. Make sure MySQL server is running")
        print("2. Check if the password 'Jay@2005' is correct")
        print("3. Make sure you have permission to create databases")
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    setup_database()