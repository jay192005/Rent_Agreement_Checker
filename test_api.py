#!/usr/bin/env python3
"""
Simple test script to verify API endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_registration():
    """Test user registration"""
    try:
        test_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/register",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        print(f"Registration Test: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code in [201, 409]  # 201 = created, 409 = already exists
    except Exception as e:
        print(f"Registration test failed: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        test_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        print(f"Login Test: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Login test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    if test_health():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
    
    print("-" * 30)
    
    # Test registration
    if test_registration():
        print("✅ Registration test passed")
    else:
        print("❌ Registration test failed")
    
    print("-" * 30)
    
    # Test login
    if test_login():
        print("✅ Login test passed")
    else:
        print("❌ Login test failed")
    
    print("=" * 50)
    print("API testing complete!")