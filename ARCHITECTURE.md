# 🏗️ Strava World Map - Architecture & How It Works

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      STRAVA API                              │
│              (Your Activities & GPS Data)                    │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/OAuth
┌─────────────────────────────────────────────────────────────┐
│                   PYTHON SCRIPTS                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  authenticate.py                                     │    │
│  │  - OAuth 2.0 flow                                   │    │
│  │  - Gets access tokens                               │    │
│  │  - Saves to .env                                    │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  fetch_activities.py                                │    │
│  │  - Fetches ALL activities                           │    │
│  │  - Decodes GPS polylines                            │    │
│  │  - Saves to activities.json                         │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  sync_activities.py                                 │    │
│  │  - Fetches NEW activities only                      │    │
│  │  - Updates activities.json                          │    │
│  │  - Respects rate limits                             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓ Writes
┌─────────────────────────────────────────────────────────────┐
│                  activities.json                             │
│  [                                                           │
│    {                                                         │
│      "id": 123,                                              │
│      "name": "Morning Run",                                  │
│      "type": "Run",                                          │
│      "distance": 5000,                                       │
│      "coordinates": [[lat, lng], [lat, lng], ...]           │
│    },                                                        │
│    ...                                                       │
│  ]                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓ Reads
┌─────────────────────────────────────────────────────────────┐
│                   WEB INTERFACE                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  index.html + JavaScript + Leaflet.js              │    │
│  │  - Loads activities.json                            │    │
│  │  - Renders map with CartoDB tiles                   │    │
│  │  - Draws polylines for each activity                │    │
│  │  - Shows statistics & filters                       │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓ Displays
┌─────────────────────────────────────────────────────────────┐
│                    YOUR BROWSER                              │
│  🗺️  Interactive World Map with All Your Routes             │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Authentication Flow

```
You → authenticate.py → Strava OAuth → Browser Authorization
                                              ↓
                                        Auth Code
                                              ↓
     .env ← Access Token ← authenticate.py ← Strava
```

### 2. Initial Data Fetch

```
fetch_activities.py → Strava API → All Activities
         ↓
    For each activity:
         ↓
    Get GPS Polyline → Decode to Coordinates
         ↓
    activities.json (saved locally)
```

### 3. Ongoing Sync

```
sync_activities.py → Check latest activity date
         ↓
    Strava API → New activities since last sync
         ↓
    Merge with existing → Update activities.json
```

### 4. Visualization

```
Browser → Load index.html
    ↓
Load activities.json
    ↓
For each activity with GPS:
    ↓
Draw colored polyline on map (Leaflet.js)
    ↓
Add popup with activity details
    ↓
Calculate & display statistics
```

---

## File Purposes

| File | Purpose |
|------|---------|
| `.env` | Stores your Strava API credentials and tokens (SECRET!) |
| `.env.example` | Template showing what credentials you need |
| `.gitignore` | Protects secrets from being committed to Git |
| `requirements.txt` | Python package dependencies |
| `authenticate.py` | Handles OAuth flow with Strava |
| `fetch_activities.py` | Downloads all your activities (first run) |
| `sync_activities.py` | Updates with new activities (ongoing) |
| `activities.json` | Local database of your activities + GPS data |
| `index.html` | Web interface with map visualization |
| `server.py` | Optional local web server |
| `check_setup.py` | Verifies your setup is correct |

---

## Key Technologies

### Backend (Python)
- **stravalib**: Official Strava API client
- **polyline**: Decodes Google's polyline format to coordinates
- **python-dotenv**: Loads environment variables from .env

### Frontend (JavaScript)
- **Leaflet.js**: Open-source interactive maps library
- **CartoDB**: Beautiful map tile provider
- **Vanilla JavaScript**: No framework needed!

### Data Format
- **JSON**: Simple, human-readable data storage
- **Polyline Encoding**: Compressed GPS coordinate format

---

## API Rate Limits

Strava enforces these limits:
- **100 requests per 15 minutes**
- **1,000 requests per day**

Our scripts handle this by:
- Adding small delays between requests (0.1 seconds)
- Syncing only new activities (not re-fetching everything)
- Using summary polylines (lower detail but faster)

---

## Security & Privacy

✅ **Everything runs locally** - No external servers  
✅ **Credentials in .env** - Not committed to Git  
✅ **No tracking** - No analytics or third-party services  
✅ **Open source** - You can see exactly what it does  

⚠️ **Be careful sharing** - Your map shows where you've been  
⚠️ **Activities.json** - Contains your personal activity data  
⚠️ **Home location** - Consider privacy zones in Strava settings  

---

## Performance

- **Initial fetch**: 2-10 minutes (depends on activity count)
- **Sync**: 30 seconds - 2 minutes (only new activities)
- **Map loading**: 1-5 seconds (depends on activity count)
- **Memory**: Minimal - activities.json is typically < 10MB

---

## Customization Points

Want to customize? Here's where to look:

| What to Change | Where to Look |
|----------------|---------------|
| Activity colors | `index.html` - `activityColors` object |
| Map style | `index.html` - Leaflet tile layer URL |
| Statistics shown | `index.html` - `stat-grid` section |
| Data fetched | `fetch_activities.py` - activity_dict |
| Rate limiting | `fetch_activities.py` - `time.sleep()` calls |
| OAuth scopes | `authenticate.py` - `scope` parameter |

---

## Workflow Summary

### First Time Setup (Do Once)
```bash
1. Get API credentials from Strava
2. cp .env.example .env  # Create config file
3. Edit .env             # Add credentials
4. python authenticate.py     # Get tokens
5. python fetch_activities.py # Download all data
6. open index.html       # View your map!
```

### Regular Updates (Weekly/After Workouts)
```bash
1. python sync_activities.py  # Get new activities
2. Refresh browser            # See updates
```

---

## Troubleshooting Guide

| Problem | Solution |
|---------|----------|
| No .env file | `cp .env.example .env` |
| Missing credentials | Add to .env from Strava API settings |
| Auth error | Run `python authenticate.py` again |
| No activities.json | Run `python fetch_activities.py` |
| Map shows error | Check browser console (F12) |
| Rate limit hit | Wait 15 minutes and try again |
| No GPS data | Indoor activities don't have coordinates |

---

## What Makes This Special

1. **Fully Local** - No servers, no hosting, no costs
2. **Privacy First** - Your data never leaves your computer
3. **Beautiful** - Modern, dark-themed UI
4. **Fast** - Efficient data fetching and rendering
5. **Easy to Use** - Simple commands, clear instructions
6. **Customizable** - Open source, well-documented code
7. **Complete** - Authentication, fetching, syncing, visualization

---

## Future Enhancement Ideas

Want to take it further? Consider adding:

- 📅 Date range filters
- 📸 Photos from activities
- 🏆 Personal records highlights
- 📈 Charts and graphs
- 🌡️ Weather data integration
- 👥 Multi-athlete comparison
- 🎬 Animated timeline
- 💾 SQLite database option
- 🗓️ Calendar view
- 🏅 Achievement badges

All the code is well-structured and documented to make these additions easy!

---

**Happy Mapping! 🗺️**


