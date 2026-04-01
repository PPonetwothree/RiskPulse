# RiskPulse Intelligence Dashboard v1.0

A geopolitical intelligence system dashboard sporting a highly detailed, immersive, modernized intelligence terminal interface. 
This application simulates a multi-agent system (Collector, Analyzer, Forecaster, Alert Manager) operating in real-time to monitor global risk metrics, utilizing entirely custom retro UI elements and charts.

## Features
- **Live Event Feed**: Simulated real-time ingestion from GDELT, ACLED, and social media signals.
- **Sentiment Analysis**: Tracks shifting political stability across tracked countries.
- **Forecast Engine**: Visualizes 7-day risk forecasting utilizing ensemble models.
- **Active Alerts**: Automatically triggers visual and auditory warnings upon detecting sudden risk spikes.
- **Interactive UI**: Fully functional draggable windows, drop-down menus, modally-rendered dialogs, and a responsive toolbar.

## Architecture & Hosting

This version has been specially configured as a **Static Frontend Simulation** and requires absolutely zero backend, making it perfectly suited for free-tier CDN hosts like Netlify, Vercel, or GitHub Pages.

Because standard static hosts cannot natively run continuous background Python agents or persistent SQLite databases (which the original prototype used), the former Flask backend `app.py` has been deactivated. All dynamic logic has been carefully migrated into `static/js/dashboard.js`, where a local simulation loop authentically mimics the original Server-Sent Events (SSE) data stream.

## Deployment to Netlify

Deploying this dashboard is literally a 1-click process since it requires no build commands.

1. Fork or push this repository to your GitHub account.
2. In the Netlify dashboard, click **Add new site** -> **Import an existing project**.
3. Select this repository.
4. Leave the "Build command" and "Publish directory" fields completely blank (Netlify will default to serving the root `index.html` directory).
5. Click **Deploy Site**.

You will have a live, hyper-authentic geopolitical dashboard running instantly.

## Local Development
To run this locally, you do not need Python or any dependencies. Simply serve the folder over a local web server. For example:

```bash
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000` in your browser.
