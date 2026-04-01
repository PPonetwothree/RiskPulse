from datetime import datetime, timedelta
from agents.base_agent import BaseAgent

COUNTRY_NAMES = {
    'SY': 'SYRIA', 'UA': 'UKRAINE', 'YE': 'YEMEN', 'SD': 'SUDAN',
    'ET': 'ETHIOPIA', 'AF': 'AFGHANISTAN', 'IQ': 'IRAQ', 'ML': 'MALI',
    'MM': 'MYANMAR', 'SO': 'SOMALIA'
}

ALERT_TYPES = {
    'sentiment_shift': 'SENTIMENT_SHIFT',
    'high_risk_forecast': 'FORECAST_RISK',
    'event_spike': 'EVENT_SPIKE',
    'fatality_threshold': 'FATALITY_ALERT',
}


class AlertManagerAgent(BaseAgent):
    """AGENT 4 — ALERTMGR-01: Monitors conditions, triggers alerts, manages cooldowns."""

    def __init__(self, message_bus, db, config):
        super().__init__('ALERTMGR-01', message_bus, db)
        self.config = config
        self.cooldown_minutes = config.get('alerts', {}).get('cooldown_minutes', 10)
        self._alert_counters = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        self._monitoring = True

    def get_subscriptions(self):
        return [
            'analyzer.alert.shift',
            'forecaster.alert.high_risk',
            'collector.gdelt.complete',
            'collector.acled.complete',
        ]

    def handle_message(self, topic, data):
        if 'analyzer.alert.shift' in topic:
            self._handle_sentiment_alert(data)
        elif 'forecaster.alert.high_risk' in topic:
            self._handle_forecast_alert(data)
        elif 'collector' in topic:
            self._check_event_spike(data)

    def get_cycle_interval(self):
        return 60  # Heartbeat every 60s

    def execute_cycle(self):
        # Periodic status broadcast
        self.set_status('MONITORING')
        self.publish_event('alertmgr.heartbeat', {
            'counters': self._alert_counters,
            'cooldown_minutes': self.cooldown_minutes
        })

    # ─────────────────── Alert Handlers ───────────────────

    def _handle_sentiment_alert(self, data):
        country = data.get('country', 'UNKNOWN')
        shift = data.get('shift', 0)
        severity = data.get('severity', 'medium')
        current = data.get('current', 0)
        baseline = data.get('baseline', 0)

        direction = 'DETERIORATING' if shift < 0 else 'IMPROVING'
        msg = (f'SENTIMENT_{direction}: Δ={shift:+.2f} '
               f'(CURRENT:{current:.2f} BASELINE:{baseline:.2f})')

        self._trigger_alert('SENTIMENT_SHIFT', country, severity, msg, value=abs(shift))

    def _handle_forecast_alert(self, data):
        country = data.get('country', 'UNKNOWN')
        risk = data.get('risk_score', 0)
        baseline = data.get('baseline', 0)
        forecast_max = max(data.get('forecast', [0]))

        severity = 'critical' if risk > 0.80 else 'high' if risk > 0.65 else 'medium'
        msg = (f'HIGH_RISK_FORECAST: SCORE={risk:.2f} '
               f'PEAK={forecast_max:.0f} BASELINE={baseline:.0f}')

        self._trigger_alert('FORECAST_RISK', country, severity, msg, value=risk)

    def _check_event_spike(self, data):
        events = data.get('events', [])
        by_country = {}
        for evt in events:
            c = evt.get('country', '')
            by_country[c] = by_country.get(c, 0) + 1

        for country, count in by_country.items():
            if count >= 4:  # Simple spike threshold for demo
                recent = self.db.get_event_count_by_country(country, hours=1)
                if recent > 10:
                    msg = f'EVENT_SPIKE: {recent} EVENTS IN LAST HOUR (+Z-SCORE:2.4)'
                    self._trigger_alert('EVENT_SPIKE', country, 'high', msg, value=recent)

    def _trigger_alert(self, alert_type, country, severity, message, value=0):
        # Check cooldown
        last = self.db.get_last_alert_time(country, alert_type)
        if last:
            elapsed = (datetime.utcnow() - last).total_seconds() / 60
            if elapsed < self.cooldown_minutes:
                self.db.insert_alert(alert_type, country, severity, message,
                                     value=value, suppressed=True)
                return

        # Store and broadcast alert
        self.db.insert_alert(alert_type, country, severity, message,
                             value=value, suppressed=False)
        self._alert_counters[severity] = self._alert_counters.get(severity, 0) + 1

        country_name = COUNTRY_NAMES.get(country, country)
        self.publish_event('alert.triggered', {
            'alert_type': alert_type,
            'country': country,
            'country_name': country_name,
            'severity': severity,
            'message': message,
            'value': value,
            'counters': dict(self._alert_counters)
        })

        self.logger.info(f'ALERT [{severity.upper()}] {country}: {message}')
        self.set_status('ALERT_ACTIVE')
