from collectors.simulator import generate_acled_events


class ACLEDCollector:
    """ACLED data collector. Uses simulation by default."""

    def __init__(self, config):
        self.config = config
        self.use_simulation = config.get('use_simulation', True)

    def fetch_recent(self):
        if self.use_simulation:
            return generate_acled_events()
        raise NotImplementedError("Real ACLED fetch not configured")
