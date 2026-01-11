import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MODEL = os.getenv("MODEL", "deepseek-r1-distill-llama-70b")  # default model

# Function to talk to Groq
def ask_groq(question):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a Bengali-English assistant. Answer user questions based on custom Q/A."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data).json()
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠ Error: {str(e)}"

# Telegram handlers
def start(update, context):
    update.message.reply_text("👋 Hi! I am your Jadu Telegram Bot.\nAsk me anything in Bangla or English!")

def reply_message(update, context):
    user_text = update.message.text
    bot_reply = ask_groq(user_text)
    update.message.reply_text(bot_reply)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, reply_message))

    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
