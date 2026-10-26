"""Tests for the RateLimiter utility."""

import time
from utils.rate_limiter import RateLimiter


def test_rate_limiter_allows_first_request():
    """Initial request from any user should always be allowed."""
    limiter = RateLimiter(cooldown_seconds=1.0)
    allowed, wait = limiter.is_allowed(user_id=123)
    assert allowed is True
    assert wait == 0.0


def test_rate_limiter_blocks_immediate_repeat():
    """Rapid repeated requests within cooldown should be blocked."""
    limiter = RateLimiter(cooldown_seconds=1.0)
    allowed1, _ = limiter.is_allowed(user_id=123)
    assert allowed1 is True

    allowed2, wait2 = limiter.is_allowed(user_id=123)
    assert allowed2 is False
    assert wait2 > 0.0


def test_rate_limiter_allows_different_users():
    """Requests from different users should not block each other."""
    limiter = RateLimiter(cooldown_seconds=2.0)
    allowed_user1, _ = limiter.is_allowed(user_id=101)
    allowed_user2, _ = limiter.is_allowed(user_id=202)

    assert allowed_user1 is True
    assert allowed_user2 is True


def test_rate_limiter_reset():
    """Resetting the limiter clears the user history."""
    limiter = RateLimiter(cooldown_seconds=5.0)
    limiter.is_allowed(user_id=303)
    assert limiter.is_allowed(user_id=303)[0] is False

    limiter.reset(user_id=303)
    assert limiter.is_allowed(user_id=303)[0] is True
