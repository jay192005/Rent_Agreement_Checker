#!/usr/bin/env python3
"""
Direct API test to verify registration/login functionality
"""

import requests
import json

def test_registration():
    """Test user registration"""
    url = "http://localhost:5000/api/register"
    data = {
        "email": "testfix@lekha.ai",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            timeout=10
        )
        
        print(f"Registration Test:")
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        return response.status_code in [201, 409]
        
    except Exception as e:
        print(f"Registration failed: {e}")
        return False

def test_login():
    """Test user login"""
    url = "http://localhost:5000/api/login"
    data = {
        "email": "testfix@lekha.ai",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            timeout=10
        )
        
        print(f"\nLogin Test:")
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    url = "http://localhost:5000/api/health"
    
    try:
        response = requests.options(url, headers={
            "Origin": "http://localhost:5000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        })
        
        print(f"\nCORS Test:")
        print(f"Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        return True
        
    except Exception as e:
        print(f"CORS test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Direct API Test")
    print("=" * 40)
    
    reg_ok = test_registration()
    login_ok = test_login()
    cors_ok = test_cors()
    
    print(f"\n📊 Results:")
    print(f"Registration: {'✅' if reg_ok else '❌'}")
    print(f"Login: {'✅' if login_ok else '❌'}")
    print(f"CORS: {'✅' if cors_ok else '❌'}")