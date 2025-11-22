#!/usr/bin/env python3
"""
Sync Strava Activities
This script syncs new activities from Strava to your local database.
Run this periodically to keep your map up to date.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import polyline
import time

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_existing_activities():
    """Load existing activities from JSON file."""
    if os.path.exists('activities.json'):
        with open('activities.json', 'r') as f:
            return json.load(f)
    return []

def get_latest_activity_date(activities):
    """Get the date of the most recent activity."""
    if not activities:
        return None
    
    dates = [datetime.fromisoformat(a['start_date'].replace('Z', '+00:00')) 
             for a in activities if a.get('start_date')]
    return max(dates) if dates else None

def sync_activities():
    """Sync new activities from Strava."""
    load_dotenv()
    
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    access_token = os.getenv('STRAVA_ACCESS_TOKEN')
    
    if not all([client_id, client_secret, access_token]):
        print("ERROR: Missing credentials. Please run authenticate.py first.")
        return
    
    print("\n" + "="*60)
    print("SYNCING STRAVA ACTIVITIES")
    print("="*60)
    
    # Load existing activities
    existing_activities = load_existing_activities()
    existing_ids = {a['id'] for a in existing_activities}
    
    print(f"\nExisting activities: {len(existing_activities)}")
    
    latest_date = get_latest_activity_date(existing_activities)
    if latest_date:
        print(f"Latest activity: {latest_date.strftime('%Y-%m-%d')}")
        after_timestamp = int(latest_date.timestamp())
    else:
        print("No existing activities found. Fetching all activities...")
        after_timestamp = None
    
    new_activities = []
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        page = 1
        per_page = 50
        
        print("\nFetching new activities...")
        
        while True:
            # Build params
            params = {
                'page': page,
                'per_page': per_page
            }
            if after_timestamp:
                params['after'] = after_timestamp
            
            # Fetch activities page
            response = requests.get(
                'https://www.strava.com/api/v3/athlete/activities',
                headers=headers,
                params=params,
                verify=False
            )
            response.raise_for_status()
            activities = response.json()
            
            if not activities:
                break  # No more activities
            
            print(f"  Processing page {page} ({len(activities)} activities)...")
            
            for activity in activities:
                activity_id = activity['id']
                
                # Skip if we already have this
                if activity_id in existing_ids:
                    continue
                
                try:
                    # Get detailed activity
                    detail_response = requests.get(
                        f'https://www.strava.com/api/v3/activities/{activity_id}',
                        headers=headers,
                        verify=False
                    )
                    detail_response.raise_for_status()
                    detailed = detail_response.json()
                    
                    activity_dict = {
                        'id': activity_id,
                        'name': activity.get('name', ''),
                        'type': activity.get('type', ''),
                        'sport_type': activity.get('sport_type', activity.get('type', '')),
                        'start_date': activity.get('start_date', ''),
                        'distance': float(activity.get('distance', 0)),
                        'moving_time': int(activity.get('moving_time', 0)),
                        'elapsed_time': int(activity.get('elapsed_time', 0)),
                        'total_elevation_gain': float(activity.get('total_elevation_gain', 0)),
                        'start_latlng': activity.get('start_latlng'),
                        'end_latlng': activity.get('end_latlng'),
                        'location_city': activity.get('location_city'),
                        'location_state': activity.get('location_state'),
                        'location_country': activity.get('location_country'),
                        'map_polyline': None,
                        'coordinates': []
                    }
                    
                    # Get polyline
                    if detailed.get('map') and detailed['map'].get('polyline'):
                        polyline_str = detailed['map']['polyline']
                        activity_dict['map_polyline'] = polyline_str
                        try:
                            coords = polyline.decode(polyline_str)
                            activity_dict['coordinates'] = coords
                        except:
                            pass
                    
                    new_activities.append(activity_dict)
                    print(f"  ✓ Synced: {activity.get('name', 'Unknown')} ({activity.get('type', 'Unknown')})")
                    
                    # Delay to respect rate limits
                    time.sleep(0.15)
                    
                except Exception as e:
                    if '429' in str(e):
                        print(f"\n⚠️  Rate limit reached!")
                        print(f"   Synced {len(new_activities)} new activities so far.")
                        print(f"   Wait 15-20 minutes and run this script again to get more.")
                        break
                    else:
                        print(f"  Warning: Could not fetch details for activity {activity_id}: {e}")
                        continue
            
            # Check if we hit rate limit
            if '429' in str(response.status_code):
                break
            
            page += 1
            time.sleep(0.5)
        
        if new_activities:
            # Merge with existing
            all_activities = existing_activities + new_activities
            
            # Sort by date (newest first)
            all_activities.sort(key=lambda x: x.get('start_date', ''), reverse=True)
            
            # Save to file
            with open('activities.json', 'w') as f:
                json.dump(all_activities, f, indent=2)
            
            print(f"\n✓ Synced {len(new_activities)} new activities")
            print(f"✓ Total activities: {len(all_activities)}")
            
            new_with_gps = sum(1 for a in new_activities if a['coordinates'])
            print(f"✓ New activities with GPS data: {new_with_gps}/{len(new_activities)}")
        else:
            print("\n✓ No new activities to sync. You're up to date!")
        
    except Exception as e:
        if '429' in str(e):
            print(f"\n⚠️  Rate limit reached!")
            if new_activities:
                # Save what we got
                all_activities = existing_activities + new_activities
                all_activities.sort(key=lambda x: x.get('start_date', ''), reverse=True)
                with open('activities.json', 'w') as f:
                    json.dump(all_activities, f, indent=2)
                print(f"   Saved {len(new_activities)} new activities.")
            print(f"   Wait 15-20 minutes and run this script again to get more.")
        else:
            print(f"\nERROR: {e}")
            print("\nIf you're getting an authorization error, try running authenticate.py again.")

if __name__ == '__main__':
    sync_activities()
