import random
import time
from datetime import datetime
from collections import defaultdict
from agents.base_agent import BaseAgent

COUNTRIES = ['SY', 'UA', 'YE', 'SD', 'ET', 'AF', 'IQ', 'ML', 'MM', 'SO']

# Simulated baselines (long-term average sentiment per country)
BASELINES = {
    'SY': 0.18, 'UA': 0.22, 'YE': 0.20, 'SD': 0.28,
    'ET': 0.30, 'AF': 0.22, 'IQ': 0.32, 'ML': 0.29,
    'MM': 0.26, 'SO': 0.24,
}


class AnalyzerAgent(BaseAgent):
    """AGENT 2 — ANALYZER-01: Simulated sentiment analysis on collected events."""

    def __init__(self, message_bus, db, config):
        super().__init__('ANALYZER-01', message_bus, db)
        self.config = config
        self.threshold = config.get('sentiment', {}).get('shift_alert_threshold', 0.25)
        self.interval = config.get('sentiment', {}).get('analysis_interval', 30)

        self._pending = False
        self._items_analyzed = 0

    def get_subscriptions(self):
        return ['collector.*.complete']

    def handle_message(self, topic, data):
        self._pending = True

    def get_cycle_interval(self):
        return self.interval

    def execute_cycle(self):
        if not self._pending:
            return

        self._pending = False
        self.set_status('ANALYZING')

        try:
            # Get unprocessed events
            events = self.db.get_unprocessed_events(limit=200)
            if not events:
                self.set_status('IDLE')
                return

            # Group by country
            by_country = defaultdict(list)
            for evt in events:
                if evt['country'] in COUNTRIES:
                    by_country[evt['country']].append(evt.get('sentiment_score', 0.5))

            countries_data = []
            for country, scores in by_country.items():
                current = sum(scores) / len(scores)
                baseline = BASELINES.get(country, 0.3)

                # Add small drift to simulate dynamic change
                drift = random.gauss(0, 0.03)
                current = max(0.0, min(1.0, current + drift))

                shift = current - baseline
                count = len(scores)

                self.db.insert_sentiment(country, current, baseline, shift, count)
                self._items_analyzed += count

                country_info = {
                    'code': country,
                    'current': round(current, 3),
                    'baseline': round(baseline, 3),
                    'shift': round(shift, 3),
                    'count': count,
                    'severity': self._classify_shift(shift)
                }
                countries_data.append(country_info)

                # Trigger alert if shift is significant
                if abs(shift) >= self.threshold:
                    self.publish_event('analyzer.alert.shift', {
                        'country': country,
                        'shift': round(shift, 3),
                        'current': round(current, 3),
                        'baseline': round(baseline, 3),
                        'severity': self._classify_shift(shift),
                        'count': count
                    })

            # Mark events processed
            ids = [e['id'] for e in events]
            self.db.mark_events_processed(ids)

            # Sort by |shift| desc
            countries_data.sort(key=lambda x: abs(x['shift']), reverse=True)

            self.publish_event('analyzer.sentiment.complete', {
                'countries': countries_data,
                'total_analyzed': self._items_analyzed
            })

        except Exception as e:
            self.logger.error(f'Analysis failed: {e}', exc_info=True)
        finally:
            self.set_status('IDLE')

    def _classify_shift(self, shift):
        abs_shift = abs(shift)
        if abs_shift > 0.4:
            return 'critical'
        elif abs_shift > 0.25:
            return 'high'
        elif abs_shift > 0.15:
            return 'medium'
        return 'low'
