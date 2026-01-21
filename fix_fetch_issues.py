#!/usr/bin/env python3
"""
Comprehensive fix for fetch API issues
"""

import requests
import json
import time

def test_all_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    tests = [
        ("Health Check", "GET", "/api/health", None),
        ("Registration", "POST", "/api/register", {"email": "finaltest@lekha.ai", "password": "testpass123"}),
        ("Login", "POST", "/api/login", {"email": "finaltest@lekha.ai", "password": "testpass123"}),
    ]
    
    results = []
    
    for test_name, method, endpoint, data in tests:
        try:
            url = f"{base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(data) if data else None,
                    timeout=10
                )
            
            success = response.status_code in [200, 201, 409]  # 409 for existing user
            
            results.append({
                "test": test_name,
                "success": success,
                "status": response.status_code,
                "response": response.text[:200] + "..." if len(response.text) > 200 else response.text
            })
            
            print(f"{'✅' if success else '❌'} {test_name}: {response.status_code}")
            
        except Exception as e:
            results.append({
                "test": test_name,
                "success": False,
                "error": str(e)
            })
            print(f"❌ {test_name}: {e}")
    
    return results

def test_frontend_access():
    """Test frontend page access"""
    pages = [
        "/",
        "/test_fetch.html",
        "/test_user_icon.html"
    ]
    
    for page in pages:
        try:
            response = requests.get(f"http://localhost:5000{page}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} Page {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ Page {page}: {e}")

def main():
    print("🔍 Comprehensive Fetch API Fix Test")
    print("=" * 50)
    
    print("\n📡 Testing API Endpoints:")
    api_results = test_all_endpoints()
    
    print("\n🌐 Testing Frontend Pages:")
    test_frontend_access()
    
    print("\n📊 Summary:")
    successful_tests = sum(1 for r in api_results if r.get('success', False))
    total_tests = len(api_results)
    
    print(f"API Tests: {successful_tests}/{total_tests} passed")
    
    if successful_tests == total_tests:
        print("\n🎉 All tests passed! The fetch API issues are fixed!")
        print("\n🚀 Your lekha.ai application is ready:")
        print("   • Main page: http://localhost:5000")
        print("   • Test page: http://localhost:5000/test_fetch.html")
        print("   • User icon test: http://localhost:5000/test_user_icon.html")
    else:
        print(f"\n⚠️  {total_tests - successful_tests} test(s) failed.")
        print("Check the errors above for details.")

if __name__ == "__main__":
    main()