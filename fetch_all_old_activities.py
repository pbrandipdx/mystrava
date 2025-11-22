#!/usr/bin/env python3
"""
Fetch ALL Strava Activities (including older ones)
This script fetches ALL your activities, handling rate limits gracefully.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv
import polyline

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_all_activities():
    """Fetch all activities from Strava, handling rate limits."""
    load_dotenv()
    
    access_token = os.getenv('STRAVA_ACCESS_TOKEN')
    
    if not access_token:
        print("ERROR: Missing access token. Please run authenticate.py first.")
        return
    
    print("\n" + "="*60)
    print("FETCHING ALL STRAVA ACTIVITIES")
    print("="*60)
    
    # Load existing activities
    existing_activities = []
    if os.path.exists('activities.json'):
        with open('activities.json', 'r') as f:
            existing_activities = json.load(f)
    
    existing_ids = {a['id'] for a in existing_activities}
    print(f"\nExisting activities in database: {len(existing_activities)}")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    all_activities = list(existing_activities)  # Start with existing
    new_count = 0
    
    try:
        page = 1
        per_page = 50
        
        print("\nFetching activities from Strava...")
        print("(This respects rate limits - if hit, progress will be saved)\n")
        
        while True:
            try:
                params = {
                    'page': page,
                    'per_page': per_page
                }
                
                response = requests.get(
                    'https://www.strava.com/api/v3/athlete/activities',
                    headers=headers,
                    params=params,
                    verify=False
                )
                response.raise_for_status()
                activities = response.json()
                
                if not activities:
                    print(f"\n✓ Reached end of activities (page {page})")
                    break
                
                print(f"Page {page}: Found {len(activities)} activities...")
                
                for activity in activities:
                    activity_id = activity['id']
                    
                    # Skip if we already have it
                    if activity_id in existing_ids:
                        continue
                    
                    try:
                        # Get detailed activity with polyline
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
                        
                        all_activities.append(activity_dict)
                        existing_ids.add(activity_id)
                        new_count += 1
                        
                        if new_count % 10 == 0:
                            print(f"  ... {new_count} new activities fetched")
                        
                        # Delay to respect rate limits
                        time.sleep(0.15)
                        
                    except requests.exceptions.HTTPError as e:
                        if '429' in str(e):
                            raise e  # Re-raise to catch in outer block
                        print(f"  Warning: Could not fetch activity {activity_id}: {e}")
                        continue
                
                page += 1
                time.sleep(0.5)
                
            except requests.exceptions.HTTPError as e:
                if '429' in str(e):
                    print(f"\n⚠️  RATE LIMIT REACHED")
                    print(f"   Progress: {new_count} new activities fetched")
                    print(f"   Saving progress...")
                    
                    # Save what we have
                    all_activities.sort(key=lambda x: x.get('start_date', ''), reverse=True)
                    with open('activities.json', 'w') as f:
                        json.dump(all_activities, f, indent=2)
                    
                    print(f"   ✓ Saved {len(all_activities)} total activities")
                    print(f"\n   📋 TO CONTINUE:")
                    print(f"   1. Wait 15-20 minutes")
                    print(f"   2. Run this script again: python fetch_all_old_activities.py")
                    print(f"   3. It will continue from where it left off")
                    return
                else:
                    raise e
        
        # Save final result
        all_activities.sort(key=lambda x: x.get('start_date', ''), reverse=True)
        with open('activities.json', 'w') as f:
            json.dump(all_activities, f, indent=2)
        
        print(f"\n" + "="*60)
        print("SUCCESS! ALL ACTIVITIES FETCHED")
        print("="*60)
        print(f"\n✓ Total activities: {len(all_activities)}")
        print(f"✓ New activities fetched: {new_count}")
        
        with_gps = sum(1 for a in all_activities if a.get('coordinates'))
        print(f"✓ Activities with GPS data: {with_gps}/{len(all_activities)}")
        
        # Show date range
        dates = [a['start_date'] for a in all_activities if a.get('start_date')]
        if dates:
            print(f"\n📅 Date range:")
            print(f"   Oldest: {min(dates)[:10]}")
            print(f"   Newest: {max(dates)[:10]}")
        
        print(f"\n🗺️  Refresh your browser to see all activities on the map!")
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == '__main__':
    fetch_all_activities()


