#!/usr/bin/env python3
"""
Test database connection and verify user registration/login works
"""

import mysql.connector
from mysql.connector import Error
import requests
import json

def test_direct_db_connection():
    """Test direct database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jay@2005',
            database='rent_agreements_db'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Test if tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("✅ Database connected successfully!")
            print(f"📋 Tables found: {[table[0] for table in tables]}")
            
            # Test users table structure
            cursor.execute("DESCRIBE users")
            user_columns = cursor.fetchall()
            print(f"👤 Users table structure: {[col[0] for col in user_columns]}")
            
            # Count existing users
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"👥 Total users in database: {user_count}")
            
            return True
            
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def test_api_registration():
    """Test user registration via API"""
    try:
        test_user = {
            "email": "testuser@lekha.ai",
            "password": "testpassword123"
        }
        
        response = requests.post(
            "http://localhost:5000/api/register",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_user),
            timeout=10
        )
        
        print(f"\n🔐 Registration Test:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code in [201, 409]:  # 201 = created, 409 = already exists
            return True
        return False
        
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

def test_api_login():
    """Test user login via API"""
    try:
        test_user = {
            "email": "testuser@lekha.ai",
            "password": "testpassword123"
        }
        
        response = requests.post(
            "http://localhost:5000/api/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_user),
            timeout=10
        )
        
        print(f"\n🔑 Login Test:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

def main():
    print("🔍 Database Connection Test for lekha.ai")
    print("=" * 50)
    
    # Test direct database connection
    db_success = test_direct_db_connection()
    
    if db_success:
        # Test API endpoints
        reg_success = test_api_registration()
        login_success = test_api_login()
        
        print(f"\n📊 Test Results:")
        print(f"Database Connection: {'✅ Pass' if db_success else '❌ Fail'}")
        print(f"User Registration: {'✅ Pass' if reg_success else '❌ Fail'}")
        print(f"User Login: {'✅ Pass' if login_success else '❌ Fail'}")
        
        if db_success and reg_success and login_success:
            print(f"\n🎉 All tests passed! Your lekha.ai application is connected to MySQL!")
        else:
            print(f"\n⚠️  Some tests failed. Check the errors above.")
    else:
        print(f"\n❌ Database connection failed. Please check MySQL server and credentials.")

if __name__ == "__main__":
    main()