"""Tests for configuration parsing and validation."""

import os
from config import Config


def test_config_defaults(monkeypatch):
    """Test default values when environment variables are not set."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AI_API_KEY", raising=False)
    monkeypatch.delenv("AI_MODEL", raising=False)
    monkeypatch.delenv("ADMIN_IDS", raising=False)

    cfg = Config()
    assert cfg.telegram_bot_token == ""
    assert cfg.openai_api_key is None
    assert cfg.openai_model == "gpt-4o-mini"
    assert cfg.admin_ids == []
    assert cfg.rate_limit_seconds == 2.0
    assert cfg.max_memory_messages == 10


def test_config_admin_parsing(monkeypatch):
    """Test parsing comma-separated admin IDs."""
    monkeypatch.setenv("ADMIN_IDS", "111222333, 444555666, invalid, 777")
    cfg = Config()
    assert cfg.admin_ids == [111222333, 444555666, 777]
    assert cfg.is_admin(111222333) is True
    assert cfg.is_admin(444555666) is True
    assert cfg.is_admin(999999999) is False


def test_config_validation_missing_token(monkeypatch):
    """Test validation errors when token is missing or placeholder."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    cfg = Config()
    errors = cfg.validate()
    assert len(errors) == 1
    assert "TELEGRAM_BOT_TOKEN is missing" in errors[0]

    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token_here")
    cfg2 = Config()
    errors2 = cfg2.validate()
    assert len(errors2) == 1
    assert "placeholder" in errors2[0]


def test_config_validation_invalid_format(monkeypatch):
    """Test validation when token format does not contain colon."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "invalidtokenformatwithoutcolon")
    cfg = Config()
    errors = cfg.validate()
    assert len(errors) == 1
    assert "format appears invalid" in errors[0]


def test_config_validation_valid_token(monkeypatch):
    """Test validation passes with properly structured token."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
    cfg = Config()
    errors = cfg.validate()
    assert len(errors) == 0
