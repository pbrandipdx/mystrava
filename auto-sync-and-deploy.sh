#!/bin/bash
# Auto-sync Strava activities and deploy to hosting
# This script syncs your latest Strava data and automatically updates your hosted site

set -e  # Exit on error

echo "================================"
echo "STRAVA MAP AUTO-SYNC & DEPLOY"
echo "================================"
echo ""

# Change to the project directory
cd /Users/PBRAN4/strava-world-map

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Sync new Strava activities
echo ""
echo "🏃 Syncing new Strava activities..."
python sync_activities.py

# Check if sync was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Sync completed successfully!"
    
    # Check which hosting method is being used
    if [ -f ".deploy-config" ]; then
        source .deploy-config
        
        case $DEPLOY_METHOD in
            "netlify-cli")
                echo ""
                echo "🚀 Deploying to Netlify..."
                netlify deploy --prod --dir=.
                ;;
            "vercel-cli")
                echo ""
                echo "🚀 Deploying to Vercel..."
                vercel --prod
                ;;
            "github")
                echo ""
                echo "🚀 Pushing to GitHub..."
                git add activities.json
                git commit -m "Auto-update: Strava activities $(date +%Y-%m-%d)"
                git push origin main
                ;;
            *)
                echo ""
                echo "⚠️  No deployment method configured."
                echo "📝 Updated activities.json - manually upload to your hosting platform"
                ;;
        esac
    else
        echo ""
        echo "📝 activities.json updated!"
        echo "📤 Manual step: Upload the new activities.json to your hosting platform"
        echo ""
        echo "Or configure auto-deploy by running: ./setup-auto-deploy.sh"
    fi
    
    echo ""
    echo "================================"
    echo "✅ Done!"
    echo "================================"
else
    echo ""
    echo "❌ Sync failed. Check the error messages above."
    exit 1
fi

