from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os
from bot.handlers import start, get_name, get_date, get_size, cancel, NAME, DATE, SIZE

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_size)],
        }
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
