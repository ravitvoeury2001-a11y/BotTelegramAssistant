"""Tests for AI Service responses, offline fallback, and multilingual logic."""

import pytest
from services.ai_service import AIService


@pytest.mark.asyncio
async def test_offline_assistant_greetings_english():
    """Verify offline assistant responds to English greetings."""
    ai = AIService()
    ai._client = None
    response = await ai.generate_response(prompt="Hello there!", language="en")
    assert "Telegram Assistant Bot" in response
    assert "assist" in response.lower()


@pytest.mark.asyncio
async def test_offline_assistant_greetings_khmer():
    """Verify offline assistant responds to Khmer greetings."""
    ai = AIService()
    ai._client = None
    response = await ai.generate_response(prompt="សួស្ដីបាទ", language="km")
    assert "សួស្ដី" in response
    assert "Telegram Assistant Bot" in response


@pytest.mark.asyncio
async def test_offline_assistant_python_info():
    """Verify offline assistant answers python query."""
    ai = AIService()
    ai._client = None
    response = await ai.generate_response(prompt="Tell me about Python", language="en")
    assert "Python" in response
    assert "programming language" in response


@pytest.mark.asyncio
async def test_offline_assistant_unconfigured_guidance():
    """Verify friendly guidance when prompt is not a built-in rule in offline mode."""
    ai = AIService()
    ai._client = None
    response = await ai.generate_response(prompt="What is the capital of France?", language="en")
    assert "Smart Offline Assistant mode" in response
    assert "OPENAI_API_KEY" in response
