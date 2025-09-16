import json
from django.core.cache import cache

class RedisQueue:
    def __init__(self, name="default_queue", timeout=None):
        """
        :param name: queue name
        :param timeout: optional TTL (in seconds) for the queue key
        """
        self.key = f"queue:{name}"
        self.timeout = timeout
        self.client = cache.client.get_client(write=True)  # direct redis client

    def _set_expiry(self):
        """Apply timeout if configured."""
        if self.timeout:
            self.client.expire(self.key, self.timeout)

    def add_task(self, task):
        """Add task at the end (FIFO)."""
        self.client.rpush(self.key, json.dumps(task))
        self._set_expiry()

    def add_priority_task(self, task):
        """Add task at the front (priority)."""
        self.client.lpush(self.key, json.dumps(task))
        self._set_expiry()

    def get_task(self):
        """Get and remove task from the front (FIFO)."""
        raw = self.client.lpop(self.key)
        return json.loads(raw) if raw else None

    def peek_all(self):
        """View all tasks without removing them."""
        raw_list = self.client.lrange(self.key, 0, -1)
        return [json.loads(item) for item in raw_list]

    def clear_queue(self):
        """Clear the queue."""
        self.client.delete(self.key)

    def ttl(self):
        """Check how many seconds until expiry (-1 = no expiry, -2 = key not found)."""
        return self.client.ttl(self.key)
