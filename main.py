import telebot
import google.generativeai as genai
import os

# 1. Configuración Directa (Para asegurar que no falle por variables de Coolify)
TOKEN_TELEGRAM = "8725603893:AAF4hfK7XwMZ4vQARMe2HKvGvmhIFobB-U8"
KEY_GEMINI = "TU_CLAVE_DE_GOOGLE_AQUÍ" # <--- PEGA TU CLAVE AQUÍ

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=KEY_GEMINI)
model_ia = genai.GenerativeModel('gemini-1.5-flash')

print("🚀 Bot en modo ligero activado...")

# --- RESPUESTA INMEDIATA A TEXTO ---
@bot.message_handler(func=lambda message: True)
def responder_texto(message):
    print(f"Recibido mensaje: {message.text}")
    try:
        response = model_ia.generate_content(f"Responde de forma breve y profesional: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Estoy activo, pero Gemini necesita la API KEY correcta.")

# Eliminamos Whisper temporalmente para que el bot arranque YA
print("✅ ¡TODO LISTO! El bot está operando en modo texto.")
bot.polling(none_stop=True)
