import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction, ParseMode
import whisper
import tempfile
from groq import Groq
import re

# Carregar variáveis de ambiente
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Inicializar o modelo Whisper (carrega apenas uma vez)
model = whisper.load_model("base")

# Inicializar cliente Groq
client = Groq(api_key=GROQ_API_KEY)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action(action=ChatAction.TYPING)
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, 'audio.ogg')
        await file.download_to_drive(audio_path)
        
        # Transcrever usando Whisper
        result = model.transcribe(audio_path)
        text = result["text"].strip()
        
        # Análise gramatical via Groq
        prompt = f"""
PROMPT FOR GRAMMAR AI ON TELEGRAM:

You are a grammar correction assistant responding via a Telegram bot.
Your job is to analyze user-submitted English sentences, identify grammar mistakes, and return a well-structured and helpful correction using emojis (if necessary).

Always follow this exact response format:
📝 Analyzed sentence:  
{text}

✅ Grammar accuracy:  
{{percentage}}% correct

{{If the sentence contains mistakes, continue with the sections below. If it’s 100% correct, say so clearly and do not include the next sections.}}

🚫 Issues found:  
- List any grammar problems (such as subject-verb agreement, punctuation, tense, spelling, etc.)

💡 Correct version(s):  
- Provide 1 to 3 corrected versions of the sentence.

📚 Grammar explanation:  
- Briefly explain why each mistake is wrong and how the corrected sentence improves it.
"""
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            
            ai_awnser = completion.choices[0].message.content
            await update.message.reply_text(escape_markdown_v2(ai_awnser), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print(f"Erro na API Groq: {str(e)}")
            await update.message.reply_text('Error parsing text with AI. Please try again.')


def escape_markdown_v2(text):
    # Escapes all special characters for Telegram Markdown V2
    escape_chars = r'[_*[\]()~`>#+\-=|{}.!]'
    return re.sub(escape_chars, lambda match: '\\' + match.group(0), text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print('Bot running...')
    app.run_polling() 