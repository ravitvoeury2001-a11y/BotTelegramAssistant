"""Asynchronous tests for database persistence and queries."""

import pytest
from database import Database


@pytest.mark.asyncio
async def test_database_init_and_user_upsert(tmp_path):
    """Test schema initialization and user creation."""
    db_file = str(tmp_path / "test_bot.db")
    test_db = Database(db_path=db_file)
    await test_db.init_db()

    # Verify user upsert
    await test_db.upsert_user(user_id=12345, username="tester", first_name="John", language="en")
    lang = await test_db.get_user_language(12345)
    assert lang == "en"

    # Update language to Khmer
    await test_db.set_user_language(12345, "km")
    new_lang = await test_db.get_user_language(12345)
    assert new_lang == "km"


@pytest.mark.asyncio
async def test_database_messages_and_history(tmp_path):
    """Test saving and retrieving conversation messages with ordering and limit."""
    db_file = str(tmp_path / "test_bot.db")
    test_db = Database(db_path=db_file)
    await test_db.init_db()

    user_id = 99999
    await test_db.upsert_user(user_id=user_id, first_name="Alice")

    # Add 4 messages
    await test_db.save_message(user_id, "user", "Message 1")
    await test_db.save_message(user_id, "assistant", "Response 1")
    await test_db.save_message(user_id, "user", "Message 2")
    await test_db.save_message(user_id, "assistant", "Response 2")

    # Retrieve with limit=2 (should be Message 2 and Response 2)
    history = await test_db.get_conversation_history(user_id, limit=2)
    assert len(history) == 2
    assert history[0]["content"] == "Message 2"
    assert history[1]["content"] == "Response 2"

    count = await test_db.get_user_history_count(user_id)
    assert count == 4

    # Clear conversation history
    deleted = await test_db.clear_conversation_history(user_id)
    assert deleted == 4
    count_after = await test_db.get_user_history_count(user_id)
    assert count_after == 0


@pytest.mark.asyncio
async def test_database_stats(tmp_path):
    """Test system statistics calculation."""
    db_file = str(tmp_path / "test_bot.db")
    test_db = Database(db_path=db_file)
    await test_db.init_db()

    await test_db.upsert_user(user_id=1, first_name="U1")
    await test_db.upsert_user(user_id=2, first_name="U2")
    await test_db.save_message(1, "user", "Hello")
    await test_db.save_message(1, "assistant", "Hi")

    stats = await test_db.get_stats()
    assert stats["total_users"] == 2
    assert stats["active_users"] == 2
    assert stats["total_messages"] == 2
