import time
from agents.base_agent import BaseAgent
from collectors.gdelt import GDELTCollector
from collectors.acled import ACLEDCollector
from collectors.reddit import RedditCollector


class CollectorAgent(BaseAgent):
    """AGENT 1 — COLLECTOR-01: Fetches events from GDELT, ACLED, Reddit."""

    def __init__(self, message_bus, db, config):
        super().__init__('COLLECTOR-01', message_bus, db)
        self.config = config

        self.gdelt = GDELTCollector(config.get('gdelt', {}))
        self.acled = ACLEDCollector(config.get('acled', {}))
        self.reddit = RedditCollector(config.get('reddit', {}))

        sim = config.get('simulation', {})
        self.gdelt_interval = sim.get('gdelt_interval', 20)
        self.acled_interval = sim.get('acled_interval', 60)
        self.reddit_interval = sim.get('reddit_interval', 45)

        self._last_gdelt = 0
        self._last_acled = 0
        self._last_reddit = 0

        self._collected_total = 0

    def get_subscriptions(self):
        return []  # Schedule-driven, no subscriptions

    def handle_message(self, topic, data):
        pass

    def get_cycle_interval(self):
        return 5  # Check every 5 seconds which source is due

    def execute_cycle(self):
        now = time.time()

        if now - self._last_gdelt >= self.gdelt_interval:
            self._collect_gdelt()
            self._last_gdelt = now

        if now - self._last_acled >= self.acled_interval:
            self._collect_acled()
            self._last_acled = now

        if now - self._last_reddit >= self.reddit_interval:
            self._collect_reddit()
            self._last_reddit = now

    # ───────────────────────── Collection methods ─────────────────────────

    def _collect_gdelt(self):
        self.set_status('COLLECTING_GDELT')
        try:
            events = self.gdelt.fetch_latest()
            if events:
                self.db.insert_events(events)
                self._collected_total += len(events)
                self.publish_event('collector.gdelt.complete', {
                    'count': len(events),
                    'total': self._collected_total,
                    'errors': 0,
                    'events': self._format_events_for_ui(events[:5])  # send sample to UI
                })
                self.logger.info(f'GDELT: collected {len(events)} events')
        except Exception as e:
            self.logger.error(f'GDELT collect failed: {e}')
            self.publish_event('collector.error', {'source': 'GDELT', 'error': str(e)})
        finally:
            self.set_status('IDLE')

    def _collect_acled(self):
        self.set_status('COLLECTING_ACLED')
        try:
            events = self.acled.fetch_recent()
            if events:
                self.db.insert_events(events)
                self._collected_total += len(events)
                self.publish_event('collector.acled.complete', {
                    'count': len(events),
                    'total': self._collected_total,
                    'errors': 0,
                    'events': self._format_events_for_ui(events[:3])
                })
                self.logger.info(f'ACLED: collected {len(events)} events')
        except Exception as e:
            self.logger.error(f'ACLED collect failed: {e}')
            self.publish_event('collector.error', {'source': 'ACLED', 'error': str(e)})
        finally:
            self.set_status('IDLE')

    def _collect_reddit(self):
        self.set_status('COLLECTING_REDDIT')
        try:
            posts = self.reddit.fetch_posts()
            if posts:
                self.db.insert_social_posts(posts)
                self._collected_total += len(posts)
                self.publish_event('collector.reddit.complete', {
                    'count': len(posts),
                    'total': self._collected_total,
                    'errors': 0,
                    'events': self._format_events_for_ui(posts[:3])
                })
                self.logger.info(f'Reddit: collected {len(posts)} posts')
        except Exception as e:
            self.logger.error(f'Reddit collect failed: {e}')
            self.publish_event('collector.error', {'source': 'Reddit', 'error': str(e)})
        finally:
            self.set_status('IDLE')

    def _format_events_for_ui(self, events):
        return [{
            'source': e['source'],
            'country': e['country'],
            'location': e.get('location', ''),
            'summary': e['summary'],
            'severity': e.get('severity', 'low'),
        } for e in events]
