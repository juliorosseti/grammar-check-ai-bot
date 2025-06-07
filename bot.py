import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from pydub import AudioSegment
import speech_recognition as sr
from langdetect import detect
import tempfile
import requests

# Carregar variáveis de ambiente
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action(action=ChatAction.TYPING)
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_path = os.path.join(tmpdir, 'audio.ogg')
        wav_path = os.path.join(tmpdir, 'audio.wav')
        await file.download_to_drive(ogg_path)
        # Converter para WAV
        audio = AudioSegment.from_file(ogg_path)
        audio.export(wav_path, format='wav')
        # Transcrever
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='pt-BR')
            except sr.UnknownValueError:
                try:
                    text = recognizer.recognize_google(audio_data, language='en-US')
                except sr.UnknownValueError:
                    await update.message.reply_text('Não consegui entender o áudio. Tente novamente.')
                    return
        # Detectar idioma
        idioma = detect(text)
        if idioma == 'pt':
            idioma_nome = 'português'
        elif idioma == 'en':
            idioma_nome = 'inglês'
        else:
            idioma_nome = idioma
        # Análise gramatical via Groq
        prompt = f"""
Você é um corretor gramatical. Analise o texto abaixo, identifique o idioma (português ou inglês), corrija os erros gramaticais e retorne:
- Porcentagem de acerto gramatical
- Lista de todos os erros encontrados

Texto:
{text}
"""
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post('https://api.groq.com/openai/v1/chat/completions', json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            resposta_ia = result['choices'][0]['message']['content']
            await update.message.reply_text(f"Idioma detectado: {idioma_nome}\nTexto transcrito: {text}\n\n{resposta_ia}")
        else:
            await update.message.reply_text('Erro ao analisar o texto com a IA.')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print('Bot rodando...')
    app.run_polling() 