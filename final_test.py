#!/usr/bin/env python3
"""
Final comprehensive test for lekha.ai application
"""

import requests
import json
import mysql.connector
from mysql.connector import Error

def test_database_connectivity():
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
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"✅ Database: Connected ({user_count} users)")
            return True
    except Error as e:
        print(f"❌ Database: Failed - {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    results = {}
    
    # Test health
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        results['health'] = response.status_code == 200
        print(f"✅ API Health: Working" if results['health'] else f"❌ API Health: Failed")
    except:
        results['health'] = False
        print(f"❌ API Health: Failed")
    
    # Test main page
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        results['main_page'] = response.status_code == 200 and 'lekha.ai' in response.text
        print(f"✅ Main Page: Working (lekha.ai branding)" if results['main_page'] else f"❌ Main Page: Failed")
    except:
        results['main_page'] = False
        print(f"❌ Main Page: Failed")
    
    # Test user registration
    try:
        test_user = {"email": "final_test@lekha.ai", "password": "testpass123"}
        response = requests.post(f"{base_url}/api/register", 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(test_user), timeout=10)
        results['registration'] = response.status_code in [201, 409]
        print(f"✅ Registration: Working" if results['registration'] else f"❌ Registration: Failed")
    except:
        results['registration'] = False
        print(f"❌ Registration: Failed")
    
    # Test user login
    try:
        test_user = {"email": "final_test@lekha.ai", "password": "testpass123"}
        response = requests.post(f"{base_url}/api/login",
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(test_user), timeout=10)
        results['login'] = response.status_code == 200
        print(f"✅ Login: Working" if results['login'] else f"❌ Login: Failed")
    except:
        results['login'] = False
        print(f"❌ Login: Failed")
    
    return results

def test_branding():
    """Test that branding has been updated to lekha.ai"""
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        content = response.text.lower()
        
        has_lekha = 'lekha.ai' in content
        has_cleartenant = 'cleartenant' in content
        
        if has_lekha and not has_cleartenant:
            print("✅ Branding: Successfully updated to lekha.ai")
            return True
        elif has_cleartenant:
            print("⚠️  Branding: Still contains ClearTenant references")
            return False
        else:
            print("❌ Branding: No branding found")
            return False
    except:
        print("❌ Branding: Could not test")
        return False

def main():
    print("🔍 Final Test for lekha.ai Application")
    print("=" * 50)
    
    # Test database
    db_ok = test_database_connectivity()
    
    # Test API endpoints
    api_results = test_api_endpoints()
    
    # Test branding
    branding_ok = test_branding()
    
    # Summary
    print("\n📊 Final Test Results:")
    print("=" * 30)
    
    all_tests = [
        ("Database Connection", db_ok),
        ("API Health", api_results.get('health', False)),
        ("Main Page", api_results.get('main_page', False)),
        ("User Registration", api_results.get('registration', False)),
        ("User Login", api_results.get('login', False)),
        ("Branding Update", branding_ok)
    ]
    
    passed = sum(1 for _, result in all_tests if result)
    total = len(all_tests)
    
    for test_name, result in all_tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS! Your lekha.ai application is fully functional!")
        print("✅ Database connected to MySQL Workbench")
        print("✅ User registration/login working")
        print("✅ Branding updated to lekha.ai")
        print("✅ All API endpoints working")
        print("\n🚀 Your application is ready for use at: http://localhost:5000")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")

if __name__ == "__main__":
    main()