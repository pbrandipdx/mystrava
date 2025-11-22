# Deployment Guide - Strava World Map

Your Strava World Map is ready to be hosted online! This is a static website that can be deployed to various hosting platforms.

## 📦 What You Need to Deploy

Only 2 files are needed for deployment:
1. `index.html` - Your main web page
2. `activities.json` - Your Strava activities data

## 🌐 Hosting Options

### Option 1: GitHub Pages (FREE & Easy)

**Best for:** Quick deployment, version control

**Steps:**
1. Create a new GitHub repository
2. Upload only these files:
   - `index.html`
   - `activities.json`
3. Go to Settings → Pages
4. Select "Deploy from a branch" → main branch → root
5. Your site will be live at: `https://yourusername.github.io/repo-name`

**Note:** Your activities will be PUBLIC. If privacy is a concern, see Option 4.

### Option 2: Netlify (FREE & Easy)

**Best for:** Simple drag-and-drop deployment

**Steps:**
1. Go to [netlify.com](https://netlify.com) and sign up (free)
2. Click "Add new site" → "Deploy manually"
3. Drag and drop a folder containing:
   - `index.html`
   - `activities.json`
4. Your site goes live instantly with a free subdomain

**To update:** Just re-sync your Strava data locally and drag-drop the new `activities.json`

### Option 3: Vercel (FREE & Easy)

**Best for:** Fast global CDN, great performance

**Steps:**
1. Go to [vercel.com](https://vercel.com) and sign up (free)
2. Click "Add New" → "Project"
3. Upload your folder or connect to GitHub
4. Deploy - your site goes live instantly

### Option 4: Password-Protected (Netlify with Auth)

**Best for:** Keeping your activities private

**Steps:**
1. Deploy to Netlify (see Option 2)
2. Go to Site settings → Access control
3. Enable "Visitor access control" with password protection
4. Share the password only with people you want to see your map

### Option 5: Custom Domain

**Available on:** Netlify, Vercel, GitHub Pages (all free tiers)

**Steps:**
1. Deploy to any platform above
2. Buy a domain (e.g., from Namecheap, Google Domains)
3. In your hosting platform settings, add your custom domain
4. Update your domain's DNS records as instructed
5. Your site will be live at: `https://yourdomain.com`

## 🔄 Updating Your Map with New Activities

When you have new Strava activities:

1. **Sync locally:**
   ```bash
   cd /Users/PBRAN4/strava-world-map
   source venv/bin/activate
   python sync_activities.py
   ```

2. **Re-deploy:**
   - **GitHub Pages:** Commit and push the updated `activities.json`
   - **Netlify/Vercel:** Drag-drop the new `activities.json` or push to GitHub (if connected)

## 🔒 Privacy & Security

### What's Safe to Share:
- ✅ `index.html` - Your visualization code
- ✅ `activities.json` - Contains GPS routes and activity stats

### Keep Private (DON'T upload):
- ❌ `.env` - Contains your API credentials
- ❌ Python scripts - Only needed for syncing locally
- ❌ `venv/` folder - Python dependencies

### Privacy Considerations:

Your `activities.json` file contains:
- GPS coordinates of your routes
- Activity names, dates, and times
- Locations where you exercise

**Recommendations:**
1. If you don't want your routes public, use password protection (Option 4)
2. You can edit `activities.json` to remove specific activities before deploying
3. Consider using privacy zones in Strava settings to hide your home/work addresses

## 📁 Deployment Package

I'll create a clean deployment folder for you with just the files you need.

## 🎨 Your Customizations

Your deployed site includes:
- ✅ Bright green heatmap visualization (default)
- ✅ Swim and Rowing activities removed
- ✅ Dark theme design
- ✅ Interactive map with filters
- ✅ Statistics dashboard

## 🚀 Quick Start - Netlify Deploy (Recommended)

The fastest way to get online:

1. Create a deployment folder:
   ```bash
   mkdir ~/strava-map-deploy
   cp /Users/PBRAN4/strava-world-map/index.html ~/strava-map-deploy/
   cp /Users/PBRAN4/strava-world-map/activities.json ~/strava-map-deploy/
   ```

2. Go to [netlify.com](https://app.netlify.com/drop)
3. Drag the `strava-map-deploy` folder onto the page
4. Done! Your map is live!

## 💡 Tips

- **Custom Name:** On Netlify/Vercel, you can customize your subdomain for free
- **HTTPS:** All these platforms provide free SSL certificates
- **CDN:** Your site will be fast globally with built-in CDN
- **Cost:** All these options are 100% FREE for static sites

## 🆘 Need Help?

- Check that both `index.html` and `activities.json` are in the same folder
- Make sure `activities.json` is valid JSON (it should be if sync worked)
- Test locally first: open `index.html` directly in your browser

---

Ready to deploy? Pick your favorite option above and go live in minutes! 🌍

