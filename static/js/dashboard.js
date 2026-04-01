/**
 * dashboard.js — Main RiskPulse dashboard controller
 * All buttons, menus, title-bar controls fully wired.
 * STATIC SIMULATION VERSION FOR NETLIFY DEPLOYMENT
 */

class RiskPulseDashboard {
    constructor() {
        this._paused = false;
        this._alertsFired = 0;
        this._totalEvents = 0;
        this._gdeltCount = 0;
        this._acledCount = 0;
        this._redditCount = 0;
        this._alertCounters = { critical: 0, high: 0, medium: 0 };
        this._forecastData = {};
        this._selectedCountry = '';
        this._autoScroll = true;
        this._maximized = false;
        this._panelVisible = { collector: true, analyzer: true, alerts: true, forecaster: true };
        this._currentMenuId = null;   // track which dropdown is open

        // DOM refs
        this.$feed       = document.getElementById('feed-body');
        this.$alertsList = document.getElementById('alerts-list');
        this.$sentTbody  = document.getElementById('sentiment-tbody');
        this.$fcCanvas   = document.getElementById('forecast-canvas');
        this.$fcSelect   = document.getElementById('forecast-country-select');
        this.$clock      = document.getElementById('sb-clock');
        this.$modal      = document.getElementById('modal-overlay');
        this.$modalTitle = document.getElementById('modal-title');
        this.$modalBody  = document.getElementById('modal-body');

        // State for mock
        this._mockAlerts = [];
        this._mockAgents = {
            'collector': { name:'COLLECTOR-01', status:'ACTIVE', cycles: 42, errors: 0, last_run: new Date().toISOString() },
            'analyzer': { name:'ANALYZER-01', status:'MONITORING', cycles: 87, errors: 1, last_run: new Date().toISOString() },
            'forecaster': { name:'FORECASTER-01', status:'IDLE', cycles: 12, errors: 0, last_run: new Date().toISOString() },
            'alerts': { name:'ALERTMGR-01', status:'MONITORING', cycles: 300, errors: 0, last_run: new Date().toISOString() },
        };

        this._bindControls();
        this._bindMenus();
        this._startClock();
        this._loadInitialState();
        this._simulateBackend();
    }

    // ──────────────────────── Simulation Loop ────────────────────────────

    _simulateBackend() {
        this._setSBSSE('LIVE (SIM)', 'ok');
        Terminal.appendSystem(this.$feed, 'STATIC SIMULATION STARTED — GENERATING LIVE DATA');

        // Initial agent active states
        this._updateAgentStatus('COLLECTOR-01', 'ACTIVE');
        this._updateAgentStatus('ANALYZER-01', 'ANALYZING');
        this._updateAgentStatus('FORECASTER-01', 'FORECASTING');
        this._updateAgentStatus('ALERTMGR-01', 'MONITORING');

        // Event Collector Loop (every 2.5s)
        setInterval(() => {
            if (this._paused) return;
            const sources = ['GDELT', 'ACLED', 'Reddit'];
            const countries = ['SY', 'UA', 'YE', 'SD', 'ET', 'AF', 'IQ', 'ML', 'MM', 'SO'];
            const locations = ['Capital Region', 'Northern Border', 'Eastern Province', 'Coastal Zone', 'Industrial Center', 'Disputed Territory'];
            const types = ['Protest Activity', 'Military Movement', 'Diplomatic Statement', 'Infrastructure Incident', 'Unrest Reported', 'Border Clash'];
            const severities = ['low', 'low', 'low', 'medium', 'medium', 'high', 'critical'];
            
            const evtCount = Math.floor(Math.random() * 3) + 1;
            const evts = [];
            for (let i = 0; i < evtCount; i++) {
                evts.push({
                    source: sources[Math.floor(Math.random() * sources.length)],
                    country: countries[Math.floor(Math.random() * countries.length)],
                    location: locations[Math.floor(Math.random() * locations.length)],
                    summary: types[Math.floor(Math.random() * types.length)],
                    severity: severities[Math.floor(Math.random() * severities.length)],
                });
            }
            this._onEventsCollected({ events: evts, count: evtCount });

            // Randomly trigger a sentiment shift
            if (Math.random() > 0.8) {
                const shift = (Math.random() * 0.4) - 0.2;
                const cc = countries[Math.floor(Math.random() * countries.length)];
                Terminal.appendSystem(this.$feed,
                    `SENTIMENT_SHIFT: ${cc} Δ=${shift > 0 ? '+' : ''}${shift.toFixed(2)}`,
                    Math.abs(shift) > 0.15 ? 'sev-high' : 'sev-medium');
                
                // Trigger alert if big shift
                if (Math.abs(shift) > 0.18) {
                    const alertObj = {
                        alert_type: shift > 0 ? 'SUDDEN_IMPROVEMENT' : 'SUDDEN_DETERIORATION',
                        country: cc,
                        severity: Math.abs(shift) > 0.3 ? 'critical' : 'high',
                        message: `Sentiment shifted rapidly in ${cc} (${shift.toFixed(2)})`,
                        triggered_at: new Date().toISOString()
                    };
                    this._addAlert(alertObj);
                    this._mockAlerts.push(alertObj);
                }
            }
        }, 3500);

        // Forecaster Loop (every 20s)
        setInterval(() => {
            if (this._paused) return;
            // slightly perturb forecast data
            const newData = [];
            Object.values(this._forecastData).forEach(f => {
                f.forecast = f.forecast.map(v => Math.max(0, v + (Math.random() * 4) - 2));
                f.risk_score = Math.max(0, Math.min(1, f.risk_score + (Math.random() * 0.1) - 0.05));
                newData.push(f);
            });
            this._onForecastUpdated({ forecasts: newData });
            this._updateAgentStatus('FORECASTER-01', 'FORECASTING');
            setTimeout(() => this._updateAgentStatus('FORECASTER-01', 'IDLE'), 2000);
        }, 20000);
    }

    // ──────────────────────── Initial State ──────────────────────────

    _loadInitialState() {
        const countries = ['SY', 'UA', 'YE', 'SD', 'ET', 'AF', 'IQ', 'ML', 'MM', 'SO'];
        
        // Mock Sentiment
        const mockSentiment = {
            countries: countries.map(cc => ({
                code: cc,
                current_score: Math.random(),
                baseline: Math.random(),
                shift: (Math.random() * 0.4) - 0.2,
                events_analyzed: Math.floor(Math.random() * 500)
            }))
        };
        this._updateSentimentPanel(mockSentiment);

        // Mock Forecasts
        const mockForecasts = countries.map(cc => ({
            country: cc,
            forecast: Array.from({length:7}, () => Math.floor(Math.random() * 100)),
            arima: Array.from({length:7}, () => Math.floor(Math.random() * 100)),
            prophet: Array.from({length:7}, () => Math.floor(Math.random() * 100)),
            lstm: Array.from({length:7}, () => Math.floor(Math.random() * 100)),
            risk_score: Math.random(),
            baseline: 30
        }));
        
        mockForecasts.forEach(f => { this._forecastData[f.country] = f; });
        const top = mockForecasts[0];
        if (top) {
            this.$fcSelect.value = top.country;
            this._selectedCountry = top.country;
            this._renderForecast(top);
        }

        // Mock Recent Events
        for(let i=0; i<8; i++) {
            Terminal.appendToFeed(this.$feed, 'GDELT', countries[Math.floor(Math.random()*countries.length)],
                'Capital Region', 'Initial background event', 'low');
            this._totalEvents++;
            this._gdeltCount++;
        }
        this._updateEventsTotal();
        this._refreshMetrics();

        // Agents
        Object.entries(this._mockAgents).forEach(([, info]) => {
            if (info.name) this._updateAgentStatus(info.name, info.status);
        });
    }

    // ──────────────────────── Event Handlers ─────────────────────────

    _onEventsCollected(data) {
        const { events = [], count = 0 } = data;

        // Determine source from the first event in the batch
        const src = (events[0] && events[0].source) ? events[0].source : '';

        (events || []).forEach(evt => {
            Terminal.appendToFeed(this.$feed,
                evt.source || src || 'GDELT',
                evt.country, evt.location, evt.summary, evt.severity);
        });

        events.forEach(e => {
            if (e.source === 'GDELT')        this._gdeltCount++;
            else if (e.source === 'ACLED')   this._acledCount++;
            else if (e.source === 'Reddit')  this._redditCount++;
        });

        this._totalEvents += count;
        this._updateEventsTotal();
        this._refreshMetrics();

        Terminal.appendSystem(this.$feed,
            `COLLECTED ${count} EVENTS [TOTAL: ${data.total || this._totalEvents}]`, 'dim');
    }

    _onForecastUpdated(data) {
        const { forecasts = [] } = data;
        forecasts.forEach(f => { this._forecastData[f.country] = f; });

        const country = this._selectedCountry || (forecasts[0] && forecasts[0].country);
        if (country && this._forecastData[country]) {
            this._renderForecast(this._forecastData[country]);
        }

        Terminal.appendSystem(this.$feed,
            `FORECASTS UPDATED: ${forecasts.length} COUNTRIES MODELED`, 'dim');
    }

    _renderForecast(f) {
        if (!f) return;
        const { forecast = [], arima = [], prophet = [], lstm = [], risk_score = 0, baseline = 0 } = f;

        Charts.drawForecastChart(this.$fcCanvas, { arima, prophet, lstm, ensemble: forecast, baseline });

        document.getElementById('fc-arima').textContent   = arima.length   ? arima.slice(-1)[0].toFixed(0)   : '--';
        document.getElementById('fc-prophet').textContent = prophet.length  ? prophet.slice(-1)[0].toFixed(0) : '--';
        document.getElementById('fc-lstm').textContent    = lstm.length     ? lstm.slice(-1)[0].toFixed(0)    : '--';
        document.getElementById('fc-ens').textContent     = forecast.length ? forecast.slice(-1)[0].toFixed(0): '--';

        const riskPct = (risk_score * 100).toFixed(0);
        document.getElementById('risk-bar').style.width = riskPct + '%';
        document.getElementById('risk-bar').style.background =
            risk_score > 0.7 ? '#ff0000' : risk_score > 0.5 ? '#ff8c00' : '#008800';
        document.getElementById('forecast-risk-val').textContent = riskPct + '%';
        document.getElementById('forecast-risk-val').style.color =
            risk_score > 0.7 ? '#ff0000' : risk_score > 0.5 ? '#ffcc00' : '#00ff00';

        const gridHtml = forecast.map((v, i) =>
            `<span style="margin-right:8px;"><span style="color:#444;">D+${i}:</span><b style="color:#0f0;">${v.toFixed(0)}</b></span>`
        ).join('');
        document.getElementById('forecast-grid').innerHTML = gridHtml || 'NO DATA';
    }

    // ──────────────────────── Sentiment Panel ────────────────────────

    _updateSentimentPanel(data) {
        const countries = data.countries || [];
        if (countries.length === 0) return;

        let totalShifts = 0, totalAnalyzed = 0;
        const rows = countries.map(c => {
            totalAnalyzed += (c.count || c.events_analyzed || 0);
            const shift = c.shift || 0;
            const shiftAbs = Math.abs(shift);
            if (shiftAbs > 0.15) totalShifts++;

            const trend    = shift > 0.02 ? '↑ IMPR' : shift < -0.02 ? '↓ DETR' : '→ STBL';
            const trendCls = shift > 0.02 ? 'trend-up' : shift < -0.02 ? 'trend-down' : 'trend-flat';
            const sevCls   = shiftAbs > 0.3 ? 'sev-critical' : shiftAbs > 0.2 ? 'sev-high' : shiftAbs > 0.1 ? 'sev-medium' : 'sev-low';
            const status   = shiftAbs > 0.3 ? 'CRITICAL' : shiftAbs > 0.2 ? 'HIGH' : shiftAbs > 0.1 ? 'MEDIUM' : 'OK';

            return `<tr>
                <td><b>${c.code || c.country || '??'}</b></td>
                <td>${(c.current || c.current_score || 0).toFixed(3)}</td>
                <td style="color:#555;">${(c.baseline || c.baseline_score || 0).toFixed(3)}</td>
                <td class="${sevCls}">${shift >= 0 ? '+' : ''}${shift.toFixed(3)}</td>
                <td class="${trendCls}">${trend}</td>
                <td class="${sevCls}">[${status}]</td>
            </tr>`;
        });

        this.$sentTbody.innerHTML = rows.join('');
        document.getElementById('metric-analyzed').textContent = totalAnalyzed;
        document.getElementById('metric-shifts').textContent = totalShifts;
    }

    // ──────────────────────── Alerts Panel ───────────────────────────

    _addAlert(alert) {
        const {
            alert_type = 'UNKNOWN', country = '??',
            severity = 'low', message = '', triggered_at,
        } = alert;

        this._alertsFired++;
        this._alertCounters[severity] = (this._alertCounters[severity] || 0) + 1;
        this._updateAlertCounters(this._alertCounters);

        const ts = triggered_at
            ? new Date(triggered_at + (triggered_at.includes('Z') ? '' : 'Z')).toISOString().substring(11,19)
            : new Date().toISOString().substring(11,19);

        const sevCls = Terminal.severityClass(severity);
        const isNew  = !triggered_at || (Date.now() - new Date(triggered_at).getTime()) < 10000;

        const div = document.createElement('div');
        div.className = `alert-line ${sevCls}`;
        div.innerHTML =
            `<span class="t-time dim">[${ts}]</span>` +
            `<span class="${sevCls}" style="font-weight:bold;min-width:72px;">${severity.toUpperCase()}</span>` +
            `<span class="t-country" style="color:#88aaff;">${country}</span>` +
            `<span class="t-msg ${sevCls}">${alert_type}: ${message}</span>`;

        if (isNew && severity === 'critical') {
            div.classList.add('alert-blink');
            setTimeout(() => div.classList.remove('alert-blink'), 5000);
            this._beep();
        }

        this.$alertsList.insertBefore(div, this.$alertsList.firstChild);
        while (this.$alertsList.children.length > 50) {
            this.$alertsList.removeChild(this.$alertsList.lastChild);
        }

        document.getElementById('metric-alerts-fired').textContent = this._alertsFired;
        this._updateSBAlerts();
    }

    _updateAlertCounters(counters) {
        document.getElementById('ac-critical').textContent = counters.critical || 0;
        document.getElementById('ac-high').textContent     = counters.high     || 0;
        document.getElementById('ac-medium').textContent   = counters.medium   || 0;
        this._alertCounters = counters;
        this._updateSBAlerts();
    }

    // ──────────────────────── Agent Status ───────────────────────────

    _updateAgentStatus(agentName, status) {
        const map = {
            'COLLECTOR-01':  'status-collector',
            'ANALYZER-01':   'status-analyzer',
            'FORECASTER-01': 'status-forecaster',
            'ALERTMGR-01':   'status-alerts',
        };
        const elId = map[agentName];
        if (!elId) return;
        const el = document.getElementById(elId);
        if (!el) return;

        const s = (status || '').toUpperCase();
        let cls = 'idle', icon = '○';

        if (['ACTIVE', 'MONITORING', 'ALERT_ACTIVE'].includes(s)) {
            cls = 'active'; icon = '●';
        } else if (s.startsWith('COLLECTING') || s.startsWith('ANALYZING') ||
                   s.startsWith('FORECASTING') || s.startsWith('MODELING')) {
            cls = 'busy'; icon = '⧗';
        } else if (s === 'ERROR' || s === 'STOPPED') {
            cls = 'error'; icon = '✕';
        }

        el.className = `panel-status-badge ${cls}`;
        el.textContent = `${icon} ${s.length > 16 ? s.substring(0,14)+'..' : s}`;
        this._updateSBAgents();
    }

    // ──────────────────────── Toolbar Controls ────────────────────────

    _bindControls() {
        // ── Refresh
        document.getElementById('btn-refresh').addEventListener('click', () => {
            this._loadInitialState();
            Terminal.appendSystem(this.$feed, 'MANUAL REFRESH REQUESTED');
        });

        // ── Pause / Resume feed display
        document.getElementById('btn-pause').addEventListener('click', () => {
            this._paused = true;
            document.getElementById('btn-pause').style.display  = 'none';
            document.getElementById('btn-resume').style.display = '';
            Terminal.appendSystem(this.$feed, 'FEED PAUSED — DATA STILL SIMULATING IN BACKGROUND');
        });

        document.getElementById('btn-resume').addEventListener('click', () => {
            this._paused = false;
            document.getElementById('btn-pause').style.display  = '';
            document.getElementById('btn-resume').style.display = 'none';
            Terminal.appendSystem(this.$feed, 'FEED RESUMED');
        });

        // ── Clear Alerts
        document.getElementById('btn-clear-alerts').addEventListener('click', () => {
            this._clearAlerts();
        });

        // ── Force Collect
        document.getElementById('btn-force-collect').addEventListener('click', () => {
            Terminal.appendSystem(this.$feed, 'FORCE COLLECT — COLLECTOR RESTARTED (SIMULATION)');
        });

        // ── Forecast country selector
        this.$fcSelect.addEventListener('change', () => {
            this._selectedCountry = this.$fcSelect.value;
            if (this._selectedCountry && this._forecastData[this._selectedCountry]) {
                this._renderForecast(this._forecastData[this._selectedCountry]);
            }
        });

        // ── Title bar: Minimize
        document.getElementById('btn-minimize').addEventListener('click', () => {
            const w = document.getElementById('main-window');
            if (w.classList.contains('minimized')) {
                w.classList.remove('minimized');
            } else {
                w.classList.add('minimized');
            }
        });

        // ── Title bar: Maximize / Restore
        document.getElementById('btn-maximize').addEventListener('click', () => {
            const w = document.getElementById('main-window');
            this._maximized = !this._maximized;
            if (this._maximized) {
                w.style.inset = '0px';
                document.getElementById('btn-maximize').textContent = '❐';
                document.getElementById('btn-maximize').title = 'Restore';
            } else {
                w.style.inset = '6px';
                document.getElementById('btn-maximize').textContent = '□';
                document.getElementById('btn-maximize').title = 'Maximize';
            }
        });

        // ── Title bar: Close (confirm dialog)
        document.getElementById('btn-close').addEventListener('click', () => {
            this._showModal(
                'CLOSE RISKPULSE',
                'Shut down the RiskPulse Intelligence Dashboard?\n\nAll agent monitoring will stop.',
                () => { window.location.href = 'about:blank'; }
            );
        });

        // ── Modal OK / Cancel / X
        document.getElementById('modal-ok').addEventListener('click', () => {
            if (this._modalCallback) this._modalCallback();
            this._closeModal();
        });
        document.getElementById('modal-cancel').addEventListener('click', () => this._closeModal());
        document.getElementById('modal-close-btn').addEventListener('click', () => this._closeModal());
        document.getElementById('modal-overlay').addEventListener('click', e => {
            if (e.target === document.getElementById('modal-overlay')) this._closeModal();
        });

        // ── Close all dropdowns when clicking outside
        document.addEventListener('click', e => {
            if (!e.target.closest('.menu-item') && !e.target.closest('.dropdown')) {
                this._closeAllDropdowns();
            }
        });

        // ── Keyboard shortcuts
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') {
                this._closeAllDropdowns();
                this._closeModal();
            }
            if (e.key === 'F5') { e.preventDefault(); this._loadInitialState(); }
        });
    }

    // ──────────────────────── Menu System ────────────────────────────

    _bindMenus() {
        const menuMap = {
            'menu-file':    'dd-file',
            'menu-view':    'dd-view',
            'menu-agents':  'dd-agents',
            'menu-reports': 'dd-reports',
            'menu-help':    'dd-help',
        };

        // Open dropdown on click
        Object.entries(menuMap).forEach(([menuId, ddId]) => {
            const menuEl = document.getElementById(menuId);
            const ddEl   = document.getElementById(ddId);
            if (!menuEl || !ddEl) return;

            menuEl.addEventListener('click', e => {
                e.stopPropagation();
                const isOpen = ddEl.classList.contains('open');
                this._closeAllDropdowns();
                if (!isOpen) {
                    const rect = menuEl.getBoundingClientRect();
                    ddEl.style.left = rect.left + 'px';
                    ddEl.style.top  = (rect.bottom) + 'px';
                    ddEl.classList.add('open');
                    menuEl.classList.add('active');
                    this._currentMenuId = menuId;
                }
            });
        });

        // ── FILE menu actions
        this._ddAction('dd-export-log', () => {
            const lines = Array.from(document.querySelectorAll('#feed-body .t-line'))
                .map(l => l.innerText).join('\n');
            this._downloadText('riskpulse_event_log.txt', lines);
        });

        this._ddAction('dd-export-alerts', () => {
            const lines = Array.from(document.querySelectorAll('#alerts-list .alert-line'))
                .map(l => l.innerText).join('\n');
            this._downloadText('riskpulse_alerts.txt', lines);
        });

        this._ddAction('dd-clear-feed', () => {
            this.$feed.innerHTML = '<div class="t-line dim"><span class="t-msg">FEED CLEARED</span></div>';
            Terminal.appendSystem(this.$feed, 'EVENT FEED CLEARED BY USER');
        });

        this._ddAction('dd-exit', () => {
            document.getElementById('btn-close').click();
        });

        // ── VIEW menu: toggle panels
        const panelToggleMap = {
            'dd-toggle-feed':      'panel-collector',
            'dd-toggle-sentiment': 'panel-analyzer',
            'dd-toggle-alerts':    'panel-alerts',
            'dd-toggle-forecast':  'panel-forecaster',
        };
        Object.entries(panelToggleMap).forEach(([ddItemId, panelId]) => {
            this._ddAction(ddItemId, () => {
                const el   = document.getElementById(panelId);
                const item = document.getElementById(ddItemId);
                if (!el) return;
                const hidden = el.classList.toggle('panel-hidden');
                item.textContent = (hidden ? '   ' : '✔ ') + item.textContent.replace(/^[✔\s]+/, '');
                this._reflowGrid();
            });
        });

        this._ddAction('dd-autoscroll', () => {
            this._autoScroll = !this._autoScroll;
            const item = document.getElementById('dd-autoscroll');
            item.textContent = (this._autoScroll ? '✔ ' : '   ') + 'Auto-Scroll Feed';
        });

        // ── AGENTS menu
        this._ddAction('dd-start-all', () => this._controlAllAgents('start'));
        this._ddAction('dd-stop-all',  () => this._controlAllAgents('stop'));
        this._ddAction('dd-restart-all', () => this._controlAllAgents('restart'));

        const agentRestartMap = {
            'dd-restart-collector':  'collector',
            'dd-restart-analyzer':   'analyzer',
            'dd-restart-forecaster': 'forecaster',
            'dd-restart-alertmgr':   'alerts',
        };
        Object.entries(agentRestartMap).forEach(([ddId, agentKey]) => {
            this._ddAction(ddId, () => {
                Terminal.appendSystem(this.$feed, `RESTARTING AGENT: ${agentKey.toUpperCase()} (SIMULATION)`);
            });
        });

        // ── REPORTS menu
        this._ddAction('dd-show-stats', () => {
            const agents = this._mockAgents;
            const lines = Object.values(agents).map(a =>
                `${(a.name||'??').padEnd(16)} STATUS: ${(a.status||'??').padEnd(12)} CYCLES: ${a.cycles||0}  ERRORS: ${a.errors||0}  LAST: ${a.last_run ? a.last_run.substring(11,19) : '--'}`
            ).join('\n');
            this._showModal('AGENT STATISTICS', lines, null, false);
        });

        this._ddAction('dd-show-risk', () => {
            const riskLines = Object.entries(this._forecastData).map(([cc, f]) => {
                const risk = (f.risk_score * 100).toFixed(0);
                const bar  = '█'.repeat(Math.round(f.risk_score * 20)).padEnd(20, '░');
                return `${cc.padEnd(4)} [${bar}] ${risk}%  BASELINE: ${(f.baseline||0).toFixed(0)}`;
            }).join('\n') || 'No forecast data yet. Wait for the Forecaster agent to run.';
            this._showModal('RISK SUMMARY — ALL COUNTRIES', riskLines, null, false);
        });

        this._ddAction('dd-show-history', () => {
            const alerts = this._mockAlerts.slice(-50);
            const lines = alerts.map(a =>
                `[${(a.triggered_at||'').substring(11,19)}] ${(a.severity||'').toUpperCase().padEnd(9)} ${(a.country||'??').padEnd(4)} ${a.alert_type}: ${a.message}`
            ).join('\n') || 'No alerts recorded yet.';
            this._showModal('ALERT HISTORY (LAST 50)', lines, null, false);
        });

        // ── HELP menu
        this._ddAction('dd-about', () => {
            this._showModal('ABOUT RISKPULSE',
`RISKPULSE INTELLIGENCE v1.0
Geopolitical Analysis System

Multi-agent conflict risk monitoring dashboard.

AGENTS:
  COLLECTOR-01   Data ingestion (GDELT/ACLED/Reddit)
  ANALYZER-01    Sentiment analysis engine
  FORECASTER-01  7-day ensemble forecast (ARIMA+Prophet+LSTM)
  ALERTMGR-01    Alert conditions & notifications

DATA SOURCES:
  GDELT     Global event database (free, no key)
  ACLED     Armed Conflict Location & Event Data
  Reddit    Social media signal extraction

MODE: STATIC SIMULATION (No backend required)
`, null, false);
        });

        this._ddAction('dd-shortcuts', () => {
            this._showModal('KEYBOARD SHORTCUTS',
`F5              Refresh dashboard
Escape          Close menus / dialog
Space           [toolbar] Pause/Resume feed
`, null, false);
        });
    }

    // ──────────────────────── Dropdown Helpers ────────────────────────

    _closeAllDropdowns() {
        document.querySelectorAll('.dropdown.open').forEach(d => d.classList.remove('open'));
        document.querySelectorAll('.menu-item.active').forEach(m => m.classList.remove('active'));
        this._currentMenuId = null;
    }

    _ddAction(id, fn) {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('click', e => {
            e.stopPropagation();
            this._closeAllDropdowns();
            fn();
        });
    }

    // ──────────────────────── Modal ──────────────────────────────────

    _showModal(title, body, okCallback = null, showCancel = true) {
        this.$modalTitle.textContent = title;
        this.$modalBody.textContent  = body;
        this._modalCallback = okCallback;
        document.getElementById('modal-cancel').style.display = showCancel ? '' : 'none';
        this.$modal.style.display = 'flex';
    }

    _closeModal() {
        this.$modal.style.display = 'none';
        this._modalCallback = null;
    }

    // ──────────────────────── Agent API helpers ───────────────────────

    _controlAllAgents(action) {
        ['collector','analyzer','forecaster','alerts'].forEach(key => {
            Terminal.appendSystem(this.$feed, `AGENT ${key.toUpperCase()}: ${action.toUpperCase()} (SIMULATION)`);
        });
    }

    // ──────────────────────── Misc helpers ───────────────────────────

    _clearAlerts() {
        this.$alertsList.innerHTML = '<div class="t-line dim"><span class="t-msg">ALERT HISTORY CLEARED</span></div>';
        this._alertsFired = 0;
        this._alertCounters = { critical: 0, high: 0, medium: 0 };
        this._updateAlertCounters(this._alertCounters);
        document.getElementById('metric-alerts-fired').textContent = '0';
    }

    _reflowGrid() {
        const content = document.getElementById('content');
        const visible = Array.from(content.querySelectorAll('.panel:not(.panel-hidden)')).length;
        // Adjust grid columns based on visible count
        if (visible === 1)      content.style.gridTemplateColumns = '1fr';
        else if (visible <= 2)  content.style.gridTemplateColumns = '1fr 1fr';
        else                    content.style.gridTemplateColumns = '1fr 1fr';
        content.style.gridTemplateRows = visible <= 2 ? '1fr' : '1fr 1fr';
    }

    _downloadText(filename, text) {
        const blob = new Blob([text], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        a.click();
        Terminal.appendSystem(this.$feed, `EXPORTED: ${filename}`);
    }

    _startClock() {
        const update = () => {
            this.$clock && (this.$clock.textContent =
                new Date().toISOString().replace('T',' ').substring(0,19) + ' UTC');
        };
        update();
        setInterval(update, 1000);
    }

    _updateEventsTotal() {
        document.getElementById('tb-events-total').textContent = `EVENTS: ${this._totalEvents}`;
    }

    _refreshMetrics() {
        document.getElementById('metric-gdelt').textContent  = this._gdeltCount;
        document.getElementById('metric-acled').textContent  = this._acledCount;
        document.getElementById('metric-reddit').textContent = this._redditCount;
        document.getElementById('metric-total').textContent  = this._totalEvents;
    }

    _setSBSSE(txt, cls) {
        const el = document.getElementById('sb-sse');
        if (!el) return;
        el.textContent = `SSE: ${txt}`;
        el.className = `sb-seg ${cls || 'dim'}`;
    }

    _updateSBAlerts() {
        const c = this._alertCounters;
        const total = (c.critical||0) + (c.high||0) + (c.medium||0);
        const el = document.getElementById('sb-alerts');
        if (el) {
            el.textContent = `ALERTS: ${total}`;
            el.className = `sb-seg ${total > 0 ? (c.critical > 0 ? 'alert' : 'warn') : 'ok'}`;
        }
        document.getElementById('tb-alerts-count').textContent = `ALERTS: ${total}`;
    }

    _updateSBAgents() {
        const ids = ['status-collector','status-analyzer','status-forecaster','status-alerts'];
        const active = ids.filter(id => {
            const el = document.getElementById(id);
            return el && !el.textContent.includes('✕') && !el.textContent.includes('STOPPED');
        }).length;
        const el = document.getElementById('sb-agents');
        if (el) el.textContent = `AGENTS: ${active}/4 ACTIVE`;
    }

    _beep() {
        try {
            const ctx  = new (window.AudioContext || window.webkitAudioContext)();
            const osc  = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'square';
            osc.frequency.value = 880;
            gain.gain.setValueAtTime(0.05, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.15);
        } catch (e) { /* audio not supported */ }
    }
}

// ─── Boot ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new RiskPulseDashboard();
});
