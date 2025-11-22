# ⚡ Quick Start: Auto-Sync Your Strava Map

## Choose Your Method

### 🖥️ Option 1: Local Automation (Easiest)
**Your Mac syncs daily**

```bash
cd /Users/PBRAN4/strava-world-map
./setup-auto-sync.sh
```

That's it! Answer 2 questions and you're done.

---

### ☁️ Option 2: Cloud Automation (No Mac needed)
**GitHub syncs daily in the cloud**

1. Push to GitHub
2. Add Strava secrets to repo settings
3. Enable GitHub Pages or connect Netlify
4. Done!

---

## What Happens After Setup?

Every day:
1. New Strava activities are fetched
2. Your `activities.json` is updated
3. Your hosted map is automatically updated
4. Nothing for you to do! 🎉

---

## Test It Now

```bash
cd /Users/PBRAN4/strava-world-map
./auto-sync-and-deploy.sh
```

You should see: ✅ Sync completed!

---

## Manage Auto-Sync

```bash
# Check status
launchctl list | grep stravamap

# View logs
cat /Users/PBRAN4/strava-world-map/sync-logs/output.log

# Stop auto-sync
launchctl unload ~/Library/LaunchAgents/com.stravamap.autosync.plist

# Start auto-sync
launchctl load ~/Library/LaunchAgents/com.stravamap.autosync.plist
```

---

## 📖 Full Guides

- **AUTOMATION-SETUP.md** - Compare methods & choose
- **AUTO-SYNC-GUIDE.md** - Complete setup & troubleshooting
- **READY-TO-DEPLOY.md** - Hosting your site

---

**That's all! Your Strava map is now fully automated.** 🚀

