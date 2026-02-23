import telebot
import google.generativeai as genai
import os

# 1. Configuración de Identidad y Abundancia
TOKEN_TELEGRAM = "8725603893:AAF4hfK7XwMZ4vQARMe2HKvGvmhIFobB-U8"
# Usamos tu nueva clave confirmada
KEY_GEMINI = "AIzaSyBlfbCU54Pqb7qSt_I6cfnKuov_-D7ASdM"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
genai.configure(api_key=KEY_GEMINI)

# Cambiamos a 'gemini-pro', que es la versión con mayor compatibilidad inmediata
model_ia = genai.GenerativeModel('gemini-pro')

print("🚀 Bot en modo ligero activado con nueva presencia...")

@bot.message_handler(func=lambda message: True)
def responder_texto(message):
    print(f"Recibido mensaje: {message.text}")
    try:
        # Prompt enfocado en resultados
        prompt = f"Actúa como un asistente de élite. Responde de forma clara: {message.text}"
        response = model_ia.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error detectado: {e}")
        # Si falla gemini-pro, intentamos con flash explícitamente
        try:
            model_alt = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model_alt.generate_content(message.text)
            bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "Presencia confirmada, pero mi conexión con la inteligencia superior está en mantenimiento.")

print("✅ ¡TODO LISTO! El bot está operando en modo texto.")
bot.infinity_polling(skip_pending=True)
