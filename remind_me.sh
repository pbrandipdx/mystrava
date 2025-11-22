#!/bin/bash
# Strava Data Pull Reminder
# This script waits 20 minutes then shows a notification and runs the fetch script

echo "⏰ Reminder set! I'll notify you in 20 minutes..."
echo "Starting at: $(date)"
echo ""

# Wait 20 minutes (1200 seconds)
sleep 1200

# Show notification
osascript -e 'display notification "Time to pull more Strava data! Run: python fetch_all_old_activities.py" with title "🗺️ Strava World Map" sound name "Glass"'

# Ask if you want to run it now
echo ""
echo "============================================================"
echo "⏰ TIME TO PULL MORE STRAVA DATA!"
echo "============================================================"
echo ""
echo "Run this command:"
echo "cd /Users/PBRAN4/strava-world-map && source venv/bin/activate && python fetch_all_old_activities.py"
echo ""


