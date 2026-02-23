import telebot
import google.generativeai as genai
import whisper
import os
from pydub import AudioSegment

# Configuración (Asegúrate de tener TOKEN_TELEGRAM y KEY_GEMINI en las Variables de Coolify)
TOKEN_TELEGRAM = os.getenv('TOKEN_TELEGRAM')
KEY_GEMINI = os.getenv('KEY_GEMINI')

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=KEY_GEMINI)
model_ia = genai.GenerativeModel('gemini-1.5-flash')

# Usamos el modelo "tiny" para una descarga ultra rápida en el servidor
print("🚀 Cargando motor Whisper (versión ligera)...")
model_whisper = whisper.load_model("tiny")

# --- FUNCIÓN PARA TEXTO (Para saber que el bot está vivo) ---
@bot.message_handler(commands=['start', 'help'])
def enviar_bienvenida(message):
    bienvenida = (
        "🌟 **¡Presencia Confirmada!**\n\n"
        "Tu asistente de élite está activo y listo para canalizar la abundancia de información. "
        "Envíame una **nota de voz** y crearé un reporte estratégico para ti de inmediato."
    )
    bot.reply_to(message, bienvenida, parse_mode="Markdown")

# --- FUNCIÓN PARA VOZ ---
@bot.message_handler(content_types=['voice'])
def manejar_voz(message):
    bot.reply_to(message, "📥 **Audio recibido.** Procesando con inteligencia... ⏳")
    
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("temp.ogg", 'wb') as f: f.write(downloaded_file)
        
        # Convertimos el audio
        AudioSegment.from_ogg("temp.ogg").export("temp.wav", format="wav")
        
        # Transcripción
        result = model_whisper.transcribe("temp.wav")
        
        # Análisis con la IA de Google
        prompt_maestro = (
            "Actúa como un asistente de alta dirección. Organiza esta información de visita médica "
            "con claridad y abundancia de detalles en 4 puntos: "
            "1. Resumen, 2. Puntos Clave, 3. Compromisos y 4. Próximos pasos.\n\n"
            f"Texto: {result['text']}"
        )
        
        response = model_ia.generate_content(prompt_maestro)
        
        bot.send_message(message.chat.id, f"📊 **REPORTE ESTRATÉGICO:**\n\n{response.text}", parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Hubo un pequeño obstáculo: {str(e)}")

print("✅ ¡TODO LISTO! El bot está operando ahora mismo.")
bot.polling()
