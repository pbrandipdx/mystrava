#!/usr/bin/env python3
"""
Strava OAuth Authentication Script
This script helps you authenticate with Strava and get your access tokens.
"""

import os
import webbrowser
import requests
from stravalib.client import Client
from dotenv import load_dotenv

# Disable SSL verification warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def authenticate():
    """
    Authenticate with Strava API and get access token.
    """
    load_dotenv()
    
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("ERROR: Please set STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET in .env file")
        print("\nSteps to get your credentials:")
        print("1. Go to https://www.strava.com/settings/api")
        print("2. Create an application (if you haven't already)")
        print("3. Copy your Client ID and Client Secret")
        print("4. Create a .env file based on .env.example")
        return
    
    client = Client()
    
    # Authorization URL
    authorize_url = client.authorization_url(
        client_id=client_id,
        redirect_uri='http://localhost:8000/authorized',
        scope=['read_all', 'activity:read_all', 'profile:read_all']
    )
    
    print("\n" + "="*60)
    print("STRAVA AUTHENTICATION")
    print("="*60)
    print("\nOpening browser for Strava authorization...")
    print("If browser doesn't open, go to this URL:")
    print(f"\n{authorize_url}\n")
    
    # Open browser
    webbrowser.open(authorize_url)
    
    print("\nAfter authorizing, you'll be redirected to a URL like:")
    print("http://localhost:8000/authorized?code=XXXXX&scope=...")
    print("\nCopy the 'code' parameter from that URL and paste it here:")
    
    auth_code = input("\nEnter authorization code: ").strip()
    
    try:
        # Exchange authorization code for access token using direct requests
        # to avoid SSL certificate issues
        token_url = 'https://www.strava.com/oauth/token'
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(token_url, data=payload, verify=False)
        response.raise_for_status()
        token_response = response.json()
        
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']
        expires_at = token_response['expires_at']
        
        print("\n" + "="*60)
        print("SUCCESS! Authentication complete.")
        print("="*60)
        print("\nAdd these to your .env file:")
        print(f"STRAVA_ACCESS_TOKEN={access_token}")
        print(f"STRAVA_REFRESH_TOKEN={refresh_token}")
        print("\nYour access token will expire, but the script will automatically")
        print("refresh it using your refresh token when needed.")
        
        # Update .env file automatically
        update_env_file(access_token, refresh_token)
        
    except Exception as e:
        print(f"\nERROR: Authentication failed: {e}")
        print("Please try again and make sure you copied the code correctly.")

def update_env_file(access_token, refresh_token):
    """Update .env file with new tokens."""
    env_path = '.env'
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        updated = False
        with open(env_path, 'w') as f:
            for line in lines:
                if line.startswith('STRAVA_ACCESS_TOKEN='):
                    f.write(f'STRAVA_ACCESS_TOKEN={access_token}\n')
                    updated = True
                elif line.startswith('STRAVA_REFRESH_TOKEN='):
                    f.write(f'STRAVA_REFRESH_TOKEN={refresh_token}\n')
                else:
                    f.write(line)
            
            if not updated:
                f.write(f'\nSTRAVA_ACCESS_TOKEN={access_token}\n')
                f.write(f'STRAVA_REFRESH_TOKEN={refresh_token}\n')
        
        print(f"\n✓ Updated {env_path} with your tokens")
    else:
        with open(env_path, 'w') as f:
            f.write(f'STRAVA_CLIENT_ID={os.getenv("STRAVA_CLIENT_ID")}\n')
            f.write(f'STRAVA_CLIENT_SECRET={os.getenv("STRAVA_CLIENT_SECRET")}\n')
            f.write(f'STRAVA_ACCESS_TOKEN={access_token}\n')
            f.write(f'STRAVA_REFRESH_TOKEN={refresh_token}\n')
        
        print(f"\n✓ Created {env_path} with your credentials")

if __name__ == '__main__':
    authenticate()

