import os
import telebot
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://daldobro.xyz",
        "X-Title": "DALDOBROBot"
    }
)

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

if __name__ == "__main__":
    print("DALDOBROBot запущен через OpenRouter")
    bot.polling(non_stop=True, skip_pending=True)