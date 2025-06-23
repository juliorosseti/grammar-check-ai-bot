# Grammar Checker Telegram Bot

A Telegram bot that transcribes voice messages and provides detailed grammar analysis and corrections in English.

## Features

- Voice message transcription using Groq's Whisper API
- Detailed grammar analysis and corrections
- Support for English language
- Clear and structured feedback with emojis
- Real-time processing

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bot-grammar-checker.git
cd bot-grammar-checker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

5. Run the bot:
```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send a voice message in English
3. The bot will:
   - Transcribe your voice message
   - Analyze the grammar
   - Provide corrections and explanations
   - Show the accuracy percentage
   - List any issues found
   - Offer corrected versions
   - Explain the grammar rules

## Response Format

The bot provides responses in the following format:

📝 Analyzed sentence:  
[Your transcribed text]

✅ Grammar accuracy:  
[Percentage]% correct

🚫 Issues found:  
- [List of grammar problems]

💡 Correct version(s):  
- [1-3 corrected versions]

📚 Grammar explanation:  
- [Explanation of corrections]

## Requirements

- Python 3.8+
- python-telegram-bot
- python-dotenv
- groq
- requests

## License

This project is licensed under the MIT License - see the LICENSE file for details. 