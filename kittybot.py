import logging
import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
RESERVE_URL = os.getenv('RESERVE_URL')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = RESERVE_URL
        response = requests.get(new_url)

    response = response.json()
    return response[0].get('url')


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def say_hi(update, context):
    chat = update.effective_chat

    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name

    button = ReplyKeyboardMarkup([
        ['/newcat'],
    ], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=(
              f'Спасибо, что включили меня.\n'
              f'Привет, {name}. Посмотри, какого котика я тебе нашёл'
        ),
        reply_markup=button,
    )

    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    updater.start_polling(poll_interval=20.0)

    updater.idle()


if __name__ == '__main__':
    main()
