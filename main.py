import os
import telebot
from openrouter import OpenAI
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# Настройка OpenRouter через OpenAI SDK
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://daldobro.xyz",  # можно свой сайт
        "X-Title": "DALDOBROBOT"
    }
)

# Обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Ошибка: {str(e)}"

    bot.reply_to(message, reply)

# Запуск бота
if __name__ == "__main__":
    print("DALDOBROBOT запущен через OpenRouter")
    bot.polling(non_stop=True, skip_pending=True)