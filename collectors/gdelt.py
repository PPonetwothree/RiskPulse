from collectors.simulator import generate_gdelt_events


class GDELTCollector:
    """GDELT data collector. Uses simulation by default."""

    def __init__(self, config):
        self.config = config
        self.use_simulation = config.get('use_simulation', True)

    def fetch_latest(self):
        if self.use_simulation:
            return generate_gdelt_events()
        # Real GDELT fetch would go here
        raise NotImplementedError("Real GDELT fetch not configured")
