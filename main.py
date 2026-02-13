import os
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# Flask app (Render needs a web service running)
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running!"

# Telegram command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi Jachu!\n\n"
        "Send me any file (document/video/audio/photo)\n"
        "and I will generate a Telegram direct download link 🔥"
    )

# File handler
async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # Detect file type
    file_obj = None
    if msg.document:
        file_obj = msg.document
    elif msg.video:
        file_obj = msg.video
    elif msg.audio:
        file_obj = msg.audio
    elif msg.photo:
        file_obj = msg.photo[-1]  # highest quality photo

    if not file_obj:
        await msg.reply_text("❌ Please send a valid file.")
        return

    # Get file path from Telegram
    tg_file = await file_obj.get_file()
    file_path = tg_file.file_path

    # Direct download link
    direct_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    await msg.reply_text(
        f"✅ Direct Download Link Generated:\n\n{direct_link}\n\n"
        "⚡ Tip: Use IDM or 1DM for maximum speed."
    )

# Run bot
def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.ALL & ~filters.COMMAND, file_handler)
    )

    application.run_polling()

if __name__ == "__main__":
    # Run bot in background + Flask for Render
    from threading import Thread

    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
