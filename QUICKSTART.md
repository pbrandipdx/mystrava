# Quick Start Guide 🚀

Get your Strava World Map up and running in 5 minutes!

## Step 1: Get Strava API Credentials (2 minutes)

1. Go to **https://www.strava.com/settings/api**
2. Click **"Create an App"** (or use an existing one)
3. Fill in the form:
   - **Application Name**: My World Map
   - **Category**: Visualizer  
   - **Club**: (leave blank)
   - **Website**: `http://localhost`
   - **Authorization Callback Domain**: `localhost`
4. Click **"Create"**
5. Copy your **Client ID** and **Client Secret**

## Step 2: Install Dependencies (1 minute)

```bash
cd strava-world-map

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 3: Configure Credentials (30 seconds)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
# Replace your_client_id_here and your_client_secret_here
```

Your `.env` file should look like:
```
STRAVA_CLIENT_ID=12345
STRAVA_CLIENT_SECRET=abcdef1234567890
```

## Step 4: Authenticate (1 minute)

```bash
python authenticate.py
```

- A browser window will open
- Click **"Authorize"** to allow access to your Strava data
- Copy the code from the URL and paste it back in the terminal
- Done! Your tokens are saved automatically

## Step 5: Fetch Your Activities (2-10 minutes depending on activity count)

```bash
python fetch_activities.py
```

This downloads all your Strava activities with GPS data.

## Step 6: View Your Map! (5 seconds)

**Option A: Simple (just open the file)**
```bash
open index.html  # macOS
# or drag index.html into your browser
```

**Option B: With a local server (recommended)**
```bash
python server.py
```
Then open: **http://localhost:8000**

---

## That's It! 🎉

You should now see your beautiful world map with all your activities!

## Keep Your Map Updated

Run this command after each workout (or weekly/monthly):

```bash
python sync_activities.py
```

---

## Troubleshooting

**"Could not load activities.json"**
- Make sure you ran `fetch_activities.py` first

**"Authorization error"**  
- Run `authenticate.py` again to get a fresh token

**"No activities with GPS data"**
- Indoor activities (treadmill, gym) don't have GPS
- Only outdoor activities with location tracking will show on the map

**Need help?**
- Check the full README.md for more details
- Verify your .env file has the correct credentials
