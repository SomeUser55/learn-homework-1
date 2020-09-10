"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging
import os
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem


TOKEN = os.environ['TOKEN']

PLANET_NAMES = [name for _, _, name in ephem._libastro.builtin_planets()]
PLANET_CLASSES = {planet: getattr(ephem, planet)
    for planet in PLANET_NAMES
}

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 
        'password': 'python'
    }
}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)


def handle_planet_command(bot, update):
    print('called handle_planet_command')
    user_text = update.message.text 
    planet_name = user_text.split()[1]
    now = datetime.today().strftime('%Y/%m/%d')
    planet = PLANET_CLASSES[planet_name](now)
    constellations = ephem.constellation(planet)
    constellations_str = ', '.join(constellations)
    text = f'{planet_name} находится в следующих созвездиях: {constellations_str}'
    update.message.reply_text(text)


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", handle_planet_command))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()
