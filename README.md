# Strava World Map Visualization 🌍

A beautiful one-page website that visualizes all your Strava activities on an interactive world map. See everywhere you've run, biked, and worked out!

![Strava World Map](https://img.shields.io/badge/Strava-FC5200?style=for-the-badge&logo=strava&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white)

## Features ✨

- **Interactive World Map**: See all your activities plotted on a beautiful dark-themed world map
- **Activity Filtering**: Filter by activity type (running, cycling, swimming, etc.)
- **Statistics Dashboard**: View total distance, time, elevation, and activity counts
- **Activity Details**: Click on any route to see detailed information
- **Heatmap Mode**: Toggle between individual routes and heatmap visualization
- **Auto-Sync**: Easy script to keep your map updated with new activities

## Screenshots

The map displays:
- All your GPS-tracked activities as colored polylines
- Different colors for different activity types (runs, rides, walks, etc.)
- Interactive popups with activity details
- Real-time statistics about your athletic journey

## Setup Instructions 🚀

### 1. Prerequisites

- Python 3.7 or higher
- A Strava account
- Your activity data on Strava

### 2. Get Strava API Credentials

1. Go to [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Create a new application:
   - **Application Name**: "My World Map" (or whatever you prefer)
   - **Category**: "Visualizer"
   - **Club**: Leave blank
   - **Website**: `http://localhost` (or your actual website)
   - **Authorization Callback Domain**: `localhost`
3. After creating, you'll see your **Client ID** and **Client Secret**
4. Copy these - you'll need them in the next step

### 3. Install Dependencies

```bash
cd strava-world-map

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Your Credentials

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Strava credentials:

```
STRAVA_CLIENT_ID=your_client_id_here
STRAVA_CLIENT_SECRET=your_client_secret_here
```

### 5. Authenticate with Strava

Run the authentication script:

```bash
python authenticate.py
```

This will:
1. Open your browser to authorize the application
2. Ask you to copy the authorization code
3. Exchange it for access tokens
4. Automatically save the tokens to your `.env` file

### 6. Fetch Your Activities

Download all your Strava activities:

```bash
python fetch_activities.py
```

This will:
- Fetch all your activities from Strava
- Download GPS data for each activity
- Save everything to `activities.json`
- Show you statistics about your activities

**Note**: This may take a few minutes if you have many activities. The script respects Strava's rate limits.

### 7. View Your Map

Open `index.html` in your web browser:

```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html
```

Or simply drag and drop `index.html` into your browser.

## Usage 🗺️

### Interactive Map Features

- **Pan & Zoom**: Use mouse/trackpad to explore the map
- **Activity Details**: Click on any route to see activity information
- **Fit to Activities**: Button to zoom out and see all your activities
- **Toggle Heatmap**: Switch between individual routes and heatmap view
- **Filter by Type**: Check/uncheck activity types to show/hide them

### Keeping Your Map Updated

To sync new activities:

```bash
python sync_activities.py
```

This will:
- Check for new activities since your last sync
- Download only the new activities
- Update your `activities.json` file
- Refresh your browser to see the updates

You can run this as often as you like - daily, weekly, or after each workout!

## File Structure 📁

```
strava-world-map/
├── authenticate.py        # Strava OAuth authentication
├── fetch_activities.py    # Initial data fetch
├── sync_activities.py     # Sync new activities
├── index.html            # Main visualization page
├── activities.json       # Your activities data (generated)
├── requirements.txt      # Python dependencies
├── .env                  # Your credentials (do not commit!)
├── .env.example          # Template for .env
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Customization 🎨

### Change Activity Colors

Edit the `activityColors` object in `index.html`:

```javascript
const activityColors = {
    'Run': '#fc5200',        // Orange (Strava's color)
    'Ride': '#00d4ff',       // Cyan
    'Walk': '#ffa500',       // Orange
    // Add more types as needed
};
```

### Change Map Style

In `index.html`, replace the tile layer URL with another provider:

```javascript
// Current: Dark theme
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', ...)

// Alternative: Light theme
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', ...)

// Alternative: Satellite
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', ...)
```

## Troubleshooting 🔧

### "Could not load activities.json"

Make sure you've run `fetch_activities.py` first to download your activities.

### "Authorization error"

Your access token may have expired. Run `authenticate.py` again to get a new token.

### "No activities with GPS data"

Some activities (like gym workouts) don't have GPS coordinates. Only activities with GPS tracks will appear on the map.

### Rate Limit Errors

Strava has rate limits (100 requests per 15 minutes, 1000 per day). If you hit the limit, wait and try again later. The scripts include delays to help avoid this.

## Privacy & Security 🔒

- Your `.env` file contains sensitive credentials - never commit it to Git
- The `activities.json` file contains your personal workout data
- This runs entirely locally - no data is sent to any external servers
- Only share your map publicly if you're comfortable sharing your workout locations

## Contributing 🤝

Feel free to customize this project for your needs! Some ideas:

- Add filters for date ranges
- Show statistics by year or month
- Add elevation profiles
- Create animations showing your activities over time
- Add photos from activities
- Compare different time periods

## Credits & Technologies

- **Strava API**: For providing access to activity data
- **Leaflet.js**: For the interactive map
- **stravalib**: Python library for Strava API
- **CartoDB**: For the beautiful dark map tiles

## License

MIT License - feel free to use and modify as you wish!

## Support

If you encounter issues:
1. Check that your `.env` file is configured correctly
2. Make sure you've run all the setup steps in order
3. Check the Strava API documentation: https://developers.strava.com/

---

**Enjoy exploring your athletic journey! 🏃‍♂️🚴‍♀️🏊‍♂️**

