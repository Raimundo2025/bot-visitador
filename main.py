import telebot
import google.generativeai as genai
import os

# 1. Configuración de Identidad y Poder (Actualizada con tu nueva Key)
TOKEN_TELEGRAM = "8725603893:AAF4hfK7XwMZ4vQARMe2HKvGvmhIFobB-U8"
KEY_GEMINI = "AIzaSyBlfbCU54Pqb7qSt_I6cfnKuov_-D7ASdM" # <--- Tu nueva clave maestra

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=KEY_GEMINI)
model_ia = genai.GenerativeModel('gemini-1.5-flash')

print("🚀 Bot en modo ligero activado con nueva presencia...")

# --- RESPUESTA DE ÉLITE A TEXTO ---
@bot.message_handler(func=lambda message: True)
def responder_texto(message):
    print(f"Recibido mensaje: {message.text}")
    try:
        # Prompt que proyecta abundancia y profesionalidad
        prompt = f"Actúa como un asistente de alto nivel. Responde con presencia y claridad a: {message.text}"
        response = model_ia.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error detectado: {e}")
        bot.reply_to(message, "El canal con la inteligencia superior está activo, pero verifica la configuración de la clave.")

# Comando final para mantener la conexión vibrante y constante
print("✅ ¡TODO LISTO! El bot está operando en modo texto.")
bot.infinity_polling()
