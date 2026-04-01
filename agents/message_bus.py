import queue
import threading
import json
import fnmatch
import logging
from datetime import datetime

logger = logging.getLogger('riskpulse.message_bus')


class MessageBus:
    """
    In-process pub/sub message bus using Python queues.
    Provides a Redis PubSub-compatible interface without requiring Redis.
    Supports wildcard topic patterns (e.g. 'collector.*').
    """

    def __init__(self):
        self.handlers = {}   # topic_pattern -> [callback, ...]
        self._lock = threading.RLock()
        self._queue = queue.Queue()
        self._running = False
        self._listener_thread = None

        # SSE broadcast queue (for Flask SSE endpoint)
        self.sse_queue = queue.Queue(maxsize=500)

    def subscribe(self, topic_pattern, handler):
        """Subscribe a handler to a topic pattern (supports * wildcards)."""
        with self._lock:
            if topic_pattern not in self.handlers:
                self.handlers[topic_pattern] = []
            self.handlers[topic_pattern].append(handler)

    def publish(self, topic, data):
        """Publish data dict to a topic."""
        if not isinstance(data, dict):
            data = {'value': data}
        data.setdefault('timestamp', datetime.utcnow().isoformat())

        message = {'topic': topic, 'data': data}
        self._queue.put(message)

        # Also put in SSE queue for real-time frontend updates
        try:
            self.sse_queue.put_nowait(message)
        except queue.Full:
            # Drop oldest
            try:
                self.sse_queue.get_nowait()
                self.sse_queue.put_nowait(message)
            except queue.Empty:
                pass

    def start_listening(self):
        """Start background dispatcher thread."""
        self._running = True
        self._listener_thread = threading.Thread(
            target=self._dispatch_loop,
            name='MessageBus-Dispatcher',
            daemon=True
        )
        self._listener_thread.start()
        logger.info('MessageBus started')

    def stop_listening(self):
        self._running = False

    def _dispatch_loop(self):
        while self._running:
            try:
                message = self._queue.get(timeout=0.1)
                self._dispatch(message)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f'Dispatch error: {e}')

    def _dispatch(self, message):
        topic = message['topic']
        data = message['data']

        with self._lock:
            handlers_copy = dict(self.handlers)

        for pattern, handlers in handlers_copy.items():
            if fnmatch.fnmatch(topic, pattern):
                for handler in handlers:
                    try:
                        handler(topic, data)
                    except Exception as e:
                        logger.error(f'Handler error for {topic}: {e}')
