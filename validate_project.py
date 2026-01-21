#!/usr/bin/env python3
"""
Project validation script to check for errors and issues
"""

import os
import json
import requests
from pathlib import Path

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def check_javascript_syntax(filepath):
    """Basic JavaScript syntax check"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic checks
        issues = []
        
        # Check for common syntax issues
        if content.count('{') != content.count('}'):
            issues.append("Mismatched curly braces")
        
        if content.count('(') != content.count(')'):
            issues.append("Mismatched parentheses")
        
        if content.count('[') != content.count(']'):
            issues.append("Mismatched square brackets")
        
        # Check for merge conflict markers
        if '<<<<<<' in content or '>>>>>>' in content or '======' in content:
            issues.append("Git merge conflict markers found")
        
        return issues
    except Exception as e:
        return [f"Error reading file: {e}"]

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    results = {}
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        results['health'] = {
            'status': response.status_code,
            'response': response.json() if response.status_code == 200 else response.text
        }
    except Exception as e:
        results['health'] = {'error': str(e)}
    
    # Test static file serving
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        results['static'] = {
            'status': response.status_code,
            'content_type': response.headers.get('content-type', 'unknown')
        }
    except Exception as e:
        results['static'] = {'error': str(e)}
    
    return results

def main():
    print("🔍 Project Validation Report")
    print("=" * 50)
    
    # Check critical files
    critical_files = [
        'app.py',
        'ai.py',
        '.env',
        'requirements.txt',
        'static/index.html',
        'static/analyzer.html',
        'static/history.html',
        'static/script.js',
        'static/analyzer.js',
        'static/history.js',
        'static/style.css',
        'static/analyzer.css'
    ]
    
    print("\n📁 File Existence Check:")
    missing_files = []
    for file in critical_files:
        if check_file_exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    # Check JavaScript files for syntax issues
    print("\n🔧 JavaScript Syntax Check:")
    js_files = [
        'static/script.js',
        'static/analyzer.js', 
        'static/history.js',
        'script.js',
        'analyzer.js',
        'history.js'
    ]
    
    js_issues = {}
    for js_file in js_files:
        if check_file_exists(js_file):
            issues = check_javascript_syntax(js_file)
            if issues:
                js_issues[js_file] = issues
                print(f"⚠️  {js_file}: {', '.join(issues)}")
            else:
                print(f"✅ {js_file}")
        else:
            print(f"⏭️  {js_file} - Not found (skipping)")
    
    # Test API endpoints
    print("\n🌐 API Endpoint Tests:")
    api_results = test_api_endpoints()
    
    for endpoint, result in api_results.items():
        if 'error' in result:
            print(f"❌ {endpoint}: {result['error']}")
        elif result.get('status') == 200:
            print(f"✅ {endpoint}: Working")
        else:
            print(f"⚠️  {endpoint}: Status {result.get('status', 'unknown')}")
    
    # Summary
    print("\n📊 Summary:")
    print(f"Missing files: {len(missing_files)}")
    print(f"JavaScript issues: {len(js_issues)}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
    
    if js_issues:
        print(f"\n⚠️  JavaScript files with issues:")
        for file, issues in js_issues.items():
            print(f"   - {file}: {', '.join(issues)}")
    
    if not missing_files and not js_issues:
        print("\n🎉 All checks passed! Your project looks good.")
    else:
        print(f"\n⚠️  Found {len(missing_files) + len(js_issues)} issues that need attention.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()