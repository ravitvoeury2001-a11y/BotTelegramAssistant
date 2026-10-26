"""AI Service providing generative responses via OpenAI API with smart offline fallback."""

import logging
import re
from typing import Dict, List, Optional
from config import config

logger = logging.getLogger(__name__)


class AIService:
    """Manages AI interactions using OpenAI API or smart built-in fallback."""

    def __init__(self) -> None:
        self.api_key = config.openai_api_key
        self.model = config.openai_model
        self._client = None

        if self.api_key:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized with model: %s", self.model)
            except Exception as e:
                logger.warning("Failed to initialize OpenAI client: %s", e)
                self._client = None
        else:
            logger.info("OpenAI API key not configured. Smart offline assistant enabled.")

    @property
    def is_online(self) -> bool:
        """Check whether OpenAI client is configured and available."""
        return self._client is not None

    def get_status_description(self) -> str:
        """Return human-readable status of AI backend."""
        if self.is_online:
            return f"OpenAI Online ({self.model})"
        return "Smart Offline Assistant (Built-in)"

    async def generate_response(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        language: str = "en",
    ) -> str:
        """
        Generate an intelligent answer to the user query.

        Args:
            prompt: User's question or message.
            conversation_history: List of previous {'role': ..., 'content': ...} dicts.
            language: Preferred language code ('en' or 'km').

        Returns:
            The assistant's text response.
        """
        if self._client:
            try:
                return await self._call_openai(prompt, conversation_history, language)
            except Exception as e:
                logger.error("OpenAI API call failed, falling back to offline assistant: %s", e)
                # Fall back to offline assistant seamlessly on error
                return self._generate_offline_response(prompt, language, is_fallback=True)

        return self._generate_offline_response(prompt, language, is_fallback=False)

    async def _call_openai(
        self,
        prompt: str,
        conversation_history: Optional[List[Dict[str, str]]],
        language: str,
    ) -> str:
        """Call OpenAI Chat Completions API with system prompt and context."""
        lang_instruction = (
            "You MUST respond primarily in Khmer (ភាសាខ្មែរ), politely and naturally, "
            "unless the user explicitly asks in English or another language."
            if language == "km"
            else "Respond helpfully, politely, and concisely in English (or the language the user speaks)."
        )

        system_prompt = (
            "You are a friendly, intelligent, and highly knowledgeable Telegram Bot Assistant. "
            f"{lang_instruction}\n"
            "Keep responses well-formatted using clear Markdown. Avoid overly verbose explanations "
            "unless the user asks for in-depth details."
        )

        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

        if conversation_history:
            for msg in conversation_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": prompt})

        response = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        return reply.strip() if reply else "..."

    def _generate_offline_response(
        self, prompt: str, language: str, is_fallback: bool = False
    ) -> str:
        """
        Smart built-in rule-based knowledge engine for offline / free operation.

        Provides helpful, natural answers for greetings, bot questions, programming,
        Khmer language phrases, and friendly guidance.
        """
        text = prompt.strip().lower()

        # Khmer language responses
        if language == "km" or self._is_khmer_text(prompt):
            if any(w in text for w in ["សួស្ដី", "ជំរាបសួរ", "hello", "hi", "hey"]):
                return (
                    "សួស្ដីបាទ! ខ្ញុំជា Telegram Assistant Bot 🤖\n"
                    "តើខ្ញុំអាចជួយអ្វីអ្នកបាននៅថ្ងៃនេះ? "
                    "អ្នកអាចសួរសំណួរ ឬវាយ `/help` ដើម្បីមើលបញ្ជាទាំងអស់!"
                )
            if any(w in text for w in ["សុខសប្បាយ", "how are you", "សុខទេ"]):
                return "ខ្ញុំសុខសប្បាយជាធម្មតាទេបាទ! អរគុណច្រើនដែលបានសួរ។ ចុះអ្នកវិញសុខសប្បាយទេ?"
            if any(w in text for w in ["ឈ្មោះ", "name", "who are you", "អ្នកជាអ្នកណា"]):
                return "ខ្ញុំជា Telegram Bot Assistant ដែលបង្កើតឡើងដោយ Python និងគាំទ្រទាំងភាសាខ្មែរ និងអង់គ្លេស!"
            if any(w in text for w in ["python", "ពៃថុន"]):
                return (
                    "🐍 **ភាសា Python** គឺជាភាសាសរសេរកូដកម្រិតខ្ពស់ដែលមានភាពពេញនិយមយ៉ាងខ្លាំង "
                    "ងាយស្រួលរៀន និងមានបណ្ណាល័យ (Libraries) ច្រើនសម្រាប់ Artificial Intelligence (AI), "
                    "Data Science, Web Development, និង Telegram Bot Automation!"
                )
            if any(w in text for w in ["អរគុណ", "thanks", "thank you"]):
                return "រីករាយណាស់ដែលបានជួយបាទ! ប្រសិនបើមានចម្ងល់បន្ថែម អ្នកអាចសួរខ្ញុំបានគ្រប់ពេល។"

            notice = (
                "*(ចំណាំ៖ សេវា OpenAI API ជួបបញ្ហាការតភ្ជាប់)*\n\n" if is_fallback else ""
            )
            return (
                f"{notice}💡 **ខ្ញុំបានទទួលសំណួររបស់អ្នក៖** \"{prompt}\"\n\n"
                "បច្ចុប្បន្ន Bot កំពុងដំណើរការក្នុងទម្រង់ **Offline Assistant** "
                "(មិនទាន់បានភ្ជាប់ OpenAI API Key)។\n\n"
                "✨ **ដើម្បីបើកដំណើរការ AI ឆ្លាតវៃពេញលេញ៖**\n"
                "1. បង្កើត API Key នៅលើ [platform.openai.com](https://platform.openai.com)\n"
                "2. បញ្ចូល key ទៅក្នុងអថេរ `OPENAI_API_KEY` នៅក្នុងឯកសារ `.env`\n"
                "3. បើកដំណើរការ bot ឡើងវិញ!\n\n"
                "អ្នកនៅតែអាចប្រើ `/help`, `/settings`, ឬ `/about` បានយ៉ាងរលូន។"
            )

        # English responses
        if any(w in text for w in ["hello", "hi", "hey", "greetings"]):
            return (
                "Hello there! 👋 I am your Telegram Assistant Bot.\n"
                "How can I assist you today? Feel free to ask a question or type `/help`!"
            )
        if any(w in text for w in ["how are you", "how are u"]):
            return "I'm doing fantastic, thank you for asking! How are you doing today?"
        if any(w in text for w in ["who are you", "what are you", "your name"]):
            return (
                "I am **Telegram Assistant Bot**, an intelligent conversational assistant "
                "built with Python 3.12, SQLite memory, and support for both English & Khmer!"
            )
        if "python" in text:
            return (
                "🐍 **Python** is a high-level, interpreted programming language known for its "
                "clean syntax and readability. It is widely used in AI, Data Science, Web Backends, "
                "and Telegram Bot development!"
            )
        if any(w in text for w in ["thank you", "thanks", "thx"]):
            return "You're very welcome! Let me know if there's anything else I can help you with."

        notice = "*(Note: OpenAI connection issue detected)*\n\n" if is_fallback else ""
        return (
            f"{notice}💡 **Question Received:** \"{prompt}\"\n\n"
            "The bot is currently running in **Smart Offline Assistant mode** "
            "(OpenAI API key not configured).\n\n"
            "✨ **To unlock full generative AI power:**\n"
            "1. Obtain an API key from [platform.openai.com](https://platform.openai.com)\n"
            "2. Add `OPENAI_API_KEY=your_key` to your `.env` file\n"
            "3. Restart the bot!\n\n"
            "In the meantime, you can explore `/help`, `/settings`, and `/about`."
        )

    def _is_khmer_text(self, text: str) -> bool:
        """Detect whether a text snippet contains Khmer unicode characters (U+1780 to U+17FF)."""
        return bool(re.search(r"[\u1780-\u17FF]", text))


# Global singleton instance
ai_service = AIService()
