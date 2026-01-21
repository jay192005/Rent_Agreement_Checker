#!/usr/bin/env python3
"""
Inspect the current database structure
"""
import mysql.connector
from mysql.connector import Error

def inspect_database():
    """Inspect current database and table structure"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jay@2005',
            database='rent_agreements_db',
            port=3306
        )
        
        cursor = connection.cursor()
        
        print("🔍 Inspecting current database structure...")
        
        # Show all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Tables in database:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Show users table structure
        if ('users',) in tables:
            print(f"\n📋 'users' table structure:")
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            for column in columns:
                print(f"   {column[0]} - {column[1]} - {'NULL' if column[2] == 'YES' else 'NOT NULL'} - {column[3] if column[3] else ''}")
            
            # Show sample data
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"\n📊 Total users: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM users LIMIT 3")
                users = cursor.fetchall()
                print("📋 Sample users:")
                for user in users:
                    print(f"   {user}")
        
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    inspect_database()