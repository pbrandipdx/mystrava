#!/usr/bin/env python3
"""
Fetch Strava Activities
This script fetches all your Strava activities and saves them to a JSON file.
"""

import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import polyline

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_activities():
    """Fetch all activities from Strava using direct API calls."""
    load_dotenv()
    
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    access_token = os.getenv('STRAVA_ACCESS_TOKEN')
    
    if not all([client_id, client_secret, access_token]):
        print("ERROR: Missing credentials. Please run authenticate.py first.")
        return
    
    print("\n" + "="*60)
    print("FETCHING STRAVA ACTIVITIES")
    print("="*60)
    
    # Get athlete info first
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        athlete_response = requests.get(
            'https://www.strava.com/api/v3/athlete',
            headers=headers,
            verify=False
        )
        athlete_response.raise_for_status()
        athlete = athlete_response.json()
        print(f"\nAthlete: {athlete.get('firstname', '')} {athlete.get('lastname', '')}")
    except Exception as e:
        print(f"ERROR: Could not get athlete info: {e}")
        return
    
    print("\nFetching activities... (this may take a while)")
    
    activities_data = []
    page = 1
    per_page = 50
    
    while True:
        try:
            # Fetch activities page by page
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
                break  # No more activities
            
            print(f"  Fetching page {page} ({len(activities)} activities)...")
            
            for activity in activities:
                try:
                    activity_id = activity['id']
                    
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
                    
                    # Get polyline from map
                    if detailed.get('map') and detailed['map'].get('polyline'):
                        polyline_str = detailed['map']['polyline']
                        activity_dict['map_polyline'] = polyline_str
                        
                        try:
                            coords = polyline.decode(polyline_str)
                            activity_dict['coordinates'] = coords
                        except:
                            pass
                    
                    activities_data.append(activity_dict)
                    
                    # Small delay to respect rate limits
                    time.sleep(0.15)
                    
                except Exception as e:
                    print(f"  Warning: Could not fetch details for activity {activity.get('id')}: {e}")
                    continue
            
            page += 1
            
            # Small delay between pages
            time.sleep(0.5)
            
        except Exception as e:
            print(f"\nERROR: {e}")
            break
    
    print(f"\n✓ Successfully fetched {len(activities_data)} activities")
    
    # Save to JSON file
    output_file = 'activities.json'
    with open(output_file, 'w') as f:
        json.dump(activities_data, f, indent=2)
    
    print(f"✓ Saved activities to {output_file}")
    
    # Print statistics
    print("\n" + "="*60)
    print("STATISTICS")
    print("="*60)
    
    total_distance = sum(a['distance'] for a in activities_data)
    total_time = sum(a['moving_time'] for a in activities_data)
    
    activity_types = {}
    for a in activities_data:
        sport_type = a['sport_type'] or a['type']
        activity_types[sport_type] = activity_types.get(sport_type, 0) + 1
    
    print(f"\nTotal Activities: {len(activities_data)}")
    print(f"Total Distance: {total_distance/1000:.2f} km")
    print(f"Total Time: {total_time/3600:.2f} hours")
    print(f"\nActivities by type:")
    for sport_type, count in sorted(activity_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sport_type}: {count}")
    
    activities_with_map = sum(1 for a in activities_data if a['coordinates'])
    print(f"\nActivities with GPS data: {activities_with_map}/{len(activities_data)}")
    
    print("\n✓ All done! Now open index.html to see your map!")

if __name__ == '__main__':
    fetch_activities()
