import time
import threading
from typing import Dict, List, Tuple

class InMemoryRateLimiter:
    """
    Thread-safe in-memory sliding-window rate limiter for brute-force protection.
    Tracks timestamps of failed attempts per key (e.g. email or client IP)
    and enforces temporary lockouts when threshold is reached.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._attempts: Dict[str, List[float]] = {}

    def is_rate_limited(self, key: str, max_attempts: int, window_seconds: int) -> Tuple[bool, int]:
        """
        Checks whether the given key has exceeded max_attempts within window_seconds.
        Returns:
            Tuple[bool, int]: (is_limited, seconds_until_reset)
        """
        now = time.time()
        with self._lock:
            timestamps = self._attempts.get(key, [])
            # Filter out timestamps older than the sliding window
            valid_timestamps = [t for t in timestamps if now - t < window_seconds]
            self._attempts[key] = valid_timestamps

            if len(valid_timestamps) >= max_attempts:
                # Calculate time until the oldest attempt drops outside the window
                oldest = valid_timestamps[0]
                retry_after = max(1, int(window_seconds - (now - oldest)))
                return True, retry_after

            return False, 0

    def record_failure(self, key: str) -> None:
        """Records a failed attempt timestamp for the specified key."""
        now = time.time()
        with self._lock:
            if key not in self._attempts:
                self._attempts[key] = []
            self._attempts[key].append(now)

    def reset(self, key: str) -> None:
        """Clears recorded failures upon successful authentication."""
        with self._lock:
            self._attempts.pop(key, None)

    def clear_all(self) -> None:
        """Resets all tracked keys (useful during testing)."""
        with self._lock:
            self._attempts.clear()

# Global singleton rate limiter instance
auth_rate_limiter = InMemoryRateLimiter()

