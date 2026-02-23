import telebot
import google.generativeai as genai
import whisper
import os
from pydub import AudioSegment

# Configuración mediante variables de entorno (se configuran en Coolify)
TOKEN_TELEGRAM = os.getenv('TOKEN_TELEGRAM')
KEY_GEMINI = os.getenv('KEY_GEMINI')

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=KEY_GEMINI)
model_ia = genai.GenerativeModel('gemini-1.5-flash')

print("Cargando motor Whisper en el servidor...")
model_whisper = whisper.load_model("base")

@bot.message_handler(content_types=['voice'])
def manejar_voz(message):
    bot.reply_to(message, "Recibido en el servidor. Procesando audio... ⏳")
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("temp.ogg", 'wb') as f: f.write(downloaded_file)
    AudioSegment.from_ogg("temp.ogg").export("temp.wav", format="wav")
    
    result = model_whisper.transcribe("temp.wav")
    
    # Prompt de abundancia para el reporte
    prompt = f"Actúa como asistente de élite. Resume esta visita médica: {result['text']}"
    response = model_ia.generate_content(prompt)
    
    bot.send_message(message.chat.id, f"📊 **REPORTE ESTRATÉGICO:**\n\n{response.text}")

bot.polling()
