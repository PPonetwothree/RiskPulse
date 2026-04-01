from collectors.simulator import generate_reddit_posts


class RedditCollector:
    """Reddit collector. Uses simulation by default."""

    def __init__(self, config):
        self.config = config
        self.use_simulation = config.get('use_simulation', True)

    def fetch_posts(self):
        if self.use_simulation:
            return generate_reddit_posts()
        raise NotImplementedError("Real Reddit fetch not configured")
