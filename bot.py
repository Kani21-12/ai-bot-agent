from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Agent state
total_reward = 0

def reward_function(text):
    positive = ["thanks", "good", "great"]
    negative = ["bad", "useless"]

    if any(word in text.lower() for word in positive):
        return 10
    elif any(word in text.lower() for word in negative):
        return -5
    return 1


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_reward

    user_text = update.message.text

    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": user_text}
                ]
            },
            timeout=10
        )

        data = response.json()

        if "choices" in data:
            bot_reply = data["choices"][0]["message"]["content"]
        else:
            bot_reply = f"API Error: {data}"

    except Exception as e:
        bot_reply = f"Error: {e}"

    reward = reward_function(user_text)
    total_reward += reward

    reply = f"{bot_reply}\n\nReward: {reward} | Total: {total_reward}"
    await update.message.reply_text(reply)


# Start bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot running...")
app.run_polling()