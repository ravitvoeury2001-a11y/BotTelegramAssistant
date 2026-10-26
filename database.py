"""Asynchronous SQLite database interface for user settings and conversation history."""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import aiosqlite

from config import config

logger = logging.getLogger(__name__)


class Database:
    """Manages SQLite database connections and queries using aiosqlite."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or config.database_path

    async def init_db(self) -> None:
        """Initialize database schema and tables."""
        # Ensure parent directory exists
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
                """
            )

            # Create index for fast message retrieval by user
            await db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_messages_user_id_id 
                ON messages(user_id, id);
                """
            )

            await db.commit()
            logger.info("Database schema initialized at %s", self.db_path)

    async def upsert_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        language: Optional[str] = None,
    ) -> None:
        """Insert or update user record with active timestamp."""
        now = datetime.now(timezone.utc).isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            if language is not None:
                await db.execute(
                    """
                    INSERT INTO users (user_id, username, first_name, language, last_active_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username = excluded.username,
                        first_name = excluded.first_name,
                        language = excluded.language,
                        last_active_at = excluded.last_active_at;
                    """,
                    (user_id, username, first_name, language, now),
                )
            else:
                await db.execute(
                    """
                    INSERT INTO users (user_id, username, first_name, last_active_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username = excluded.username,
                        first_name = excluded.first_name,
                        last_active_at = excluded.last_active_at;
                    """,
                    (user_id, username, first_name, now),
                )
            await db.commit()

    async def get_user_language(self, user_id: int) -> str:
        """Get the user's preferred language code (default: 'en')."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT language FROM users WHERE user_id = ?;", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    return str(row[0])
                return "en"

    async def set_user_language(self, user_id: int, language: str) -> None:
        """Update the user's preferred language."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE users SET language = ? WHERE user_id = ?;
                """,
                (language, user_id),
            )
            await db.commit()

    async def save_message(self, user_id: int, role: str, content: str) -> None:
        """Save a message in conversation history."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO messages (user_id, role, content)
                VALUES (?, ?, ?);
                """,
                (user_id, role, content),
            )
            await db.commit()

    async def get_conversation_history(
        self, user_id: int, limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Fetch recent conversation history for a user, ordered from oldest to newest.

        Args:
            user_id: Telegram user ID.
            limit: Maximum number of recent messages to return.

        Returns:
            List of dicts with 'role' and 'content'.
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Query recent messages in descending order, then reverse to chronological order
            async with db.execute(
                """
                SELECT role, content FROM (
                    SELECT role, content, id FROM messages
                    WHERE user_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                ) ORDER BY id ASC;
                """,
                (user_id, limit),
            ) as cursor:
                rows = await cursor.fetchall()
                return [{"role": row[0], "content": row[1]} for row in rows]

    async def get_user_history_count(self, user_id: int) -> int:
        """Get total number of stored messages for a user."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM messages WHERE user_id = ?;", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return int(row[0]) if row else 0

    async def clear_conversation_history(self, user_id: int) -> int:
        """Clear all stored messages for a specific user."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM messages WHERE user_id = ?;", (user_id,)
            )
            deleted_count = cursor.rowcount
            await db.commit()
            return deleted_count

    async def get_all_user_ids(self) -> List[int]:
        """Fetch all registered user IDs for broadcasts."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT user_id FROM users;") as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics for admin report."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM users;") as cursor:
                total_users = (await cursor.fetchone())[0]

            async with db.execute(
                """
                SELECT COUNT(*) FROM users 
                WHERE last_active_at >= datetime('now', '-1 day');
                """
            ) as cursor:
                active_users = (await cursor.fetchone())[0]

            async with db.execute("SELECT COUNT(*) FROM messages;") as cursor:
                total_messages = (await cursor.fetchone())[0]

            return {
                "total_users": total_users,
                "active_users": active_users,
                "total_messages": total_messages,
            }


# Default singleton instance
db = Database()
