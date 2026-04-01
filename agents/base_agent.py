import threading
import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for all RiskPulse agents."""

    def __init__(self, name, message_bus, db):
        self.name = name
        self.message_bus = message_bus
        self.db = db
        self.status = 'IDLE'
        self.running = False
        self._thread = None
        self.logger = logging.getLogger(f'Agent.{name}')
        self._cycle_count = 0
        self._error_count = 0
        self._last_run = None

        # Register subscriptions
        for topic in self.get_subscriptions():
            self.message_bus.subscribe(topic, self.handle_message)

    # ──────────────────────── Abstract interface ────────────────────────

    @abstractmethod
    def get_subscriptions(self) -> list:
        """Return list of topic patterns this agent subscribes to."""
        pass

    @abstractmethod
    def handle_message(self, topic: str, data: dict):
        """Handle an incoming message from the bus."""
        pass

    @abstractmethod
    def execute_cycle(self):
        """Main work unit — called periodically by the run loop."""
        pass

    @abstractmethod
    def get_cycle_interval(self) -> float:
        """Seconds to sleep between execute_cycle calls."""
        pass

    # ──────────────────────── Lifecycle ────────────────────────

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(
            target=self._run_loop,
            name=f'Agent-{self.name}',
            daemon=True
        )
        self._thread.start()
        self.logger.info(f'{self.name} started')
        self.set_status('ACTIVE')

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        self.logger.info(f'{self.name} stopped')
        self.set_status('STOPPED')

    def _run_loop(self):
        while self.running:
            try:
                self._last_run = datetime.utcnow()
                self.execute_cycle()
                self._cycle_count += 1
            except Exception as e:
                self._error_count += 1
                self.logger.error(f'Cycle error: {e}', exc_info=True)
                self.publish_event(f'agent.{self.name}.error', {
                    'error': str(e),
                    'cycle': self._cycle_count
                })

            time.sleep(self.get_cycle_interval())

    # ──────────────────────── Helpers ────────────────────────

    def set_status(self, status: str):
        self.status = status
        self.message_bus.publish(f'agent.{self.name}.status', {
            'agent': self.name,
            'status': status,
            'cycles': self._cycle_count,
            'errors': self._error_count
        })

    def publish_event(self, topic: str, data: dict):
        data['agent'] = self.name
        self.message_bus.publish(topic, data)

    def get_info(self) -> dict:
        return {
            'name': self.name,
            'status': self.status,
            'cycles': self._cycle_count,
            'errors': self._error_count,
            'last_run': self._last_run.isoformat() if self._last_run else None,
            'running': self.running
        }
