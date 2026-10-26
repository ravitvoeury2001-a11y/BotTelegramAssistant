"""Internationalization (i18n) module supporting English and Khmer (ភាសាខ្មែរ)."""

from typing import Dict, Any

SUPPORTED_LANGUAGES = {
    "en": "English 🇬🇧",
    "km": "ភាសាខ្មែរ 🇰🇭",
}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "welcome": {
        "en": (
            "👋 **Hello {name}! Welcome to Telegram Assistant Bot!**\n\n"
            "I am your intelligent assistant ready to help answer questions, "
            "provide information, and support your daily tasks.\n\n"
            "✨ **Main Features:**\n"
            "• 🤖 **AI Chat:** Ask questions with `/ask <question>` or simply send a message!\n"
            "• 🧠 **Memory:** I remember recent messages to maintain context.\n"
            "• 🌐 **Bilingual:** Full support for Khmer (ភាសាខ្មែរ) & English.\n"
            "• ⚙️ **Customizable:** Change preferences anytime with `/settings`.\n\n"
            "Press a button below or type `/help` to see all commands."
        ),
        "km": (
            "👋 **សួស្ដី {name}! សូមស្វាគមន៍មកកាន់ Telegram Assistant Bot!**\n\n"
            "ខ្ញុំជាជំនួយការឆ្លាតវៃដែលត្រៀមខ្លួនជួយឆ្លើយសំណួរ ផ្ដល់ព័ត៌មាន "
            "និងជួយសម្រួលដល់កិច្ចការប្រចាំថ្ងៃរបស់អ្នក។\n\n"
            "✨ **មុខងារចម្បងៗ៖**\n"
            "• 🤖 **ជជែកជាមួយ AI៖** សួរសំណួរដោយប្រើ `/ask <សំណួរ>` ឬផ្ញើសារមកខ្ញុំផ្ទាល់!\n"
            "• 🧠 **ការចងចាំបរិបទ៖** ចងចាំការសន្ទនាមុនៗដើម្បីឆ្លើយកាន់តែត្រូវគោលដៅ\n"
            "• 🌐 **ពីរភាសា៖** គាំទ្រទាំងភាសាខ្មែរ និងភាសាអង់គ្លេស\n"
            "• ⚙️ **ការកំណត់៖** កំណត់ភាសា ឬសម្អាតការចងចាំតាមរយៈ `/settings`\n\n"
            "សូមចុចប៊ូតុងខាងក្រោម ឬវាយបញ្ជា `/help` ដើម្បីមើលបញ្ជាទាំងអស់។"
        ),
    },
    "help": {
        "en": (
            "📖 **Available Commands & Usage Guide**\n\n"
            "🔹 `/start` - Start the bot and show welcome menu\n"
            "🔹 `/help` - View this help guide\n"
            "🔹 `/ask <question>` - Ask a question to the AI assistant\n"
            "🔹 `/about` - Information about the bot & developer\n"
            "🔹 `/settings` - Configure language and memory settings\n"
            "🔹 `/clear` - Clear your conversation memory history\n\n"
            "💡 **Pro Tip:** In private chat, you can simply send any text message "
            "without typing `/ask`! I will reply automatically."
        ),
        "km": (
            "📖 **បញ្ជីពាក្យបញ្ជា និងការណែនាំអំពីការប្រើប្រាស់**\n\n"
            "🔹 `/start` - ចាប់ផ្ដើមដំណើរការ bot និងបង្ហាញម៉ឺនុយស្វាគមន៍\n"
            "🔹 `/help` - មើលការណែនាំនេះ\n"
            "🔹 `/ask <សំណួរ>` - សួរសំណួរទៅកាន់ជំនួយការ AI\n"
            "🔹 `/about` - ព័ត៌មានលម្អិតអំពី bot និងអ្នកអភិវឌ្ឍន៍\n"
            "🔹 `/settings` - កំណត់ភាសា និងជម្រើសអង្គចងចាំ\n"
            "🔹 `/clear` - លុបប្រវត្តិនៃការសន្ទនាពីមុនៗរបស់អ្នក\n\n"
            "💡 **គន្លឹះមានប្រយោជន៍៖** នៅក្នុងការសន្ទនាផ្ទាល់ខ្លួន អ្នកគ្រាន់តែផ្ញើសារធម្មតា "
            "ដោយមិនបាច់វាយពាក្យ `/ask` ក៏បាន! ខ្ញុំនឹងឆ្លើយតបដោយស្វ័យប្រវត្តិ។"
        ),
    },
    "about": {
        "en": (
            "ℹ️ **About Telegram Assistant Bot**\n\n"
            "• **Version:** 1.0.0\n"
            "• **Platform:** Python 3.12+ (python-telegram-bot)\n"
            "• **Storage:** SQLite Async Database\n"
            "• **AI Engine:** {ai_engine}\n"
            "• **Languages:** English & Khmer (ភាសាខ្មែរ)\n"
            "• **Privacy:** Conversations are kept private and secure.\n\n"
            "Built with ❤️ for intelligent, friendly conversations."
        ),
        "km": (
            "ℹ️ **អំពី Telegram Assistant Bot**\n\n"
            "• **កំណែ (Version):** 1.0.0\n"
            "• **បច្ចេកវិទ្យា:** Python 3.12+ (python-telegram-bot)\n"
            "• **ទិន្នន័យ:** SQLite Async Database\n"
            "• **ម៉ាស៊ីន AI:** {ai_engine}\n"
            "• **ភាសា:** ភាសាខ្មែរ និងភាសាអង់គ្លេស\n"
            "• **ឯកជនភាព:** ទិន្នន័យនៃការសន្ទនាត្រូវបានរក្សាការសម្ងាត់យ៉ាងល្អ\n\n"
            "បង្កើតឡើងដោយក្ដីស្រឡាញ់ ❤️ ដើម្បីផ្ដល់ភាពងាយស្រួលដល់ការសន្ទនាឆ្លាតវៃ។"
        ),
    },
    "settings_menu": {
        "en": (
            "⚙️ **Bot Settings**\n\n"
            "• **Current Language:** {current_lang}\n"
            "• **Stored History:** {history_count} message(s)\n\n"
            "Choose an option below to update your preferences:"
        ),
        "km": (
            "⚙️ **ការកំណត់ Bot (Settings)**\n\n"
            "• **ភាសាបច្ចុប្បន្ន៖** {current_lang}\n"
            "• **ប្រវត្តិសន្ទនាដែលបានរក្សាទុក៖** {history_count} សារ\n\n"
            "សូមជ្រើសរើសជម្រើសខាងក្រោមដើម្បីកែប្រែការកំណត់របស់អ្នក៖"
        ),
    },
    "language_changed": {
        "en": "✅ Language changed to **English** 🇬🇧.",
        "km": "✅ បានប្តូរភាសាទៅជា **ភាសាខ្មែរ** 🇰🇭 ដោយជោគជ័យ។",
    },
    "memory_cleared": {
        "en": "🧹 Your conversation memory has been cleared successfully!",
        "km": "🧹 ប្រវត្តិការសន្ទនារបស់អ្នកត្រូវបានសម្អាតដោយជោគជ័យ!",
    },
    "rate_limited": {
        "en": "⏳ You're sending requests too fast! Please wait {seconds}s before trying again.",
        "km": "⏳ លោកអ្នកកំពុងផ្ញើសារលឿនពេក! សូមរង់ចាំ {seconds} វិនាទីសិនមុននឹងសួរម្ដងទៀត។",
    },
    "ask_empty": {
        "en": "❓ Please provide a question after `/ask`.\n\n*Example:* `/ask What is Python?`",
        "km": "❓ សូមបញ្ចូលសំណួរដែលអ្នកចង់សួរនៅពីក្រោយ `/ask`។\n\n*ឧទាហរណ៍៖* `/ask តើភាសា Python ជាអ្វី?`",
    },
    "error_generic": {
        "en": "⚠️ Sorry, an error occurred while processing your request. Please try again later.",
        "km": "⚠️ សូមអភ័យទោស! មានបញ្ហាក្នុងការដំណើរការសំណើរបស់អ្នក។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។",
    },
    "admin_only": {
        "en": "⛔ Access denied: This command is restricted to administrators.",
        "km": "⛔ បដិសេធការចូលប្រើ៖ បញ្ជានេះសម្រាប់តែអ្នកគ្រប់គ្រង (Admin) ប៉ុណ្ណោះ។",
    },
    "admin_stats": {
        "en": (
            "📊 **System Administration Statistics**\n\n"
            "• 👥 **Total Users:** {total_users}\n"
            "• 🟢 **Active Users (24h):** {active_users}\n"
            "• 💬 **Total Messages Logged:** {total_messages}\n"
            "• 🤖 **AI Mode:** {ai_mode}\n"
            "• 🛡️ **Registered Admins:** {admin_count}"
        ),
        "km": (
            "📊 **ស្ថិតិប្រព័ន្ធរដ្ឋបាល (Admin Stats)**\n\n"
            "• 👥 **ចំនួនអ្នកប្រើប្រាស់សរុប៖** {total_users}\n"
            "• 🟢 **អ្នកសកម្មក្នុងរយៈពេល ២៤ ម៉ោង៖** {active_users}\n"
            "• 💬 **សារទាំងអស់ក្នុងប្រព័ន្ធ៖** {total_messages}\n"
            "• 🤖 **ដំណើរការ AI៖** {ai_mode}\n"
            "• 🛡️ **ចំនួន Admin៖** {admin_count}"
        ),
    },
    "broadcast_started": {
        "en": "📢 Starting broadcast to {total_users} users...",
        "km": "📢 កំពុងចាប់ផ្ដើមផ្ញើសារជូនដំណឹងទៅកាន់អ្នកប្រើប្រាស់ចំនួន {total_users} នាក់...",
    },
    "broadcast_finished": {
        "en": "✅ Broadcast completed!\n• Delivered: {success}\n• Failed: {failed}",
        "km": "✅ ការផ្ញើសារជូនដំណឹងបានបញ្ចប់!\n• ជោគជ័យ៖ {success}\n• បរាជ័យ៖ {failed}",
    },
    "broadcast_empty": {
        "en": "⚠️ Usage: `/broadcast <message to send>`",
        "km": "⚠️ របៀបប្រើប្រាស់៖ `/broadcast <ខ្លឹមសារសារដែលត្រូវផ្ញើ>`",
    },
}


def get_text(key: str, lang: str = "en", **kwargs: Any) -> str:
    """
    Retrieve localized string by key and format with kwargs.

    Args:
        key: Translation dictionary key.
        lang: Target language code ('en' or 'km').
        **kwargs: Values to interpolate into formatted string.

    Returns:
        Formatted localized string or fallback.
    """
    if lang not in SUPPORTED_LANGUAGES:
        lang = "en"

    translation_dict = TRANSLATIONS.get(key, {})
    template = translation_dict.get(lang) or translation_dict.get("en", f"[{key}]")

    try:
        return template.format(**kwargs)
    except Exception:
        return template
