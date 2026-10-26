"""Rate limiter to prevent user spamming and flooding."""

import time
from typing import Dict, Tuple, Optional


class RateLimiter:
    """Simple in-memory rate limiter enforcing a cooldown between user actions."""

    def __init__(self, cooldown_seconds: float = 2.0) -> None:
        self.cooldown_seconds = cooldown_seconds
        self._last_action: Dict[int, float] = {}

    def is_allowed(self, user_id: int) -> Tuple[bool, float]:
        """
        Check if a user is allowed to perform an action.

        Args:
            user_id: The Telegram user ID.

        Returns:
            Tuple of (is_allowed: bool, wait_seconds: float).
        """
        now = time.monotonic()
        last_time = self._last_action.get(user_id, 0.0)
        elapsed = now - last_time

        if elapsed >= self.cooldown_seconds:
            self._last_action[user_id] = now
            return True, 0.0

        remaining = self.cooldown_seconds - elapsed
        return False, round(remaining, 1)

    def reset(self, user_id: Optional[int] = None) -> None:
        """Clear rate limit history for a specific user or everyone."""
        if user_id is not None:
            self._last_action.pop(user_id, None)
        else:
            self._last_action.clear()
