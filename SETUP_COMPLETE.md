# 🌍 Strava World Map - Setup Complete!

Your Strava World Map visualization project is ready to go! Here's everything that's been set up for you:

## 📁 Project Structure

```
strava-world-map/
├── .env.example          ← Template for your API credentials
├── .gitignore           ← Protects your secrets from Git
├── requirements.txt     ← Python dependencies
├── authenticate.py      ← OAuth authentication script
├── fetch_activities.py  ← Downloads all your Strava activities
├── sync_activities.py   ← Updates with new activities
├── server.py           ← Local web server (optional)
├── index.html          ← Beautiful map visualization
├── README.md           ← Full documentation
└── QUICKSTART.md       ← Fast 5-minute setup guide
```

## 🚀 Quick Start (5 Minutes)

### 1️⃣ Get Strava API Credentials (2 min)
Visit: **https://www.strava.com/settings/api**

Create an app with:
- **Application Name**: My World Map
- **Website**: `http://localhost`
- **Authorization Callback Domain**: `localhost`

Copy your **Client ID** and **Client Secret**

### 2️⃣ Install & Configure (1 min)

```bash
cd /Users/PBRAN4/strava-world-map

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up credentials
cp .env.example .env
# Edit .env and add your Client ID and Secret
```

### 3️⃣ Authenticate with Strava (1 min)

```bash
python authenticate.py
```

Follow the prompts to authorize the app. Your tokens will be saved automatically.

### 4️⃣ Download Your Activities (2-10 min)

```bash
python fetch_activities.py
```

This fetches all your activities with GPS data from Strava.

### 5️⃣ View Your Map! (5 sec)

**Option A - Simple:**
```bash
open index.html
```

**Option B - With Server (Recommended):**
```bash
python server.py
# Then open: http://localhost:8000
```

---

## ✨ Features

Your world map includes:

🗺️ **Interactive Map** - Pan, zoom, and explore all your activities  
🎨 **Color-Coded Routes** - Different colors for runs, rides, walks, etc.  
📊 **Live Statistics** - Total distance, time, elevation, activity counts  
🔍 **Activity Details** - Click any route to see details  
🎛️ **Filters** - Show/hide activity types  
🔥 **Heatmap Mode** - Toggle between individual routes and heatmap  
🔄 **Auto-Sync** - Easy updates with new activities  

---

## 🔄 Keeping Your Map Updated

After each workout (or weekly/monthly):

```bash
python sync_activities.py
```

This downloads only new activities and updates your map!

---

## 🎨 What You'll See

The map displays:
- **Orange** = Runs 🏃
- **Cyan** = Rides 🚴
- **Green** = Hikes 🥾
- **Blue** = Swims 🏊
- **Purple** = Weight Training 💪
- And more!

All plotted on a beautiful dark-themed world map with:
- Statistics dashboard
- Activity type breakdown
- Interactive popups with details
- Zoom to fit all activities button

---

## 🛠️ Technology Stack

- **Backend**: Python 3.7+ with stravalib
- **Frontend**: Leaflet.js for mapping
- **Data**: JSON storage (all local, no external servers)
- **Maps**: CartoDB dark theme tiles

---

## 📝 Important Notes

✅ **Privacy**: Everything runs locally. No data sent to external servers  
✅ **Security**: `.env` is in `.gitignore` to protect your credentials  
✅ **Rate Limits**: Scripts include delays to respect Strava's API limits  
✅ **GPS Data**: Only activities with GPS tracks appear on the map  

---

## 🆘 Troubleshooting

**"Could not load activities.json"**  
→ Run `python fetch_activities.py` first

**"Authorization error"**  
→ Run `python authenticate.py` again to refresh tokens

**"No activities on map"**  
→ Indoor activities don't have GPS. Only outdoor tracked activities show up

**Rate limit hit**  
→ Wait 15 minutes and try again. Strava limits: 100 req/15min, 1000/day

---

## 🎯 Next Steps

1. **Get your API credentials** from Strava
2. **Run the Quick Start** steps above
3. **View your amazing map!**
4. **Share screenshots** (without revealing private locations if concerned)

For detailed documentation, see `README.md`  
For fastest setup, see `QUICKSTART.md`

---

## 🤝 Customization Ideas

Want to make it your own? Try:
- Change map themes (satellite, light, terrain)
- Modify activity colors
- Add date range filters
- Show photos from activities
- Create animations over time
- Compare year-over-year

All code is well-commented and easy to customize!

---

**Enjoy exploring your athletic journey! 🏃‍♂️🚴‍♀️🏊‍♂️🏋️‍♀️**

Need help? Check the README.md or the Strava API docs: https://developers.strava.com/


