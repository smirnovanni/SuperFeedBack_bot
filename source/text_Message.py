import telebot
from source.config import *
from source.log import log
bot = telebot.TeleBot(TOKEN)
def main():
    @bot.message_handler(content_types=['text'],regexp=None)
    def text_handler (message):
        if message.chat.id != int(CHAT):
            bot.send_message(CHAT,message.text)


if __name__ == '__main__':
    main()