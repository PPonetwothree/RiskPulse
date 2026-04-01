# RiskPulse Intelligence Dashboard v1.0 — User Manual

## 1. Introduction
Welcome to **RiskPulse Intelligence**, a state-of-the-art geopolitical monitoring platform engineered with a sleek modernized intelligence terminal interface. This dashboard synthesizes intelligence inputs across multiple simulated tracking agents, analyzing sentiment, predicting conflict risks, and surfacing actionable alerts in real time. 

This document serves as your complete guide to operating the dashboard interface, managing the agent simulation, and interpreting the synthesized intelligence.

---

## 2. Interface Layout

The dashboard utilizes an immersive, draggable windowing system containing a Menu Bar, a quick-action Toolbar, four specialized Intelligence Panels, and a persistent Status Bar.

### 2.1 The Menu Bar
Located at the top of the interface, the Menu Bar houses fundamental controls:
- **File**: Export current event logs to `.txt`, export caught alerts, or clear the live terminal feed. You can also trigger a visual interface shutdown.
- **View**: Toggle the visibility of the four core panels. Use **Auto-Scroll Feed** to lock or unlock the automatic scrolling behavior of the Live Event terminal.
- **Agents**: Control the lifecycle of the simulated background agents. You can issue Start/Stop commands across the board, or force individual agents to output restart logs.
- **Reports**: Generate modally-rendered summary reports including overall **Agent Statistics**, a summarized **Risk Summary** spanning all monitored countries, and the full unabridged **Alert History**.
- **Help**: View system methodology metrics, version info, and keyboard shortcuts.

### 2.2 The Toolbar
Located immediately beneath the Menu Bar, the Toolbar provides quick access to critical actions:
- **REFRESH (⟳)**: Reloads the simulated starting state of the dashboard.
- **PAUSE / RESUME (⏸ / ▶)**: Halts or resumes the live appending of incoming data feeds. (Note: The background simulation engine continues generating data invisibly).
- **CLR ALERTS (🗑)**: Purges all active alerts and resets the critical/high/medium counters back to zero.
- **FORCE COLLECT (⚡)**: Commands the Collector agent to forcefully output an immediate ingestion log.
- **Counters**: Live trackers indicating the total ingested events and the volume of alerts triggered since session start.

---

## 3. The Core Intelligence Panels (Agents)

The workspace is divided into four distinct panels, each managed by a dedicated sub-agent.

### 3.1 Live Event Feed (COLLECTOR-01)
The primary ingestion terminal. It mimics connections to massive OSINT datasets like **GDELT**, **ACLED**, and social signal scrapers (e.g., **Reddit**).
- **Function**: Automatically streams synthesized political, military, and diplomatic events every few seconds.
- **Status Badges**: Shows agent state (e.g., ACTIVE) and bottom aggregates of how many events originated from each respective network.

### 3.2 Sentiment Analysis (ANALYZER-01)
Monitors the political temperature of tracked states (e.g., Syria, Ukraine, Yemen, Sudan).
- **Function**: Displays current and baseline sentiment algorithms. 
- **Metrics Tracked**:
  - `Δ SHIFT`: The magnitude of sentiment divergence from the baseline.
  - `TREND`: Improvment (`↑ IMPR`), Deterioration (`↓ DETR`), or Stability (`→ STBL`).
  - `STATUS`: Severity coding (`OK`, `MEDIUM`, `HIGH`, `CRITICAL`) based on standard deviation limits.

### 3.3 Active Alerts (ALERTMGR-01)
The crisis monitoring hub. If the Analyzer agent detects a drastic sentiment shift (Δ > 0.18), this panel trips an alarm.
- **Function**: Displays flashing, critical UI alerts. The terminal audibly beeps whenever a top-tier incident surfaces.
- **Counters**: Tracks the volume of Critical, High, and Medium severity events caught by the alarm system. Older alerts are automatically pushed down the terminal stack.

### 3.4 Forecasts & Predictions (FORECASTER-01)
A visual prognostic engine plotting a 7-day predicted risk index.
- **Function**: Uses simulated predictive models (ARIMA, Prophet, LSTM, and an ensemble aggregate).
- **Controls**: Use the **Country drop-down menu** in the top left of the panel to load the specific forecasting chart for a given theater.
- **Visuals**: A dynamically rendered canvas chart, complemented by a horizontal `RISK SCORE` percentage bar and a granular day-by-day (D+0, D+1, etc.) grid output.

---

## 4. Keyboard Shortcuts

For rapid OSINT operation, the dashboard supports the following hotkeys:
- `F5` — Hard refresh the entire dashboard, resetting the data simulation to day zero.
- `Escape (Esc)` — Immediately dismisses any open dropdown menu or modal dialog box.

---

## 5. Working with the Simulation

*Note: This specific deployment runs purely as a **Static Frontend Simulation** and requires no active database or backend.*

Because it is a simulation, the dashboard relies on a continuous JavaScript background engine.
- **Data Generation**: Random but realistic geopolitical summaries, sources, and regions are spliced together into the Event Feed continuously.
- **Sentiment Alarm Trigger**: Every cycle has a small probability to generate a heavy shift in a random country's stability metrics. Leave the dashboard running in an open tab, and you will organically catch "CRITICAL" state shifts and alarm sirens as time goes on.
- **Forecast Mutation**: The 7-day predictive curves morph subtly every ~20 seconds to represent evolving situational models.

## 6. Frequently Asked Questions

**Q: Where do the exported logs go?**  
A: Exporting via **File > Export Event Log** triggers a direct browser download of a plain `.txt` file containing the precise string outputs of the terminal feed.

**Q: Can I close panels permanently?**  
A: Partially. Using the **View** dropdown, you can toggle panels off. The grid display will dynamically reflow to dedicate more screen real-estate to the remaining active agents.

**Q: The alarm beep is startling. Can I disable it?**  
A: Currently, audio alerts are hardwired into the `ALERTMGR-01` simulation core. Browsers may restrict the auto-play of the `AudioContext` until you click or interact with the page. To silence it indefinitely, you can pause the entire feed via the Toolbar, or toggle the Active Alerts panel off.

---
*RiskPulse Intelligence // Build v1.0 // System Manual*
