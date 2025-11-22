#!/usr/bin/env python3
"""
Setup Checker
Verifies that your Strava World Map is properly configured.
"""

import os
import sys

def check_file(filename, required=True):
    """Check if a file exists."""
    exists = os.path.exists(filename)
    symbol = "✓" if exists else "✗"
    status = "Found" if exists else ("MISSING" if required else "Not found")
    print(f"  {symbol} {filename}: {status}")
    return exists

def check_env_var(var_name, required=True):
    """Check if an environment variable is set."""
    from dotenv import load_dotenv
    load_dotenv()
    value = os.getenv(var_name)
    is_set = value and value != f'your_{var_name.lower()}_here' and value.strip()
    symbol = "✓" if is_set else "✗"
    status = "Set" if is_set else ("NOT SET" if required else "Not set")
    print(f"  {symbol} {var_name}: {status}")
    return is_set

def main():
    print("\n" + "="*60)
    print("STRAVA WORLD MAP - SETUP CHECK")
    print("="*60)
    
    all_good = True
    
    # Check Python packages
    print("\n📦 Python Packages:")
    try:
        import stravalib
        print("  ✓ stravalib: Installed")
    except ImportError:
        print("  ✗ stravalib: NOT INSTALLED")
        print("    → Run: pip install -r requirements.txt")
        all_good = False
    
    try:
        import polyline
        print("  ✓ polyline: Installed")
    except ImportError:
        print("  ✗ polyline: NOT INSTALLED")
        print("    → Run: pip install -r requirements.txt")
        all_good = False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv: Installed")
    except ImportError:
        print("  ✗ python-dotenv: NOT INSTALLED")
        print("    → Run: pip install -r requirements.txt")
        all_good = False
    
    # Check required files
    print("\n📄 Required Files:")
    check_file("requirements.txt")
    check_file("authenticate.py")
    check_file("fetch_activities.py")
    check_file("sync_activities.py")
    check_file("index.html")
    check_file("server.py")
    
    # Check configuration
    print("\n⚙️  Configuration:")
    has_env = check_file(".env", required=False)
    
    if has_env:
        print("\n🔑 Credentials:")
        has_client_id = check_env_var("STRAVA_CLIENT_ID")
        has_client_secret = check_env_var("STRAVA_CLIENT_SECRET")
        has_access_token = check_env_var("STRAVA_ACCESS_TOKEN", required=False)
        
        if not has_client_id or not has_client_secret:
            print("\n  ⚠️  You need to set your Strava API credentials in .env")
            print("     Get them from: https://www.strava.com/settings/api")
            all_good = False
        elif not has_access_token:
            print("\n  ⚠️  You need to authenticate with Strava")
            print("     Run: python authenticate.py")
            all_good = False
    else:
        print("\n  ⚠️  No .env file found. Create one from .env.example")
        print("     Run: cp .env.example .env")
        print("     Then add your Strava API credentials")
        all_good = False
    
    # Check data
    print("\n📊 Data:")
    has_activities = check_file("activities.json", required=False)
    
    if not has_activities:
        print("\n  ℹ️  No activities data found yet")
        print("     Run: python fetch_activities.py")
    
    # Final verdict
    print("\n" + "="*60)
    if all_good and has_activities:
        print("✅ ALL SET! Your Strava World Map is ready!")
        print("\n   View your map:")
        print("   → python server.py")
        print("   → Open http://localhost:8000")
    elif all_good:
        print("⚠️  ALMOST READY! Just fetch your activities:")
        print("\n   Next step:")
        print("   → python fetch_activities.py")
    else:
        print("❌ SETUP INCOMPLETE")
        print("\n   Next steps:")
        if not has_env:
            print("   1. cp .env.example .env")
            print("   2. Add your Strava credentials to .env")
        print("   3. python authenticate.py")
        print("   4. python fetch_activities.py")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()


