# RiskPulse Intelligence Dashboard - Complete Build Prompt

## Project Specification: Windows 98-Style Multi-Agent Geopolitical Intelligence Dashboard

### MISSION STATEMENT
Build a web-based geopolitical intelligence dashboard with a Windows 98 aesthetic that uses multiple specialized AI agents to collect, analyze, and present real-time conflict risk data. The dashboard must be minimal, functional, and reminiscent of 1990s-era intelligence software (Palantir-style) with no modern design flourishes.

---

## PART 1: VISUAL DESIGN SPECIFICATION (WINDOWS 98 THEME)

### Core Aesthetic Principles
```
1. BRUTALIST FUNCTIONALITY - Form follows function, zero decoration
2. GRID-BASED LAYOUT - Everything aligned to strict grid
3. SYSTEM FONTS - Only Arial, Courier New, MS Sans Serif
4. FLAT UI - No gradients, shadows, or 3D effects (except window chrome)
5. LIMITED PALETTE - Classic Windows 98 colors only
6. MONOSPACE DATA - All numeric data in Courier New
7. TERMINAL AESTHETIC - Black backgrounds for data panels
```

### Color Palette (STRICT)
```css
/* Windows 98 System Colors */
--win98-gray: #c0c0c0;           /* Window background */
--win98-title-active: #000080;   /* Active title bar (navy) */
--win98-title-inactive: #808080; /* Inactive title bar */
--win98-white: #ffffff;          /* Text on colored backgrounds */
--win98-black: #000000;          /* Primary text */
--win98-shadow-dark: #808080;    /* 3D shadow (dark) */
--win98-shadow-light: #ffffff;   /* 3D highlight */
--win98-button-face: #c0c0c0;    /* Button background */
--win98-menu-highlight: #000080; /* Selected menu item */

/* Intelligence Terminal Colors */
--terminal-bg: #000000;          /* Terminal background */
--terminal-green: #00ff00;       /* Success/normal data */
--terminal-amber: #ffcc00;       /* Warnings */
--terminal-red: #ff0000;         /* Alerts/critical */
--terminal-blue: #00ccff;        /* Info/headers */
--terminal-gray: #808080;        /* Dimmed text */

/* Status Colors */
--status-ok: #008000;            /* Green - normal */
--status-warning: #ff8c00;       /* Orange - elevated */
--status-alert: #ff0000;         /* Red - critical */
--status-unknown: #808080;       /* Gray - no data */
```

### Typography Rules
```css
/* System Fonts Only */
--font-system: 'MS Sans Serif', Arial, sans-serif;
--font-mono: 'Courier New', Courier, monospace;
--font-title: 'Arial', sans-serif;

/* Size Scale (8px based - Windows 98 standard) */
--text-xs: 8px;   /* Micro text */
--text-sm: 10px;  /* Small labels */
--text-md: 11px;  /* Body text */
--text-lg: 12px;  /* Headers */
--text-xl: 14px;  /* Title bars */
--text-2xl: 16px; /* Main titles */

/* All text must be pixel-perfect aligned to 8px baseline grid */
```

### UI Component Specifications

#### 1. Window Chrome (Top Bar)
```html
<div class="win98-window">
  <div class="win98-titlebar">
    <span class="win98-title">RISKPULSE INTELLIGENCE v1.0</span>
    <div class="win98-controls">
      <button class="win98-minimize">_</button>
      <button class="win98-maximize">□</button>
      <button class="win98-close">×</button>
    </div>
  </div>
  <div class="win98-menubar">
    <span class="menu-item">File</span>
    <span class="menu-item">View</span>
    <span class="menu-item">Agents</span>
    <span class="menu-item">Reports</span>
    <span class="menu-item">Help</span>
  </div>
  <div class="win98-toolbar">
    <!-- Toolbar buttons with icons -->
  </div>
</div>
```

#### 2. Data Panels (Terminal Style)
```html
<div class="terminal-panel">
  <div class="panel-header">
    <span class="panel-title">// LIVE EVENT FEED</span>
    <span class="panel-status">[ACTIVE]</span>
  </div>
  <div class="terminal-content">
    <div class="terminal-line">
      <span class="timestamp">[14:32:05]</span>
      <span class="severity severity-high">ALERT</span>
      <span class="location">SY-DAMASCUS</span>
      <span class="message">EVENT_SPIKE +320% Z-SCORE:3.2</span>
    </div>
  </div>
</div>
```

#### 3. Status Bar (Bottom)
```html
<div class="win98-statusbar">
  <span class="status-segment">GDELT: SYNCED [14:30:00]</span>
  <span class="status-segment">ACLED: OK</span>
  <span class="status-segment">AGENTS: 4/4 ACTIVE</span>
  <span class="status-segment">ALERTS: 3 CRITICAL</span>
  <span class="status-segment">14:32:15 UTC</span>
</div>
```

#### 4. Data Tables (Fixed-Width)
```
╔════════════════════════════════════════════════════════════════╗
║ COUNTRY │ EVENTS │ RISK │ ΔSENTIMENT │ FATALITIES │ FORECAST ║
╠════════════════════════════════════════════════════════════════╣
║ SY      │    245 │ 0.87 │     -0.42  │         23 │ ▲ HIGH   ║
║ UA      │    189 │ 0.78 │     -0.35  │         12 │ ▲ HIGH   ║
║ YE      │    156 │ 0.72 │     -0.28  │         18 │ ▲ MED    ║
║ IL      │    134 │ 0.65 │     -0.15  │          5 │ → MED    ║
╚════════════════════════════════════════════════════════════════╝
```

Use ASCII box-drawing characters: │ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼

#### 5. Charts (ASCII/Minimalist)
```
THREAT LEVEL TIMELINE (7 DAYS)
1.0 ┤                                      ●
    │                                    ●
0.8 ┤                              ●   ●
    │                        ●   ●
0.6 ┤                  ●   ●
    │            ●   ●
0.4 ┤      ●   ●
    │    ●
0.2 ┤  ●
    └────────────────────────────────────
    D-7  D-6  D-5  D-4  D-3  D-2  D-1  NOW
```

Or use simple canvas-based line charts with green phosphor effect.

### Layout Structure (Grid-Based)
```
┌─────────────────────────────────────────────────────────────────┐
│ [=] RISKPULSE INTELLIGENCE v1.0                        [_][□][×] │
├─────────────────────────────────────────────────────────────────┤
│ File  View  Agents  Reports  Help                               │
├─────────────────────────────────────────────────────────────────┤
│ [⟳] [▶] [⏸] [■] [⚙] [?]                                        │
├──────────────────────┬──────────────────────────────────────────┤
│ // LIVE EVENT FEED   │ // THREAT MAP                            │
│ [AGENT: COLLECTOR]   │ [AGENT: ANALYZER]                        │
│                      │                                          │
│ [14:32:05] ALERT SY  │  ┌──────────────────────────────┐       │
│ EVENT_SPIKE +320%    │  │      [WORLD MAP - ASCII]     │       │
│                      │  │   ● SY (0.87)  ● UA (0.78)   │       │
│ [14:31:42] HIGH UA   │  │   ● YE (0.72)  ● IL (0.65)   │       │
│ SENTIMENT_SHIFT -0.35│  └──────────────────────────────┘       │
│                      │                                          │
├──────────────────────┼──────────────────────────────────────────┤
│ // COUNTRY ANALYSIS  │ // FORECASTS                             │
│ [AGENT: SENTIMENT]   │ [AGENT: FORECASTER]                      │
│                      │                                          │
│ ┌──────────────────┐ │  SYRIA 7-DAY FORECAST:                  │
│ │ SY │ 245│0.87│-42││ │  D+1: 28  D+2: 32  D+3: 35              │
│ │ UA │ 189│0.78│-35││ │  D+4: 38  D+5: 40  D+6: 42              │
│ │ YE │ 156│0.72│-28││ │  D+7: 45  RISK: CRITICAL                │
│ └──────────────────┘ │                                          │
├──────────────────────┴──────────────────────────────────────────┤
│ GDELT:OK | ACLED:OK | AGENTS:4/4 | ALERTS:3 | 14:32:15 UTC    │
└─────────────────────────────────────────────────────────────────┘
```

---

## PART 2: MULTI-AGENT ARCHITECTURE

### Agent System Overview

The dashboard uses 4 specialized autonomous agents, each responsible for a specific domain. Agents run independently, communicate via message bus, and update shared state.

```
                    ┌─────────────────────┐
                    │   MESSAGE BUS       │
                    │   (Redis PubSub)    │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
    │ AGENT 1 │          │ AGENT 2 │          │ AGENT 3 │
    │COLLECTOR│          │ANALYZER │          │FORECAST │
    └────┬────┘          └────┬────┘          └────┬────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                        ┌──────▼────────┐
                        │  SHARED STATE │
                        │  (PostgreSQL) │
                        └───────────────┘
```

### Agent Definitions

#### AGENT 1: DATA COLLECTOR AGENT
```yaml
Name: "COLLECTOR-01"
Status Indicator: "● ACTIVE" (green) / "○ IDLE" (gray) / "✕ ERROR" (red)
Display Panel: "// LIVE EVENT FEED"
Responsibilities:
  - Fetch GDELT data every 15 minutes
  - Fetch ACLED data daily
  - Fetch Reddit posts hourly
  - Parse and normalize data
  - Store in database
  - Publish events to message bus

Workflow:
  1. SCHEDULE_TRIGGER → Start collection cycle
  2. API_FETCH → Download data from source
  3. PARSE_DATA → Extract relevant fields
  4. VALIDATE → Check data quality
  5. STORE → Insert into database
  6. PUBLISH_EVENT → Broadcast to message bus {"type": "new_events", "count": N}
  7. UPDATE_UI → Show latest events in feed panel
  8. SLEEP → Wait until next scheduled run

UI Display:
  - Scrolling terminal feed of collected events
  - Format: "[HH:MM:SS] SOURCE EVENT_TYPE LOCATION SUMMARY"
  - Color coding: GDELT (green), ACLED (amber), Reddit (blue)
  - Show collection metrics: "COLLECTED: 245 EVENTS | ERRORS: 0"

Agent Controls:
  - [▶ START] [⏸ PAUSE] [⟳ FORCE SYNC] [⚙ CONFIG]

Message Bus Events Published:
  - "collector.gdelt.complete" → {count, timestamp, errors}
  - "collector.acled.complete" → {count, timestamp, errors}
  - "collector.reddit.complete" → {count, timestamp, errors}
  - "collector.error" → {source, error_message}
```

#### AGENT 2: SENTIMENT ANALYZER AGENT
```yaml
Name: "ANALYZER-01"
Status Indicator: "● PROCESSING" / "○ IDLE" / "⧗ QUEUED"
Display Panel: "// SENTIMENT ANALYSIS"
Responsibilities:
  - Monitor message bus for new events
  - Load unprocessed content
  - Run BERT sentiment model
  - Calculate sentiment scores
  - Detect sentiment shifts
  - Trigger alerts on anomalies

Workflow:
  1. LISTEN → Wait for "new_events" message
  2. FETCH_UNPROCESSED → Load events without sentiment
  3. BATCH → Group into batches of 32
  4. LOAD_MODEL → Initialize BERT (cached)
  5. INFERENCE → Run sentiment classification
  6. CALCULATE_METRICS → Compute aggregates by country
  7. DETECT_SHIFTS → Compare to baseline
  8. STORE_RESULTS → Save sentiment scores
  9. CHECK_THRESHOLDS → If shift > 0.3, publish alert
  10. PUBLISH_EVENT → Broadcast results
  11. UPDATE_UI → Refresh sentiment display

UI Display:
  - Country sentiment table (sorted by shift magnitude)
  - Format: "COUNTRY | CURRENT | BASELINE | Δ | STATUS"
  - Visual indicator: ↑ (improving), ↓ (deteriorating), → (stable)
  - Processing status: "ANALYZING: 127 ITEMS | MODEL: BERT-SST2"

Agent Controls:
  - [▶ ANALYZE NOW] [⏸ PAUSE] [🔄 RETRAIN] [📊 STATS]

Message Bus Events Published:
  - "analyzer.sentiment.complete" → {countries_analyzed, shifts_detected}
  - "analyzer.alert.shift" → {country, shift_value, severity}
  - "analyzer.error" → {error_type, details}

Message Bus Events Subscribed:
  - "collector.*.complete" → Triggers analysis
```

#### AGENT 3: FORECASTING AGENT
```yaml
Name: "FORECASTER-01"
Status Indicator: "● TRAINING" / "● PREDICTING" / "○ IDLE"
Display Panel: "// FORECASTS & PREDICTIONS"
Responsibilities:
  - Prepare time-series data
  - Run ARIMA/Prophet/LSTM models
  - Generate 7-day forecasts
  - Calculate risk scores
  - Trigger high-risk alerts
  - Retrain models weekly

Workflow:
  1. SCHEDULE_TRIGGER → Daily at 00:00 UTC
  2. FETCH_HISTORY → Load 90 days of event counts
  3. PREPARE_SERIES → Aggregate by country/day
  4. MODEL_ARIMA → Train and forecast
  5. MODEL_PROPHET → Train and forecast
  6. MODEL_LSTM → Train and forecast
  7. ENSEMBLE → Weighted average (30/30/40)
  8. CALCULATE_RISK → Compare to baseline
  9. STORE_FORECASTS → Save predictions
  10. CHECK_THRESHOLDS → If risk > 0.7, publish alert
  11. PUBLISH_EVENT → Broadcast forecasts
  12. UPDATE_UI → Refresh forecast charts

UI Display:
  - ASCII chart showing 7-day forecast trajectory
  - Risk score with visual indicator (bar chart)
  - Model comparison: "ARIMA: 25 | PROPHET: 28 | LSTM: 30 | ENSEMBLE: 28"
  - Confidence intervals shown as ranges

Agent Controls:
  - [▶ FORECAST NOW] [🔄 RETRAIN ALL] [📈 MODEL STATS] [⚙ WEIGHTS]

Message Bus Events Published:
  - "forecaster.complete" → {countries_forecasted, high_risk_count}
  - "forecaster.alert.high_risk" → {country, risk_score}
  - "forecaster.retrain.complete" → {models_updated}

Message Bus Events Subscribed:
  - "analyzer.sentiment.complete" → May trigger re-forecast
```

#### AGENT 4: ALERT MANAGER AGENT
```yaml
Name: "ALERTMGR-01"
Status Indicator: "● MONITORING" / "⚠ ALERT ACTIVE"
Display Panel: "// ACTIVE ALERTS"
Responsibilities:
  - Monitor all alert conditions
  - Apply severity classification
  - Enforce cooldown periods
  - Send notifications (email/Slack)
  - Log all alerts
  - Provide alert history

Workflow:
  1. LISTEN → Monitor message bus for all events
  2. CHECK_CONDITIONS → Evaluate alert rules
     - Event spike (Z-score > 2.0)
     - Sentiment shift (|Δ| > 0.3)
     - Fatality threshold (> 10)
     - High forecast risk (> 0.7)
  3. CALCULATE_SEVERITY → Low/Medium/High/Critical
  4. CHECK_COOLDOWN → Skip if alert sent recently
  5. FORMAT_MESSAGE → Prepare notification
  6. SEND_EMAIL → SMTP delivery (if enabled)
  7. SEND_SLACK → Webhook POST (if enabled)
  8. LOG_ALERT → Store in database
  9. PUBLISH_EVENT → Broadcast alert
  10. UPDATE_UI → Add to alert panel

UI Display:
  - Blinking alert panel when active (Win98 style)
  - Alert list with severity color coding
  - Format: "[HH:MM] SEVERITY COUNTRY TYPE MESSAGE"
  - Alert counter: "CRITICAL: 3 | HIGH: 7 | MED: 12"
  - Cooldown status: "NEXT ALERT: SY in 42m"

Agent Controls:
  - [🔕 MUTE] [📧 RESEND] [📋 HISTORY] [⚙ RULES]

Message Bus Events Published:
  - "alert.triggered" → {alert_id, severity, country, type}
  - "alert.sent" → {alert_id, channels, timestamp}

Message Bus Events Subscribed:
  - "collector.gdelt.complete" → Check event spike
  - "analyzer.alert.shift" → Process sentiment alert
  - "forecaster.alert.high_risk" → Process forecast alert
```

---

## PART 3: TECHNICAL IMPLEMENTATION SPECIFICATION

### Technology Stack (FREE ONLY)

```yaml
Backend:
  Framework: Flask 3.0 (Python web framework)
  Database: PostgreSQL 14+ (data storage)
  Message Bus: Redis 7.0 (PubSub for agent communication)
  Task Queue: APScheduler (scheduling) OR Python threading
  
Agent Runtime:
  Language: Python 3.9+
  Concurrency: Threading OR asyncio
  
Frontend:
  Core: HTML5 + CSS3 + Vanilla JavaScript (no frameworks)
  Charting: Canvas API (custom drawing) OR Chart.js (configured for Win98 look)
  Real-time: Server-Sent Events (SSE) OR WebSocket
  
Data Sources (ALL FREE):
  - GDELT (HTTP downloads)
  - ACLED API (free tier)
  - Reddit API (PRAW library)
  - Hugging Face Transformers (self-hosted models)

Hosting:
  Development: localhost
  Production: Any VPS with 4GB RAM (DigitalOcean, AWS, etc.)
```

### File Structure

```
riskpulse-dashboard/
├── app.py                          # Flask application entry point
├── config.yaml                     # Configuration
├── requirements.txt                # Python dependencies
│
├── agents/                         # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py              # Abstract base agent class
│   ├── collector_agent.py         # AGENT 1: Data collection
│   ├── analyzer_agent.py          # AGENT 2: Sentiment analysis
│   ├── forecaster_agent.py        # AGENT 3: Forecasting
│   ├── alert_manager_agent.py     # AGENT 4: Alert management
│   └── message_bus.py             # Redis PubSub wrapper
│
├── models/                         # Database models
│   ├── __init__.py
│   ├── event.py
│   ├── sentiment.py
│   ├── forecast.py
│   └── alert.py
│
├── collectors/                     # Data source integrations
│   ├── gdelt.py
│   ├── acled.py
│   └── reddit.py
│
├── static/                         # Frontend assets
│   ├── css/
│   │   └── win98.css              # Windows 98 theme
│   ├── js/
│   │   ├── dashboard.js           # Main UI logic
│   │   ├── terminal.js            # Terminal emulation
│   │   └── charts.js              # Chart rendering
│   └── fonts/
│       └── ms-sans-serif.ttf      # Windows 98 font
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base layout
│   └── dashboard.html             # Main dashboard
│
└── utils/
    ├── database.py
    ├── logger.py
    └── scheduler.py
```

### Agent Base Class

```python
# agents/base_agent.py

import threading
import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name, message_bus, db_connection):
        self.name = name
        self.message_bus = message_bus
        self.db = db_connection
        self.status = "IDLE"
        self.running = False
        self.thread = None
        self.logger = logging.getLogger(f"Agent.{name}")
        
        # Subscribe to message bus topics
        self.subscriptions = self.get_subscriptions()
        for topic in self.subscriptions:
            self.message_bus.subscribe(topic, self.handle_message)
    
    @abstractmethod
    def get_subscriptions(self):
        """Return list of message topics this agent subscribes to"""
        pass
    
    @abstractmethod
    def handle_message(self, topic, message):
        """Handle incoming message from bus"""
        pass
    
    @abstractmethod
    def execute_cycle(self):
        """Main execution logic - run once per cycle"""
        pass
    
    def start(self):
        """Start the agent in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.logger.info(f"{self.name} started")
        self.publish_status("ACTIVE")
    
    def stop(self):
        """Stop the agent gracefully"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info(f"{self.name} stopped")
        self.publish_status("STOPPED")
    
    def _run_loop(self):
        """Main agent loop"""
        while self.running:
            try:
                self.execute_cycle()
            except Exception as e:
                self.logger.error(f"Cycle error: {e}", exc_info=True)
                self.publish_error(str(e))
            
            time.sleep(self.get_cycle_interval())
    
    @abstractmethod
    def get_cycle_interval(self):
        """Return seconds between execution cycles"""
        pass
    
    def publish_event(self, topic, data):
        """Publish event to message bus"""
        data['agent'] = self.name
        data['timestamp'] = datetime.utcnow().isoformat()
        self.message_bus.publish(topic, data)
    
    def publish_status(self, status):
        """Publish status update"""
        self.status = status
        self.publish_event(f'agent.{self.name}.status', {'status': status})
    
    def publish_error(self, error_message):
        """Publish error event"""
        self.publish_event(f'agent.{self.name}.error', {
            'error': error_message,
            'status': 'ERROR'
        })
```

### Message Bus Implementation

```python
# agents/message_bus.py

import redis
import json
import threading

class MessageBus:
    """Redis-based pub/sub message bus for agent communication"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        self.handlers = {}
        self.listener_thread = None
        self.running = False
    
    def subscribe(self, topic, handler):
        """Subscribe to a topic with a handler function"""
        if topic not in self.handlers:
            self.handlers[topic] = []
            self.pubsub.subscribe(topic)
        
        self.handlers[topic].append(handler)
    
    def publish(self, topic, data):
        """Publish data to a topic"""
        message = json.dumps(data)
        self.redis_client.publish(topic, message)
    
    def start_listening(self):
        """Start listening for messages in background thread"""
        self.running = True
        self.listener_thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )
        self.listener_thread.start()
    
    def _listen_loop(self):
        """Background thread that processes messages"""
        for message in self.pubsub.listen():
            if not self.running:
                break
            
            if message['type'] == 'message':
                topic = message['channel']
                data = json.loads(message['data'])
                
                # Call all registered handlers for this topic
                for handler in self.handlers.get(topic, []):
                    try:
                        handler(topic, data)
                    except Exception as e:
                        print(f"Handler error: {e}")
    
    def stop_listening(self):
        """Stop the listener thread"""
        self.running = False
        if self.listener_thread:
            self.listener_thread.join(timeout=5)
```

### Collector Agent Implementation

```python
# agents/collector_agent.py

from agents.base_agent import BaseAgent
from collectors.gdelt import GDELTCollector
from collectors.acled import ACLEDCollector
from collectors.reddit import RedditCollector
import time

class CollectorAgent(BaseAgent):
    """AGENT 1: Collects data from GDELT, ACLED, and Reddit"""
    
    def __init__(self, message_bus, db_connection, config):
        super().__init__("COLLECTOR-01", message_bus, db_connection)
        
        self.config = config
        self.gdelt = GDELTCollector(config['gdelt'])
        self.acled = ACLEDCollector(config['acled'])
        self.reddit = RedditCollector(config['reddit'])
        
        # Tracking
        self.last_gdelt_run = 0
        self.last_acled_run = 0
        self.last_reddit_run = 0
        
        # Intervals (seconds)
        self.gdelt_interval = 900   # 15 minutes
        self.acled_interval = 86400  # 24 hours
        self.reddit_interval = 3600  # 1 hour
    
    def get_subscriptions(self):
        """This agent doesn't subscribe to messages, it's scheduled"""
        return []
    
    def handle_message(self, topic, message):
        """Not used - agent is schedule-driven"""
        pass
    
    def get_cycle_interval(self):
        """Check every minute for scheduled tasks"""
        return 60
    
    def execute_cycle(self):
        """Main collection logic"""
        current_time = time.time()
        
        # GDELT collection (every 15 min)
        if current_time - self.last_gdelt_run >= self.gdelt_interval:
            self.collect_gdelt()
            self.last_gdelt_run = current_time
        
        # ACLED collection (daily)
        if current_time - self.last_acled_run >= self.acled_interval:
            self.collect_acled()
            self.last_acled_run = current_time
        
        # Reddit collection (hourly)
        if current_time - self.last_reddit_run >= self.reddit_interval:
            self.collect_reddit()
            self.last_reddit_run = current_time
    
    def collect_gdelt(self):
        """Collect GDELT events"""
        self.publish_status("COLLECTING_GDELT")
        
        try:
            events = self.gdelt.fetch_latest()
            
            if events:
                # Store in database
                self.db.insert_events(events)
                
                # Publish success event
                self.publish_event('collector.gdelt.complete', {
                    'count': len(events),
                    'errors': 0
                })
                
                self.logger.info(f"Collected {len(events)} GDELT events")
            
        except Exception as e:
            self.logger.error(f"GDELT collection failed: {e}")
            self.publish_error(f"GDELT: {str(e)}")
        
        finally:
            self.publish_status("IDLE")
    
    def collect_acled(self):
        """Collect ACLED events"""
        self.publish_status("COLLECTING_ACLED")
        
        try:
            events = self.acled.fetch_recent()
            
            if events:
                self.db.insert_events(events)
                
                self.publish_event('collector.acled.complete', {
                    'count': len(events),
                    'errors': 0
                })
                
                self.logger.info(f"Collected {len(events)} ACLED events")
            
        except Exception as e:
            self.logger.error(f"ACLED collection failed: {e}")
            self.publish_error(f"ACLED: {str(e)}")
        
        finally:
            self.publish_status("IDLE")
    
    def collect_reddit(self):
        """Collect Reddit posts"""
        self.publish_status("COLLECTING_REDDIT")
        
        try:
            posts = self.reddit.fetch_posts()
            
            if posts:
                self.db.insert_social_posts(posts)
                
                self.publish_event('collector.reddit.complete', {
                    'count': len(posts),
                    'errors': 0
                })
                
                self.logger.info(f"Collected {len(posts)} Reddit posts")
            
        except Exception as e:
            self.logger.error(f"Reddit collection failed: {e}")
            self.publish_error(f"REDDIT: {str(e)}")
        
        finally:
            self.publish_status("IDLE")
```

### Frontend: Windows 98 CSS

```css
/* static/css/win98.css */

/* CSS RESET */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ROOT VARIABLES */
:root {
    /* Windows 98 Colors */
    --win98-gray: #c0c0c0;
    --win98-title-active: #000080;
    --win98-title-inactive: #808080;
    --win98-white: #ffffff;
    --win98-black: #000000;
    --win98-shadow-dark: #808080;
    --win98-shadow-light: #ffffff;
    --win98-button-face: #c0c0c0;
    
    /* Terminal Colors */
    --terminal-bg: #000000;
    --terminal-green: #00ff00;
    --terminal-amber: #ffcc00;
    --terminal-red: #ff0000;
    --terminal-blue: #00ccff;
    --terminal-gray: #808080;
    
    /* Status Colors */
    --status-ok: #008000;
    --status-warning: #ff8c00;
    --status-alert: #ff0000;
    
    /* Fonts */
    --font-system: 'MS Sans Serif', Arial, sans-serif;
    --font-mono: 'Courier New', Courier, monospace;
    
    /* Sizes (8px grid) */
    --text-xs: 8px;
    --text-sm: 10px;
    --text-md: 11px;
    --text-lg: 12px;
    --text-xl: 14px;
}

/* BODY */
body {
    background: #008080; /* Teal desktop background */
    font-family: var(--font-system);
    font-size: var(--text-md);
    color: var(--win98-black);
    overflow: hidden;
}

/* MAIN WINDOW */
.win98-window {
    position: absolute;
    top: 8px;
    left: 8px;
    right: 8px;
    bottom: 8px;
    background: var(--win98-gray);
    border: 2px solid;
    border-color: var(--win98-shadow-light) var(--win98-shadow-dark) 
                  var(--win98-shadow-dark) var(--win98-shadow-light);
    display: flex;
    flex-direction: column;
}

/* TITLE BAR */
.win98-titlebar {
    background: var(--win98-title-active);
    color: var(--win98-white);
    padding: 2px 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 20px;
    font-size: var(--text-md);
    font-weight: bold;
}

.win98-title {
    padding-left: 4px;
}

.win98-controls {
    display: flex;
    gap: 2px;
}

.win98-controls button {
    width: 16px;
    height: 14px;
    background: var(--win98-gray);
    border: 1px solid;
    border-color: var(--win98-shadow-light) var(--win98-shadow-dark) 
                  var(--win98-shadow-dark) var(--win98-shadow-light);
    font-size: var(--text-sm);
    font-weight: bold;
    cursor: pointer;
    padding: 0;
}

.win98-controls button:active {
    border-color: var(--win98-shadow-dark) var(--win98-shadow-light) 
                  var(--win98-shadow-light) var(--win98-shadow-dark);
}

/* MENU BAR */
.win98-menubar {
    background: var(--win98-gray);
    border-bottom: 1px solid var(--win98-shadow-dark);
    padding: 2px 4px;
    display: flex;
    gap: 8px;
    height: 20px;
    font-size: var(--text-md);
}

.menu-item {
    padding: 2px 8px;
    cursor: pointer;
}

.menu-item:hover {
    background: var(--win98-menu-highlight);
    color: var(--win98-white);
}

/* TOOLBAR */
.win98-toolbar {
    background: var(--win98-gray);
    border-bottom: 1px solid var(--win98-shadow-dark);
    padding: 4px;
    display: flex;
    gap: 2px;
    height: 32px;
}

.toolbar-button {
    width: 24px;
    height: 24px;
    background: var(--win98-gray);
    border: 1px solid;
    border-color: var(--win98-shadow-light) var(--win98-shadow-dark) 
                  var(--win98-shadow-dark) var(--win98-shadow-light);
    cursor: pointer;
    font-size: var(--text-lg);
}

/* MAIN CONTENT AREA */
.win98-content {
    flex: 1;
    background: var(--win98-gray);
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 4px;
    padding: 4px;
}

/* TERMINAL PANEL */
.terminal-panel {
    background: var(--terminal-bg);
    border: 2px solid;
    border-color: var(--win98-shadow-dark) var(--win98-shadow-light) 
                  var(--win98-shadow-light) var(--win98-shadow-dark);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.panel-header {
    background: var(--win98-gray);
    color: var(--win98-black);
    padding: 2px 4px;
    border-bottom: 1px solid var(--win98-shadow-dark);
    font-size: var(--text-sm);
    font-weight: bold;
    display: flex;
    justify-content: space-between;
}

.panel-title {
    color: var(--terminal-blue);
    font-family: var(--font-mono);
}

.panel-status {
    color: var(--status-ok);
    font-family: var(--font-mono);
}

.terminal-content {
    flex: 1;
    padding: 4px;
    font-family: var(--font-mono);
    font-size: var(--text-sm);
    color: var(--terminal-green);
    overflow-y: auto;
    line-height: 16px; /* 8px grid * 2 */
}

/* TERMINAL LINE */
.terminal-line {
    display: flex;
    gap: 8px;
    margin-bottom: 2px;
    white-space: nowrap;
}

.timestamp {
    color: var(--terminal-gray);
}

.severity {
    font-weight: bold;
    min-width: 64px;
}

.severity-critical {
    color: var(--terminal-red);
}

.severity-high {
    color: var(--terminal-amber);
}

.severity-medium {
    color: var(--terminal-green);
}

.location {
    color: var(--terminal-blue);
    min-width: 80px;
}

.message {
    color: var(--terminal-green);
}

/* STATUS BAR */
.win98-statusbar {
    background: var(--win98-gray);
    border-top: 1px solid var(--win98-shadow-light);
    padding: 2px 4px;
    display: flex;
    gap: 1px;
    height: 20px;
    font-size: var(--text-sm);
}

.status-segment {
    padding: 2px 8px;
    border: 1px solid;
    border-color: var(--win98-shadow-dark) var(--win98-shadow-light) 
                  var(--win98-shadow-light) var(--win98-shadow-dark);
}

/* DATA TABLE */
.data-table {
    width: 100%;
    font-family: var(--font-mono);
    font-size: var(--text-sm);
    border-collapse: collapse;
}

.data-table th {
    background: var(--win98-gray);
    padding: 4px 8px;
    border: 1px solid var(--win98-shadow-dark);
    text-align: left;
    font-weight: bold;
}

.data-table td {
    padding: 2px 8px;
    border: 1px solid var(--terminal-gray);
}

.data-table tr:hover {
    background: rgba(0, 255, 0, 0.1);
}

/* SCROLLBAR (Windows 98 style) */
::-webkit-scrollbar {
    width: 16px;
    height: 16px;
}

::-webkit-scrollbar-track {
    background: var(--win98-gray);
}

::-webkit-scrollbar-thumb {
    background: var(--win98-button-face);
    border: 2px solid;
    border-color: var(--win98-shadow-light) var(--win98-shadow-dark) 
                  var(--win98-shadow-dark) var(--win98-shadow-light);
}

/* BLINKING ALERT */
@keyframes blink {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0; }
}

.alert-active {
    animation: blink 1s infinite;
}

/* ASCII CHART */
.ascii-chart {
    font-family: var(--font-mono);
    font-size: var(--text-sm);
    line-height: 16px;
    color: var(--terminal-green);
    white-space: pre;
}
```

### Frontend: Dashboard JavaScript

```javascript
// static/js/dashboard.js

class Dashboard {
    constructor() {
        this.eventSource = null;
        this.panels = {
            collector: document.getElementById('panel-collector'),
            analyzer: document.getElementById('panel-analyzer'),
            forecaster: document.getElementById('panel-forecaster'),
            alerts: document.getElementById('panel-alerts')
        };
        
        this.init();
    }
    
    init() {
        // Connect to server-sent events
        this.connectSSE();
        
        // Update clock every second
        setInterval(() => this.updateClock(), 1000);
        
        // Request initial data
        this.fetchInitialData();
    }
    
    connectSSE() {
        this.eventSource = new EventSource('/stream');
        
        // Agent status updates
        this.eventSource.addEventListener('agent_status', (e) => {
            const data = JSON.parse(e.data);
            this.updateAgentStatus(data.agent, data.status);
        });
        
        // New events collected
        this.eventSource.addEventListener('events_collected', (e) => {
            const data = JSON.parse(e.data);
            this.addEventToFeed(data);
        });
        
        // Sentiment analysis complete
        this.eventSource.addEventListener('sentiment_analyzed', (e) => {
            const data = JSON.parse(e.data);
            this.updateSentimentPanel(data);
        });
        
        // Forecast updated
        this.eventSource.addEventListener('forecast_updated', (e) => {
            const data = JSON.parse(e.data);
            this.updateForecastPanel(data);
        });
        
        // Alert triggered
        this.eventSource.addEventListener('alert_triggered', (e) => {
            const data = JSON.parse(e.data);
            this.addAlert(data);
        });
        
        this.eventSource.onerror = () => {
            console.error('SSE connection lost, reconnecting...');
            setTimeout(() => this.connectSSE(), 5000);
        };
    }
    
    addEventToFeed(event) {
        const feed = document.getElementById('event-feed');
        
        // Create terminal line
        const line = document.createElement('div');
        line.className = 'terminal-line';
        
        const timestamp = new Date().toISOString().substr(11, 8);
        
        line.innerHTML = `
            <span class="timestamp">[${timestamp}]</span>
            <span class="severity severity-${event.severity}">${event.source.toUpperCase()}</span>
            <span class="location">${event.country}</span>
            <span class="message">${event.summary}</span>
        `;
        
        feed.appendChild(line);
        
        // Keep only last 100 lines
        while (feed.children.length > 100) {
            feed.removeChild(feed.firstChild);
        }
        
        // Auto-scroll
        feed.scrollTop = feed.scrollHeight;
    }
    
    updateSentimentPanel(data) {
        const tbody = document.querySelector('#sentiment-table tbody');
        tbody.innerHTML = '';
        
        data.countries.forEach(country => {
            const row = tbody.insertRow();
            
            const trend = country.shift > 0 ? '↑' : country.shift < 0 ? '↓' : '→';
            const severity = Math.abs(country.shift) > 0.3 ? 'critical' : 
                           Math.abs(country.shift) > 0.2 ? 'high' : 'medium';
            
            row.innerHTML = `
                <td>${country.code}</td>
                <td>${country.current.toFixed(2)}</td>
                <td>${country.baseline.toFixed(2)}</td>
                <td class="severity-${severity}">${trend} ${country.shift.toFixed(2)}</td>
            `;
        });
    }
    
    updateForecastPanel(data) {
        const container = document.getElementById('forecast-display');
        
        // ASCII chart
        const chart = this.generateASCIIChart(data.forecast);
        
        container.innerHTML = `
            <div class="ascii-chart">${chart}</div>
            <div class="forecast-stats">
                RISK SCORE: ${(data.risk_score * 100).toFixed(0)}%
                BASELINE: ${data.baseline.toFixed(0)}
                HORIZON: ${data.horizon_days} DAYS
            </div>
        `;
    }
    
    generateASCIIChart(values) {
        const height = 10;
        const width = values.length;
        const max = Math.max(...values);
        const min = Math.min(...values);
        
        let chart = '';
        
        for (let y = height; y >= 0; y--) {
            const value = min + (max - min) * (y / height);
            chart += value.toFixed(0).padStart(4) + ' ┤';
            
            for (let x = 0; x < width; x++) {
                const normalizedValue = (values[x] - min) / (max - min) * height;
                chart += Math.abs(normalizedValue - y) < 0.5 ? '●' : ' ';
            }
            
            chart += '\n';
        }
        
        chart += '    └' + '─'.repeat(width) + '\n';
        chart += '     ';
        for (let i = 0; i < width; i++) {
            chart += i === 0 ? 'NOW' : `D+${i}`;
            chart += ' ';
        }
        
        return chart;
    }
    
    addAlert(alert) {
        const container = document.getElementById('alerts-list');
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `terminal-line alert-active`;
        
        const timestamp = new Date().toISOString().substr(11, 8);
        
        alertDiv.innerHTML = `
            <span class="timestamp">[${timestamp}]</span>
            <span class="severity severity-${alert.severity}">${alert.severity.toUpperCase()}</span>
            <span class="location">${alert.country}</span>
            <span class="message">${alert.type}: ${alert.message}</span>
        `;
        
        container.insertBefore(alertDiv, container.firstChild);
        
        // Stop blinking after 5 seconds
        setTimeout(() => {
            alertDiv.classList.remove('alert-active');
        }, 5000);
        
        // Update alert counter
        this.updateAlertCounter();
    }
    
    updateAgentStatus(agent, status) {
        const statusElement = document.getElementById(`agent-${agent}-status`);
        if (statusElement) {
            const indicator = status === 'ACTIVE' ? '●' : 
                            status === 'IDLE' ? '○' : '✕';
            const color = status === 'ACTIVE' ? 'var(--status-ok)' : 
                         status === 'IDLE' ? 'var(--terminal-gray)' : 
                         'var(--status-alert)';
            
            statusElement.textContent = `[${indicator} ${status}]`;
            statusElement.style.color = color;
        }
    }
    
    updateClock() {
        const clock = document.getElementById('clock');
        const now = new Date();
        clock.textContent = now.toISOString().substr(0, 19).replace('T', ' ') + ' UTC';
    }
    
    updateAlertCounter() {
        const alerts = document.querySelectorAll('#alerts-list .terminal-line');
        const critical = Array.from(alerts).filter(a => 
            a.textContent.includes('CRITICAL')).length;
        const high = Array.from(alerts).filter(a => 
            a.textContent.includes('HIGH')).length;
        
        document.getElementById('alert-counter').textContent = 
            `ALERTS: ${critical} CRITICAL | ${high} HIGH`;
    }
    
    fetchInitialData() {
        // Load initial dashboard state
        fetch('/api/dashboard/state')
            .then(r => r.json())
            .then(data => {
                this.updateSentimentPanel(data.sentiment);
                this.updateForecastPanel(data.forecast);
                data.recent_events.forEach(e => this.addEventToFeed(e));
                data.alerts.forEach(a => this.addAlert(a));
            });
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});
```

### Flask Backend (Server-Sent Events)

```python
# app.py

from flask import Flask, render_template, Response, jsonify
import json
import time
from agents.collector_agent import CollectorAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.forecaster_agent import ForecastAgent
from agents.alert_manager_agent import AlertManagerAgent
from agents.message_bus import MessageBus
from utils.database import DatabaseManager
import yaml

app = Flask(__name__)

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Initialize components
db = DatabaseManager(config['database'])
message_bus = MessageBus()

# Initialize agents
agents = {
    'collector': CollectorAgent(message_bus, db, config),
    'analyzer': AnalyzerAgent(message_bus, db, config),
    'forecaster': ForecastAgent(message_bus, db, config),
    'alerts': AlertManagerAgent(message_bus, db, config)
}

# Start message bus
message_bus.start_listening()

# Start all agents
for agent in agents.values():
    agent.start()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/stream')
def stream():
    """Server-Sent Events endpoint for real-time updates"""
    def event_stream():
        # Subscribe to all agent events
        events_queue = []
        
        def on_message(topic, data):
            events_queue.append({
                'topic': topic,
                'data': data
            })
        
        # Subscribe to relevant topics
        message_bus.subscribe('collector.*', on_message)
        message_bus.subscribe('analyzer.*', on_message)
        message_bus.subscribe('forecaster.*', on_message)
        message_bus.subscribe('alert.*', on_message)
        message_bus.subscribe('agent.*.status', on_message)
        
        while True:
            if events_queue:
                event = events_queue.pop(0)
                
                # Determine event type
                if 'collector' in event['topic']:
                    event_type = 'events_collected'
                elif 'analyzer' in event['topic']:
                    event_type = 'sentiment_analyzed'
                elif 'forecaster' in event['topic']:
                    event_type = 'forecast_updated'
                elif 'alert' in event['topic']:
                    event_type = 'alert_triggered'
                elif 'status' in event['topic']:
                    event_type = 'agent_status'
                else:
                    event_type = 'unknown'
                
                yield f"event: {event_type}\n"
                yield f"data: {json.dumps(event['data'])}\n\n"
            
            time.sleep(0.1)
    
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/api/dashboard/state')
def dashboard_state():
    """Get current dashboard state"""
    return jsonify({
        'sentiment': db.get_latest_sentiment_analysis(),
        'forecast': db.get_latest_forecast(),
        'recent_events': db.get_recent_events(limit=50),
        'alerts': db.get_recent_alerts(limit=20),
        'agent_status': {
            name: agent.status 
            for name, agent in agents.items()
        }
    })

@app.route('/api/agents/control/<agent_name>/<action>')
def control_agent(agent_name, action):
    """Control agent (start/stop/restart)"""
    if agent_name not in agents:
        return jsonify({'error': 'Agent not found'}), 404
    
    agent = agents[agent_name]
    
    if action == 'start':
        agent.start()
    elif action == 'stop':
        agent.stop()
    elif action == 'restart':
        agent.stop()
        time.sleep(1)
        agent.start()
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
```

---

## PART 4: AGENT WORKFLOWS (DETAILED)

### Workflow 1: Event Collection → Analysis → Alert

```
┌─────────────────────────────────────────────────────────────────┐
│ WORKFLOW: New Event Processing                                  │
└─────────────────────────────────────────────────────────────────┘

STEP 1: Data Collection (AGENT 1)
  ┌──────────────────────────────────────────┐
  │ CollectorAgent.execute_cycle()           │
  │  1. Check if 15 min elapsed             │
  │  2. HTTP GET: GDELT latest file         │
  │  3. Parse CSV → Extract events          │
  │  4. Filter: countries + event types     │
  │  5. DB INSERT: events table             │
  │  6. PUBLISH: collector.gdelt.complete   │
  └───────────────┬──────────────────────────┘
                  │
                  ▼ (Message Bus)
  ┌──────────────────────────────────────────┐
  │ Message: {                               │
  │   topic: "collector.gdelt.complete"      │
  │   data: {count: 245, timestamp: ...}     │
  │ }                                        │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 2: Sentiment Analysis (AGENT 2)
  ┌──────────────────────────────────────────┐
  │ AnalyzerAgent.handle_message()           │
  │  1. Receive: collector.gdelt.complete   │
  │  2. DB QUERY: unprocessed events        │
  │  3. Batch into groups of 32             │
  │  4. Load BERT model (cached)            │
  │  5. Run inference on batch              │
  │  6. Calculate sentiment scores          │
  │  7. DB INSERT: sentiment_analysis       │
  │  8. Aggregate by country                │
  │  9. Compare to baseline                 │
  │  10. IF shift > 0.3:                    │
  │      PUBLISH: analyzer.alert.shift      │
  │  11. ELSE:                              │
  │      PUBLISH: analyzer.sentiment.complete│
  └───────────────┬──────────────────────────┘
                  │
                  ▼ (Message Bus - IF ALERT)
  ┌──────────────────────────────────────────┐
  │ Message: {                               │
  │   topic: "analyzer.alert.shift"          │
  │   data: {                                │
  │     country: "SY",                       │
  │     shift: -0.42,                        │
  │     severity: "high"                     │
  │   }                                      │
  │ }                                        │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 3: Alert Processing (AGENT 4)
  ┌──────────────────────────────────────────┐
  │ AlertManagerAgent.handle_message()       │
  │  1. Receive: analyzer.alert.shift       │
  │  2. Check cooldown (last alert SY)      │
  │  3. IF cooldown expired:                │
  │     a. Format alert message             │
  │     b. Send email (SMTP)                │
  │     c. Send Slack (webhook)             │
  │     d. DB INSERT: alerts table          │
  │     e. PUBLISH: alert.triggered         │
  │  4. ELSE:                               │
  │     Log: "Alert suppressed (cooldown)"  │
  └───────────────┬──────────────────────────┘
                  │
                  ▼ (Message Bus)
  ┌──────────────────────────────────────────┐
  │ Message: {                               │
  │   topic: "alert.triggered"               │
  │   data: {                                │
  │     id: "alert_001",                     │
  │     type: "sentiment_shift",             │
  │     country: "SY",                       │
  │     severity: "high"                     │
  │   }                                      │
  │ }                                        │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 4: UI Update (Frontend)
  ┌──────────────────────────────────────────┐
  │ Dashboard.addAlert()                     │
  │  1. Receive SSE: alert.triggered        │
  │  2. Create terminal line element        │
  │  3. Add to alerts panel (top)           │
  │  4. Apply blinking animation            │
  │  5. Update alert counter                │
  │  6. Play beep sound (optional)          │
  └──────────────────────────────────────────┘
```

### Workflow 2: Daily Forecast Generation

```
┌─────────────────────────────────────────────────────────────────┐
│ WORKFLOW: Daily Forecast Update                                 │
└─────────────────────────────────────────────────────────────────┘

TRIGGER: Cron schedule (00:00 UTC daily)

STEP 1: Data Preparation (AGENT 3)
  ┌──────────────────────────────────────────┐
  │ ForecastAgent.execute_cycle()            │
  │  1. Check: time == 00:00 UTC?           │
  │  2. DB QUERY: events last 90 days       │
  │  3. Aggregate: events per day per country│
  │  4. For each country:                   │
  └───────────────┬──────────────────────────┘
                  │
                  ▼ (For SYRIA)
  ┌──────────────────────────────────────────┐
  │ Time Series: [12,15,18,14,20,22,19,...]  │
  │ Length: 90 days                          │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 2: Model Training & Inference (AGENT 3)
  ┌──────────────────────────────────────────┐
  │ ARIMA Model:                             │
  │  1. Fit ARIMA(5,1,0)(1,1,1,7)           │
  │  2. Forecast 7 days                     │
  │  3. Output: [23,25,24,26,28,27,25]      │
  └───────────────┬──────────────────────────┘
                  │
  ┌──────────────────────────────────────────┐
  │ Prophet Model:                           │
  │  1. Fit with weekly seasonality         │
  │  2. Generate future dataframe (7 days)  │
  │  3. Predict                             │
  │  4. Output: [24,26,25,27,29,28,26]      │
  └───────────────┬──────────────────────────┘
                  │
  ┌──────────────────────────────────────────┐
  │ LSTM Model:                              │
  │  1. Prepare sequences (30-day windows)  │
  │  2. Train neural network                │
  │  3. Multi-step forecast                 │
  │  4. Output: [25,27,26,28,30,29,27]      │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 3: Ensemble & Risk Calculation (AGENT 3)
  ┌──────────────────────────────────────────┐
  │ Weighted Average:                        │
  │  Ensemble = 0.3*ARIMA + 0.3*Prophet +   │
  │             0.4*LSTM                     │
  │  = [24,26,25,27,29,28,26]               │
  │                                          │
  │ Risk Score:                              │
  │  Baseline = 18.5 (90-day average)       │
  │  Forecast Max = 29                      │
  │  Risk = min(29/18.5, 1.0) = 1.0         │
  │  → CRITICAL (> 0.7 threshold)           │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 4: Store & Alert (AGENT 3)
  ┌──────────────────────────────────────────┐
  │  1. DB INSERT: forecasts table          │
  │  2. IF risk_score > 0.7:                │
  │     PUBLISH: forecaster.alert.high_risk │
  │  3. PUBLISH: forecaster.complete        │
  └───────────────┬──────────────────────────┘
                  │
                  ▼ (Message Bus)
  ┌──────────────────────────────────────────┐
  │ Message: {                               │
  │   topic: "forecaster.alert.high_risk"    │
  │   data: {                                │
  │     country: "SY",                       │
  │     risk_score: 1.0,                     │
  │     forecast: [24,26,25,27,29,28,26]     │
  │   }                                      │
  │ }                                        │
  └───────────────┬──────────────────────────┘
                  │
                  ▼

STEP 5: Alert & UI Update (AGENT 4 + Frontend)
  Same as Workflow 1, Step 3-4
```

### Workflow 3: Agent Communication Protocol

```
MESSAGE BUS TOPICS:

Data Collection:
  - collector.gdelt.complete
  - collector.acled.complete
  - collector.reddit.complete
  - collector.error

Sentiment Analysis:
  - analyzer.sentiment.complete
  - analyzer.alert.shift
  - analyzer.error

Forecasting:
  - forecaster.complete
  - forecaster.alert.high_risk
  - forecaster.retrain.complete
  - forecaster.error

Alerts:
  - alert.triggered
  - alert.sent
  - alert.suppressed (cooldown)

Agent Status:
  - agent.COLLECTOR-01.status
  - agent.ANALYZER-01.status
  - agent.FORECASTER-01.status
  - agent.ALERTMGR-01.status

MESSAGE FORMAT:
{
  "agent": "COLLECTOR-01",
  "timestamp": "2024-03-15T14:32:05.123Z",
  "topic": "collector.gdelt.complete",
  "data": {
    "count": 245,
    "errors": 0,
    "duration_ms": 8234
  }
}
```

---

## PART 5: IMPLEMENTATION CHECKLIST

### Phase 1: Foundation (Week 1)
```
□ Set up project structure
□ Install dependencies (Flask, Redis, PostgreSQL)
□ Create database schema
□ Implement BaseAgent class
□ Implement MessageBus class
□ Create Windows 98 CSS framework
□ Build basic HTML layout
```

### Phase 2: Data Collection (Week 2)
```
□ Implement GDELT collector
□ Implement ACLED collector
□ Implement Reddit collector
□ Build CollectorAgent
□ Test data ingestion
□ Verify database inserts
□ Build event feed UI panel
```

### Phase 3: Analysis (Week 3)
```
□ Download BERT model
□ Implement sentiment analyzer
□ Build AnalyzerAgent
□ Test sentiment calculation
□ Build sentiment UI panel
□ Implement shift detection
```

### Phase 4: Forecasting (Week 4)
```
□ Implement ARIMA forecaster
□ Implement Prophet forecaster
□ Implement LSTM forecaster
□ Build ForecastAgent
□ Test ensemble forecasting
□ Build forecast UI panel (ASCII charts)
```

### Phase 5: Alerts (Week 5)
```
□ Implement alert conditions
□ Build AlertManagerAgent
□ Set up email SMTP
□ Set up Slack webhook
□ Test alert delivery
□ Build alerts UI panel
□ Implement cooldown logic
```

### Phase 6: Integration (Week 6)
```
□ Connect all agents to message bus
□ Implement Server-Sent Events
□ Build real-time dashboard updates
□ Add agent control buttons
□ Test complete workflows
□ Performance optimization
```

### Phase 7: Polish (Week 7)
```
□ Refine Windows 98 aesthetic
□ Add sound effects (beeps for alerts)
□ Implement error handling
□ Add logging
□ Create documentation
□ Deploy to production
```

---

## PART 6: DELIVERABLES

### Functional Requirements
```
✓ Real-time data collection from GDELT, ACLED, Reddit
✓ Automatic sentiment analysis on all events
✓ Daily 7-day forecasts for active countries
✓ Four types of alerts (event spike, sentiment shift, fatality, forecast risk)
✓ Multi-agent architecture with message bus
✓ Windows 98 aesthetic (strict adherence)
✓ Terminal-style data display
✓ Real-time UI updates (Server-Sent Events)
✓ Agent status monitoring
✓ Alert notifications (email + Slack)
✓ Data visualization (ASCII charts + tables)
```

### Non-Functional Requirements
```
✓ All APIs must be FREE
✓ Zero modern design elements (no gradients, shadows, rounded corners)
✓ Monospace fonts for all data
✓ Grid-based layout (8px baseline)
✓ Response time: < 100ms for UI updates
✓ System uptime: > 99%
✓ Agent autonomy: Operate independently
✓ Message bus latency: < 50ms
```

---

## END OF PROMPT

This prompt provides complete specifications for building a Windows 98-themed intelligence dashboard with multi-agent architecture using only free APIs. All visual, technical, and workflow details are defined.

**NEXT STEP**: Begin implementation following Phase 1 of the checklist.
