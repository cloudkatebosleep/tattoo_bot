from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from bot.database import get_session
from bot.models import Client, AvailableDate
from sqlalchemy import select
import datetime

NAME, DATE, SIZE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    from sqlalchemy import select
    from bot.models import AvailableDate
    async for session in get_session():
        result = await session.execute(select(AvailableDate.date))
        dates = result.scalars().all()

        print("ДАТЫ ИЗ БД:", dates)  # отладка

        if not dates:
            await update.message.reply_text("Извините, пока нет доступных дат для записи.")
            return ConversationHandler.END

        keyboard = [[str(d)] for d in dates]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text("Выбери удобную дату:", reply_markup=reply_markup)
        return DATE
    
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date = datetime.date.fromisoformat(update.message.text)
        context.user_data["tattoo_date"] = date
        await update.message.reply_text("Какой размер татуировки (например, маленькая/средняя/большая)?",
            reply_markup=ReplyKeyboardRemove())
        return SIZE
    except ValueError:
        await update.message.reply_text("Неверная дата, выбери из кнопок.")
        return DATE

async def get_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    size = update.message.text
    context.user_data["tattoo_size"] = size

    async for session in get_session():
        client = Client(
            telegram_id=update.effective_user.id,
            name=context.user_data["name"],
            tattoo_date=context.user_data["tattoo_date"],
            tattoo_size=size
        )
        session.add(client)
        await session.commit()

    await update.message.reply_text("Спасибо, ты записан! Ожидай подтверждения записи от мастера!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
