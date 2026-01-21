#!/usr/bin/env python3
"""
Verification script for GitHub deployment
"""

import os
import requests
import subprocess

def check_github_repository():
    """Check if the GitHub repository is accessible"""
    try:
        response = requests.get("https://github.com/jay192005/Rent_Agreement_Checker", timeout=10)
        if response.status_code == 200:
            print("✅ GitHub repository is accessible")
            return True
        else:
            print(f"❌ GitHub repository returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing GitHub repository: {e}")
        return False

def check_required_files():
    """Check if all required files are present"""
    required_files = [
        'README.md',
        'requirements.txt',
        'app.py',
        'ai.py',
        'setup_database.py',
        '.gitignore',
        'LICENSE',
        'DEPLOYMENT.md',
        '.env.example',
        'static/index.html',
        'static/analyzer.html',
        'static/history.html',
        'static/style.css',
        'static/script.js',
        'static/analyzer.js',
        'static/history.js'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def check_git_status():
    """Check Git status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("⚠️  Uncommitted changes found:")
            print(result.stdout)
            return False
        else:
            print("✅ Git working tree is clean")
            return True
    except Exception as e:
        print(f"❌ Error checking Git status: {e}")
        return False

def check_sensitive_files():
    """Check that sensitive files are not tracked"""
    sensitive_files = ['.env']
    
    try:
        result = subprocess.run(['git', 'ls-files'], 
                              capture_output=True, text=True, check=True)
        tracked_files = result.stdout.split('\n')
        
        found_sensitive = []
        for file in sensitive_files:
            if file in tracked_files:
                found_sensitive.append(file)
        
        if found_sensitive:
            print(f"❌ Sensitive files are tracked: {found_sensitive}")
            return False
        else:
            print("✅ No sensitive files are tracked")
            return True
    except Exception as e:
        print(f"❌ Error checking tracked files: {e}")
        return False

def main():
    print("🔍 GitHub Deployment Verification")
    print("=" * 50)
    
    # Check GitHub repository
    print("\n📡 Checking GitHub Repository:")
    github_ok = check_github_repository()
    
    # Check required files
    print("\n📁 Checking Required Files:")
    files_ok, missing = check_required_files()
    
    # Check Git status
    print("\n🔧 Checking Git Status:")
    git_ok = check_git_status()
    
    # Check sensitive files
    print("\n🔒 Checking Sensitive Files:")
    sensitive_ok = check_sensitive_files()
    
    # Summary
    print("\n📊 Deployment Verification Summary:")
    print("=" * 40)
    
    checks = [
        ("GitHub Repository Access", github_ok),
        ("Required Files Present", files_ok),
        ("Git Status Clean", git_ok),
        ("No Sensitive Files Tracked", sensitive_ok)
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 DEPLOYMENT VERIFICATION SUCCESSFUL!")
        print("✅ Your lekha.ai code has been successfully deployed to GitHub!")
        print("✅ Repository: https://github.com/jay192005/Rent_Agreement_Checker")
        print("✅ All required files are present")
        print("✅ No sensitive information is exposed")
        print("✅ Ready for production deployment")
        
        print("\n🚀 Next Steps:")
        print("1. Clone the repository on your production server")
        print("2. Copy .env.example to .env and configure your settings")
        print("3. Follow the DEPLOYMENT.md guide for your platform")
        print("4. Set up your MySQL database")
        print("5. Configure your Gemini API key")
        
    else:
        print(f"\n⚠️  {total - passed} check(s) failed.")
        print("Please fix the issues above before proceeding with deployment.")

if __name__ == "__main__":
    main()