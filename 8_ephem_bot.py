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
from pathlib import Path
from pprint import pprint
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

from expression_solver import solve_expression



PARENT_DIR = Path(__file__).parent
CORPUS_PATH = os.path.join(PARENT_DIR, 'corpus_world_city.txt')
with open(CORPUS_PATH) as f:
    cities = f.read().lower().split()

CITY_CATALOG = {}
for city in cities:
    first_letter = city[0]
    if first_letter not in CITY_CATALOG:
        CITY_CATALOG[first_letter] = [] 

    CITY_CATALOG[first_letter].append(city)

USERS_IN_GAME = {}

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
    user_id = update['message']['from_user']['id']
    global USERS_IN_GAME
    if user_id not in USERS_IN_GAME:
        update.message.reply_text(user_text)
        return

    user_city = user_text.lower()
    first_letter = user_city[0]
    if user_city not in CITY_CATALOG[first_letter]:
        USERS_IN_GAME.pop(user_id)
        update.message.reply_text('Нет такого города. Вы проиграли.')
        return

    if user_city in USERS_IN_GAME[user_id]:
        USERS_IN_GAME.pop(user_id)
        update.message.reply_text('Этот город уже был. Вы проиграли.')
        return

    USERS_IN_GAME[user_id].add(user_city)
    last_letter = user_city[-1]
    my_city = choice(CITY_CATALOG[last_letter])
    USERS_IN_GAME[user_id].add(my_city)
    update.message.reply_text(my_city.capitalize())


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


def handle_wordcount(bot, update):
    from_user = update.message.text
    words = from_user.split()
    words_cnt = len(words) - 1
    to_user = 'Количество слов: {}'.format(words_cnt)
    update.message.reply_text(to_user)


def handle_next_full_moon(bot, update):
    now = datetime.today().strftime('%Y/%m/%d')
    next_moon_date = ephem.next_full_moon(now).datetime().strftime('%Y-%m-%d')
    to_user = 'Следующее полнолуние состоится: {}'.format(next_moon_date)
    update.message.reply_text(to_user)


def handle_cities(bot, update):
    # TODO make it work
    print('handle cities')
    global USERS_IN_GAME
    user_id = update['message']['from_user']['id']
    if user_id not in USERS_IN_GAME:
        USERS_IN_GAME[user_id] = set()
        update.message.reply_text('Начинаем игру в города. Ваш ход.')
    else:
        update.message.reply_text('Закончили игру в города')
        USERS_IN_GAME.pop(user_id)


   
def handle_calc(bot, update):
    from_user = update.message.text
    expression = from_user.split('/calc')[1].replace(' ', '')
    print(expression)
    try:
        result = str(solve_expression(expression))
    except ZeroDivisionError:
        result = 'Деление на ноль!'
    except ValueError:
        result = 'Ошибка!'

    update.message.reply_text(result)


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", handle_planet_command))
    dp.add_handler(CommandHandler("wordcount", handle_wordcount))
    dp.add_handler(CommandHandler("next_full_moon", handle_next_full_moon))
    dp.add_handler(CommandHandler("cities", handle_cities))
    dp.add_handler(CommandHandler("calc", handle_calc))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()
