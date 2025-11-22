#!/usr/bin/env python3
"""
Simple HTTP server to view the Strava World Map.
Run this script and open http://localhost:8000 in your browser.
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if activities.json exists
    if not os.path.exists('activities.json'):
        print("\n" + "="*60)
        print("WARNING: activities.json not found!")
        print("="*60)
        print("\nPlease run 'python fetch_activities.py' first to download")
        print("your Strava activities before viewing the map.")
        print("\nServer will start anyway, but the map will show an error.")
        print("="*60 + "\n")
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\n" + "="*60)
        print("STRAVA WORLD MAP SERVER")
        print("="*60)
        print(f"\n✓ Server running at: http://localhost:{PORT}")
        print(f"✓ Open this URL in your browser to view your map")
        print(f"\nPress Ctrl+C to stop the server\n")
        print("="*60 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("Server stopped. Thanks for using Strava World Map!")
            print("="*60 + "\n")
            sys.exit(0)

if __name__ == '__main__':
    main()

