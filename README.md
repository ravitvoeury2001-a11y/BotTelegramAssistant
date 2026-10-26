# 🤖 Telegram Bot Assistant

An intelligent, beginner-friendly Telegram Bot Assistant written in **Python 3.12+** using the modern `python-telegram-bot` (v21) framework, asynchronous **SQLite** storage, **OpenAI API** support with smart offline fallback, **conversation memory**, **rate limiting**, and bilingual support for **Khmer (ភាសាខ្មែរ)** & **English**.

---

## 🌟 Features

- 💬 **Conversational AI:** Ask questions with `/ask <question>` or directly message the bot in private chats.
- 🧠 **Context Memory:** Remembers recent conversation messages per user in an asynchronous SQLite database.
- 🌐 **Khmer & English Support:** Full internationalization (i18n) for Khmer (ភាសាខ្មែរ) and English with instant language toggling.
- ⚙️ **Interactive Settings:** In-chat inline buttons to change languages, check history, and clear conversation memory.
- 🛡️ **Role-Based Admin Commands:** Protected `/admin`, `/stats`, and `/broadcast` commands restricted to IDs listed in `ADMIN_IDS`.
- ⚡ **Anti-Spam Rate Limiter:** Cooldown mechanism prevents flood attacks and high API usage.
- ⏳ **Typing Indicator:** Displays active typing status while the bot is querying AI or processing.
- 🔄 **Smart Offline Fallback:** If `OPENAI_API_KEY` is not provided or fails, the bot gracefully switches to a built-in knowledge engine instead of crashing.
- 🔒 **Privacy & Security First:** Secret tokens are stored strictly in `.env`, and unhandled errors are safely captured without leaking server details to users.

---

## 📁 Project Structure

```text
telegram_bot_assistant/
│
├── bot.py                  # Main entry point and lifecycle manager
├── config.py               # Environment configuration and validation
├── database.py             # Asynchronous SQLite database (aiosqlite)
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Files excluded from version control
├── README.md               # Complete documentation and setup guide
│
├── handlers/               # Command and message handlers
│   ├── __init__.py         # Handler registry for python-telegram-bot
│   ├── start.py            # /start welcome handler & inline keyboard
│   ├── help.py             # /help commands guide
│   ├── about.py            # /about bot specs & version info
│   ├── settings.py         # /settings menu, /clear & callback queries
│   ├── chat.py             # /ask, text messages, memory & rate limiting
│   └── admin.py            # /admin, /stats & /broadcast commands
│
├── services/               # External services and business logic
│   ├── __init__.py
│   └── ai_service.py       # OpenAI API integration & smart offline engine
│
├── utils/                  # Helper utilities
│   ├── __init__.py
│   ├── i18n.py             # English & Khmer translations
│   ├── rate_limiter.py     # Sliding window anti-flood limiter
│   └── logging_config.py   # Console & rotating file logger (logs/bot.log)
│
└── tests/                  # Unit and integration test suite (pytest)
    ├── __init__.py
    ├── test_config.py
    ├── test_database.py
    ├── test_ai_service.py
    ├── test_rate_limiter.py
    └── test_handlers.py
```

---

## 🚀 Step-by-Step Setup on Windows

### 1. Install Python on Windows
1. Download Python 3.12+ from the official website: [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer and **ensure you check the box**:
   > ☑️ **"Add python.exe to PATH"** (Very important!)
3. Click **Install Now**.
4. Verify the installation by opening Command Prompt or PowerShell:
   ```powershell
   python --version
   pip --version
   ```

---

### 2. Create a Telegram Bot with @BotFather
1. Open the Telegram app on your phone or PC.
2. In the search bar, search for `@BotFather` (ensure it has the verified blue checkmark).
3. Send `/start` to start a chat with BotFather.
4. Send the command:
   ```text
   /newbot
   ```
5. Enter a friendly name for your bot (e.g., `My Assistant Bot`).
6. Enter a unique username for your bot ending in `bot` (e.g., `my_khmer_assistant_bot`).
7. BotFather will reply with your **Telegram Bot Token** in the format:
   ```text
   1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
   ```
   *Keep this token secret! Never share it publicly.*

---

### 3. Find Your Telegram User ID (For Admin Access)
To use administrator commands like `/stats` and `/broadcast`, you need your numeric Telegram User ID:
1. In Telegram, search for `@userinfobot` or `@raw_data_bot`.
2. Send `/start` to the bot.
3. It will reply with your numeric `Id` (e.g., `123456789`).

---

### 4. Configure the Environment Variables
1. Open Command Prompt (`cmd`) or PowerShell in the project directory.
2. Create your `.env` file from the example template:
   - **Command Prompt:**
     ```cmd
     copy .env.example .env
     ```
   - **PowerShell:**
     ```powershell
     cp .env.example .env
     ```
3. Open `.env` with Notepad or your code editor:
   ```cmd
   notepad .env
   ```
4. Fill in your credentials:
   ```env
   # Paste your bot token from @BotFather
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ

   # (Optional) If you have an OpenAI API key, paste it here:
   OPENAI_API_KEY=sk-...

   # (Optional) Your Telegram user ID for admin privileges:
   ADMIN_IDS=123456789
   ```
5. Save the file and close Notepad.

---

### 5. Install Dependencies

You can create a virtual environment and install the required packages:

#### In Command Prompt (cmd.exe):
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### In PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

*(If PowerShell shows a script execution error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*

---

### 6. Run the Test Suite
Ensure all components, database routines, and mock handlers work correctly:
```powershell
pytest -v
```
*(Or `.\.venv\Scripts\pytest.exe -v`)*

You should see **17 passed** tests!

---

### 7. Run the Telegram Bot
Start the bot polling process:

```cmd
python bot.py
```
*(Or `.\.venv\Scripts\python.exe bot.py`)*

You will see the startup banner and confirmation:
```text
==========================================================================
                 TELEGRAM BOT ASSISTANT (PYTHON 3.12+)
                      Intelligent Conversational AI
==========================================================================
2026-10-26 10:00:00 | INFO | telegram_bot_assistant - 🤖 TELEGRAM BOT ASSISTANT STARTED SUCCESSFULLY
```

---

## 📱 Bot Commands

| Command | Description |
| :--- | :--- |
| `/start` | Welcome greeting, features overview, and interactive button menu. |
| `/help` | Detailed instructions and list of available commands. |
| `/ask <query>` | Ask any question to the AI assistant with conversation memory. |
| `/about` | Bot specifications, framework version, and AI engine status. |
| `/settings` | Toggle between Khmer (ភាសាខ្មែរ) & English, and inspect stored history. |
| `/clear` | Wipe your personal conversation context memory from the database. |
| `/admin` | *(Admin Only)* Display the administrator control center. |
| `/stats` | *(Admin Only)* View user metrics, 24h active count, and message volume. |
| `/broadcast <text>` | *(Admin Only)* Broadcast an announcement to all registered users. |

> 💡 **Tip:** In direct private chat with the bot, you don't even need to type `/ask`! Simply send any text message and the bot will reply with context-aware AI answers.

---

## 🛠️ Troubleshooting Common Windows Issues

### 1. `python` is not recognized as an internal or external command
- **Cause:** Python was installed without checking "Add python.exe to PATH".
- **Fix:** Re-run the Python installer, select **Modify**, and check **Add python.exe to PATH**.

### 2. PowerShell: `cannot be loaded because running scripts is disabled`
- **Cause:** Windows default PowerShell execution policy restricts scripts.
- **Fix:** Run this once in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

### 3. `TELEGRAM_BOT_TOKEN is missing or set to placeholder`
- **Cause:** You have not created a `.env` file or have not pasted your real token.
- **Fix:** Make sure `.env` exists in the project root and `TELEGRAM_BOT_TOKEN` contains your actual token from `@BotFather`.

### 4. `Conflict: terminated by other getUpdates request`
- **Cause:** Multiple instances of your bot are running simultaneously with the same token.
- **Fix:** Open Task Manager on Windows, end any stray `python.exe` processes, and restart `bot.py`.

### 5. AI responses say "Smart Offline Assistant mode"
- **Cause:** `OPENAI_API_KEY` was left blank in `.env`.
- **Fix:** If you want OpenAI responses, add your OpenAI key into `.env` and restart the bot. If you do not have an OpenAI key, no problem! The bot continues working in offline assistant mode.

---

## 📜 License
Distributed under the MIT License. Safe for educational and commercial applications.
