# 🤖 Automated Strava Sync - Choose Your Method

I've set up **automatic daily syncing** for your Strava World Map! Choose the method that works best for you:

## 🖥️ Method 1: Local Automation (Mac stays on)

**Best for:** If your Mac is usually on at a specific time each day

### Setup (2 minutes):
```bash
cd /Users/PBRAN4/strava-world-map
./setup-auto-sync.sh
```

**What it does:**
- Syncs new Strava data every day at your chosen time
- Automatically deploys to your hosting platform
- Runs in the background on your Mac

**Pros:**
- ✅ Simple setup
- ✅ Private (no cloud services)
- ✅ Fast and reliable

**Cons:**
- ❌ Mac needs to be on and connected to internet

📖 **Full guide:** Read `AUTO-SYNC-GUIDE.md`

---

## ☁️ Method 2: Cloud Automation (GitHub Actions)

**Best for:** If your Mac isn't always on, or you want "set it and forget it"

### Setup (5 minutes):

1. **Push to GitHub:**
   ```bash
   cd /Users/PBRAN4/strava-world-map
   git init
   git add index.html activities.json .github/workflows/sync-strava.yml requirements.txt sync_activities.py
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/strava-map.git
   git push -u origin main
   ```

2. **Add Secrets to GitHub:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `STRAVA_CLIENT_ID` (from your `.env` file)
     - `STRAVA_CLIENT_SECRET` (from your `.env` file)
     - `STRAVA_ACCESS_TOKEN` (from your `.env` file)
     - `STRAVA_REFRESH_TOKEN` (from your `.env` file)

3. **Enable GitHub Pages** (if using GitHub for hosting):
   - Go to Settings → Pages
   - Source: Deploy from branch `main`

4. **Optional - Add Netlify deployment:**
   - Add these secrets to GitHub:
     - `NETLIFY_AUTH_TOKEN` (from Netlify account settings)
     - `NETLIFY_SITE_ID` (from your Netlify site settings)

**What it does:**
- Runs every day at 6 AM UTC (customizable)
- Syncs new activities
- Commits to GitHub
- Auto-deploys to GitHub Pages or Netlify

**Pros:**
- ✅ Works even when Mac is off
- ✅ Free (GitHub Actions is free for public repos)
- ✅ Runs in the cloud
- ✅ Can manually trigger from GitHub UI

**Cons:**
- ❌ Requires GitHub account
- ❌ Your Strava credentials stored as GitHub Secrets

---

## 🎯 Comparison

| Feature | Local (Mac) | Cloud (GitHub) |
|---------|-------------|----------------|
| **Setup Time** | 2 minutes | 5 minutes |
| **Mac needs to be on?** | Yes | No |
| **Cost** | Free | Free |
| **Privacy** | More private | Credentials in GitHub |
| **Reliability** | If Mac is on | Always runs |
| **Manual trigger** | Run script | Click button in GitHub |

---

## 🔄 How Often Does It Sync?

**Default:** Once per day at your chosen time

**Want more frequent?** Edit the schedule:

**Local (Mac):**
- Edit: `~/Library/LaunchAgents/com.stravamap.autosync.plist`
- Change the `Hour` value or add multiple runs

**Cloud (GitHub):**
- Edit: `.github/workflows/sync-strava.yml`
- Change the cron schedule (e.g., `0 */6 * * *` for every 6 hours)

---

## 📱 Test Your Setup

### Local:
```bash
cd /Users/PBRAN4/strava-world-map
./auto-sync-and-deploy.sh
```

### Cloud:
- Go to your GitHub repo → Actions tab
- Click "Daily Strava Sync" → "Run workflow"

---

## 🎉 Once Set Up

You're done! Your map will:
1. ✅ Sync automatically every day
2. ✅ Pull new activities from Strava
3. ✅ Update your hosted website
4. ✅ Show your latest runs, rides, and walks

**Just keep logging activities on Strava - they'll appear on your map automatically!** 🏃‍♂️🗺️

---

## 📋 Files Created

- `auto-sync-and-deploy.sh` - Main sync & deploy script
- `setup-auto-sync.sh` - Interactive setup for local automation
- `.github/workflows/sync-strava.yml` - GitHub Actions workflow
- `AUTO-SYNC-GUIDE.md` - Detailed guide with troubleshooting
- `.deploy-config` - Stores your deployment method (created during setup)
- `sync-logs/` - Logs from automated runs (local only)

---

## 🆘 Need Help?

**Check logs:**
```bash
# Local
cat /Users/PBRAN4/strava-world-map/sync-logs/output.log

# Cloud
Go to GitHub repo → Actions → Click on a workflow run
```

**Full documentation:** See `AUTO-SYNC-GUIDE.md`

---

**Pick your method and get started! Both are fully automated after setup.** 🚀

