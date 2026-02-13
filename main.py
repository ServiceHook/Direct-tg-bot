import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me a file and I’ll generate a Telegram direct download link!"
    )


async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    file_obj = msg.document or msg.video or msg.audio or (msg.photo[-1] if msg.photo else None)

    if not file_obj:
        await msg.reply_text("❌ Send a valid file.")
        return

    tg_file = await file_obj.get_file()
    file_path = tg_file.file_path

    direct_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    await msg.reply_text(f"✅ Direct Download Link:\n\n{direct_link}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, file_handler))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
