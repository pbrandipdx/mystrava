# 🔄 Automated Daily Strava Sync & Deploy

## Overview

I've created scripts to automatically sync your Strava data every day and deploy updates to your hosted site!

## 🎯 What You Get

- ✅ **Automatic daily syncing** of new Strava activities
- ✅ **Automatic deployment** to your hosting platform
- ✅ **Runs in the background** on your Mac
- ✅ **Logs** for tracking what happened
- ✅ **No manual work needed!**

## 🚀 Quick Setup (5 minutes)

### Step 1: Run the Setup Script

```bash
cd /Users/PBRAN4/strava-world-map
./setup-auto-sync.sh
```

The script will ask you:
1. **What time to run?** (e.g., 6 for 6 AM, 18 for 6 PM)
2. **Which hosting platform?** (Netlify, Vercel, GitHub, or Manual)

### Step 2: Configure Your Hosting

#### Option A: Netlify CLI (Recommended for automation)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Link your site (run in project directory)
cd /Users/PBRAN4/strava-world-map
netlify link
```

Now your site auto-deploys daily!

#### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Link your site
cd /Users/PBRAN4/strava-world-map
vercel link
```

#### Option C: GitHub Pages

```bash
# Initialize git (if not already done)
cd /Users/PBRAN4/strava-world-map
git init
git add index.html activities.json
git commit -m "Initial commit"

# Add your GitHub repo as remote
git remote add origin https://github.com/yourusername/strava-map.git
git push -u origin main
```

Enable GitHub Pages in your repo settings.

#### Option D: Manual

The script will sync your data daily. You'll get a notification to manually upload `activities.json` to your hosting platform.

## 📋 How It Works

Every day at your chosen time:

1. **Syncs** new activities from Strava API
2. **Updates** your `activities.json` file
3. **Deploys** to your hosting platform automatically
4. **Logs** the results

All while you sleep! 😴

## 🧪 Test It Now

Before waiting for the daily schedule, test it:

```bash
cd /Users/PBRAN4/strava-world-map
./auto-sync-and-deploy.sh
```

You should see:
- ✅ Sync completed
- ✅ Deployment started (if configured)
- ✅ Success message

## 📊 Check Logs

View what happened during syncs:

```bash
# See output logs
cat /Users/PBRAN4/strava-world-map/sync-logs/output.log

# See error logs (if any)
cat /Users/PBRAN4/strava-world-map/sync-logs/error.log
```

## ⚙️ Management Commands

### Check if auto-sync is running:
```bash
launchctl list | grep stravamap
```

### Stop auto-sync:
```bash
launchctl unload ~/Library/LaunchAgents/com.stravamap.autosync.plist
```

### Start auto-sync:
```bash
launchctl load ~/Library/LaunchAgents/com.stravamap.autosync.plist
```

### Run sync manually anytime:
```bash
cd /Users/PBRAN4/strava-world-map
./auto-sync-and-deploy.sh
```

### Change the schedule:
```bash
# Edit the plist file
nano ~/Library/LaunchAgents/com.stravamap.autosync.plist

# Look for <key>Hour</key> and change the hour
# Then reload:
launchctl unload ~/Library/LaunchAgents/com.stravamap.autosync.plist
launchctl load ~/Library/LaunchAgents/com.stravamap.autosync.plist
```

## 🔒 Requirements

### Your Mac Needs to Be:
- ✅ **Powered on** at the scheduled time
- ✅ **Connected to internet**
- ❌ Doesn't need to be unlocked (runs in background)

### Tips:
- Schedule it for a time your Mac is usually on (morning/evening)
- Enable "Wake for network access" in System Preferences → Battery
- The script is fast (~30 seconds) so it won't slow down your Mac

## 🌐 Alternative: Cloud-Based Automation (Optional)

If you don't want to keep your Mac on, you can use GitHub Actions:

### GitHub Actions Setup

1. Push your project to GitHub
2. Add your Strava credentials as GitHub Secrets:
   - `STRAVA_CLIENT_ID`
   - `STRAVA_CLIENT_SECRET`
   - `STRAVA_ACCESS_TOKEN`
   - `STRAVA_REFRESH_TOKEN`

3. Create `.github/workflows/sync-strava.yml`:

```yaml
name: Sync Strava Activities

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:  # Allow manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Create .env file
        run: |
          echo "STRAVA_CLIENT_ID=${{ secrets.STRAVA_CLIENT_ID }}" >> .env
          echo "STRAVA_CLIENT_SECRET=${{ secrets.STRAVA_CLIENT_SECRET }}" >> .env
          echo "STRAVA_ACCESS_TOKEN=${{ secrets.STRAVA_ACCESS_TOKEN }}" >> .env
          echo "STRAVA_REFRESH_TOKEN=${{ secrets.STRAVA_REFRESH_TOKEN }}" >> .env
      
      - name: Sync activities
        run: python sync_activities.py
      
      - name: Commit and push if changed
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add activities.json
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto-update: Strava activities $(date)" && git push)
```

This runs in the cloud - no need for your Mac to be on!

## 📱 Notifications (Optional)

Want to get notified when sync happens? Add this to your `auto-sync-and-deploy.sh`:

```bash
# At the end of the script, add:
osascript -e 'display notification "Strava map updated!" with title "Strava Sync"'
```

Or use a service like [Healthchecks.io](https://healthchecks.io) for monitoring.

## ❓ Troubleshooting

### Sync isn't running?
```bash
# Check if launch agent is loaded
launchctl list | grep stravamap

# Check logs for errors
cat sync-logs/error.log
```

### Authentication errors?
Your Strava token expired. Re-authenticate:
```bash
cd /Users/PBRAN4/strava-world-map
source venv/bin/activate
python authenticate.py
```

### Deployment not working?
Make sure CLI is installed and linked:
```bash
# For Netlify
netlify status

# For Vercel
vercel whoami
```

## 🎉 You're All Set!

Your Strava map will now:
- ✅ **Sync automatically** every day
- ✅ **Deploy automatically** to your hosting
- ✅ **Stay up-to-date** without any manual work
- ✅ **Just keep logging activities** and they'll appear on your map!

---

**Next Steps:**
1. Run `./setup-auto-sync.sh` to configure
2. Test with `./auto-sync-and-deploy.sh`
3. Forget about it! It's automatic now! 🎊

