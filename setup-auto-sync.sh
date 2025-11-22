#!/bin/bash
# Setup automatic daily Strava sync
# This will configure your Mac to automatically sync and deploy your Strava data every day

echo "================================"
echo "STRAVA AUTO-SYNC SETUP"
echo "================================"
echo ""
echo "This will set up automatic daily syncing of your Strava activities."
echo ""

# Get the project directory
PROJECT_DIR="/Users/PBRAN4/strava-world-map"

# Ask user what time they want to run the sync
echo "⏰ What time should the sync run daily?"
echo "   (Enter hour in 24-hour format, e.g., 6 for 6 AM, 18 for 6 PM)"
read -p "Hour (0-23): " SYNC_HOUR

if [ -z "$SYNC_HOUR" ] || [ "$SYNC_HOUR" -lt 0 ] || [ "$SYNC_HOUR" -gt 23 ]; then
    echo "❌ Invalid hour. Please enter a number between 0 and 23."
    exit 1
fi

echo ""
echo "📋 Choose your deployment method:"
echo "   1) Netlify CLI (automated deployment)"
echo "   2) Vercel CLI (automated deployment)"
echo "   3) GitHub Pages (automated git push)"
echo "   4) Manual (sync only, you upload manually)"
echo ""
read -p "Choose (1-4): " DEPLOY_CHOICE

case $DEPLOY_CHOICE in
    1)
        DEPLOY_METHOD="netlify-cli"
        echo ""
        echo "📦 Installing Netlify CLI..."
        echo "   Run: npm install -g netlify-cli"
        echo "   Then run: netlify login"
        echo "   Then run: netlify link (in your project directory)"
        ;;
    2)
        DEPLOY_METHOD="vercel-cli"
        echo ""
        echo "📦 Installing Vercel CLI..."
        echo "   Run: npm install -g vercel"
        echo "   Then run: vercel login"
        echo "   Then run: vercel link (in your project directory)"
        ;;
    3)
        DEPLOY_METHOD="github"
        echo ""
        echo "📦 Make sure you have:"
        echo "   - Git repository initialized"
        echo "   - Remote 'origin' configured"
        echo "   - SSH keys or credentials set up"
        ;;
    4)
        DEPLOY_METHOD="manual"
        echo ""
        echo "📝 Manual mode: You'll upload activities.json yourself after each sync"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Save deployment config
echo "DEPLOY_METHOD=\"$DEPLOY_METHOD\"" > "$PROJECT_DIR/.deploy-config"

# Create launchd plist for macOS
PLIST_NAME="com.stravamap.autosync"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

echo ""
echo "📝 Creating launch agent..."

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PROJECT_DIR/auto-sync-and-deploy.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>$SYNC_HOUR</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/sync-logs/output.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/sync-logs/error.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# Create logs directory
mkdir -p "$PROJECT_DIR/sync-logs"

# Load the launch agent
echo "🚀 Loading launch agent..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo ""
echo "================================"
echo "✅ AUTO-SYNC CONFIGURED!"
echo "================================"
echo ""
echo "⏰ Your Strava map will sync daily at ${SYNC_HOUR}:00"
echo "📝 Logs will be saved to: $PROJECT_DIR/sync-logs/"
echo ""
echo "📋 Useful commands:"
echo "   • Test sync now:     ./auto-sync-and-deploy.sh"
echo "   • Check status:      launchctl list | grep stravamap"
echo "   • View logs:         cat sync-logs/output.log"
echo "   • Stop auto-sync:    launchctl unload ~/Library/LaunchAgents/$PLIST_NAME.plist"
echo "   • Start auto-sync:   launchctl load ~/Library/LaunchAgents/$PLIST_NAME.plist"
echo ""
echo "🎉 You're all set!"
echo ""

