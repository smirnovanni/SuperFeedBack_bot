import logging

import telebot

from source.config import TOKEN, ADMIN, CHAT
from source.log import log
from source.variables import *


def initial_bot(use_logging=True, level_name='DEBUG'):
    bot = telebot.TeleBot(TOKEN)
    logger = log('bot', 'bot.log', 'INFO')

    @bot.message_handler(commands=['start'])
    def start_handler(message: telebot.types.Message):
        bot.send_message(message.from_user.id, start_mess)
        logger.info(f"It's start handler. Message from {message.from_user.id}")

    @bot.message_handler(commands=['help'])
    def help_handler(message: telebot.types.Message):
        bot.send_message(message.from_user.id, help_mess)
        logger.info(f"It's start handler. Message from {message.from_user.id}")

    @bot.callback_query_handler(func=lambda call: call.data in ['approve'])
    def callback_handler(call):
        try:
            bot.send_message(CHAT, call.message.text)
        except:
            pass

    @bot.message_handler(content_types=['text'])
    def text_handler(message: telebot.types.Message):

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton('Опубликовать', callback_data='approve'),
                     telebot.types.InlineKeyboardButton('Отклонить', callback_data='refuse'))

        bot.send_message(ADMIN, message.text, reply_markup=keyboard)
        logger.info(f"It's text handler. Message from {message.from_user.id}")

    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))

    return bot
