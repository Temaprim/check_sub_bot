import sys
import logging
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('bot.ini')

TOKEN = CONFIG['BOT']['TOKEN']
GIFT_CHANNEL_INVITE_LINK = CONFIG['BOT']['GIFT_CHANNEL_INVITE_LINK']
DATABASE_PATH = CONFIG['DATABASE']['PATH']

if '' in [TOKEN, GIFT_CHANNEL_INVITE_LINK, DATABASE_PATH]:
    logging.error(
        'Конфиг не заполнен. Проверьте "bot.ini" в корневой папке проекта '
        'на наличие всех параметров.'
    )     
    sys.exit(1)

