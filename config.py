"""Configuration manager for Telegram Bot Assistant."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Automatically load environment variables from .env file if it exists
load_dotenv(dotenv_path=BASE_DIR / ".env")


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # Telegram Bot Token (required to connect with Telegram Bot API)
    telegram_bot_token: str = field(
        default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    )

    # Telegram Bot Username (optional)
    telegram_bot_username: str = field(
        default_factory=lambda: os.getenv("TELEGRAM_BOT_USERNAME", "").strip()
    )

    # Telegram Running Mode (polling or webhook)
    telegram_mode: str = field(
        default_factory=lambda: os.getenv("TELEGRAM_MODE", "polling").strip()
    )

    # AI API Key (supports AI_API_KEY and OPENAI_API_KEY)
    openai_api_key: Optional[str] = field(
        default_factory=lambda: (
            os.getenv("AI_API_KEY", "").strip()
            or os.getenv("OPENAI_API_KEY", "").strip()
            or None
        )
    )

    # AI Model (supports AI_MODEL and OPENAI_MODEL)
    openai_model: str = field(
        default_factory=lambda: (
            os.getenv("AI_MODEL", "").strip()
            or os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
        )
    )

    # AI Base URL (optional - e.g. https://api.deepseek.com for DeepSeek)
    ai_base_url: Optional[str] = field(
        default_factory=lambda: (
            os.getenv("AI_BASE_URL", "").strip()
            or os.getenv("OPENAI_BASE_URL", "").strip()
            or None
        )
    )

    # Admin Panel Credentials
    admin_username: str = field(
        default_factory=lambda: os.getenv("ADMIN_USERNAME", "admin").strip()
    )
    admin_password: str = field(
        default_factory=lambda: os.getenv("ADMIN_PASSWORD", "admin123456").strip()
    )

    # Database URL & Credentials (PostgreSQL / SQLite)
    database_url: Optional[str] = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "").strip() or None
    )
    database_username: Optional[str] = field(
        default_factory=lambda: os.getenv("DATABASE_USERNAME", "").strip() or None
    )
    database_password: Optional[str] = field(
        default_factory=lambda: os.getenv("DATABASE_PASSWORD", "").strip() or None
    )

    # Redis URL (Optional)
    redis_url: Optional[str] = field(
        default_factory=lambda: os.getenv("REDIS_URL", "").strip() or None
    )

    # Administrator Telegram User IDs
    admin_ids: List[int] = field(default_factory=list)

    # Database file path
    database_path: str = field(
        default_factory=lambda: os.getenv("DATABASE_PATH", str(BASE_DIR / "bot_assistant.db")).strip()
    )

    # Rate limiting in seconds (cooldown per user)
    rate_limit_seconds: float = field(
        default_factory=lambda: float(os.getenv("RATE_LIMIT_SECONDS", "2.0"))
    )

    # Maximum conversation history to retain for context
    max_memory_messages: int = field(
        default_factory=lambda: int(os.getenv("MAX_MEMORY_MESSAGES", "10"))
    )

    # Logging level
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper().strip()
    )

    def __post_init__(self) -> None:
        """Parse admin IDs from environment variable string."""
        raw_admins = os.getenv("ADMIN_IDS", "")
        parsed: List[int] = []
        for item in raw_admins.split(","):
            cleaned = item.strip()
            if cleaned and cleaned.isdigit():
                parsed.append(int(cleaned))
        self.admin_ids = parsed

    def is_admin(self, user_id: int) -> bool:
        """Check if a specific user ID is authorized as an administrator."""
        return user_id in self.admin_ids

    def validate(self) -> List[str]:
        """Validate configuration settings and return a list of error/warning messages."""
        errors: List[str] = []
        placeholder_tokens = [
            "your_telegram_bot_token_here",
            "your_bot_token_here",
            "PUT_YOUR_TOKEN_HERE",
            "",
        ]

        if not self.telegram_bot_token or self.telegram_bot_token in placeholder_tokens:
            errors.append(
                "TELEGRAM_BOT_TOKEN is missing or set to placeholder. "
                "Please configure your real token from @BotFather in .env"
            )
        elif ":" not in self.telegram_bot_token:
            errors.append(
                "TELEGRAM_BOT_TOKEN format appears invalid (expected format: 123456789:ABCdef...)"
            )

        return errors


# Global config singleton
config = Config()
