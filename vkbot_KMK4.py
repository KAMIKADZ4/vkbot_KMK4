# -*- coding: UTF-8 -*-
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from datetime import datetime
from json import load
from configparser import ConfigParser

__author__ = 'KAMIKADZ4'
__version__ = '1.0.1'

config = ConfigParser()
config.read('config_KMK4.ini')
TOKEN = config['token']
MODERS = list(map(int, config['moders'].split()))
START_MSG = config['start_msg']
NAME_USERS_FILE = config['name_users_file']
LOG_FILE = config['log_file']

with open(config['keyboard_file'], 'r', encoding='utf-8') as file:
    KEYBOARD = load(file)
    COMMANDS = list(KEYBOARD.keys())


def time():
    return datetime.strftime(datetime.now(), '%H:%M:%S %d-%m-%y')


def name_id(user_id):
    result = VK.users.get(user_ids=user_id)[0]
    return result['last_name'] + ' ' + result['first_name']


def write_msg(message, user_id, keyboard=None, user_ids=None):
    VK.messages.send(user_id=user_id,
                     message=message,
                     user_ids=user_ids,
                     random_id=randint(100000, 999999),
                     keyboard=keyboard)
    return message


def send(message, user_id):
    print('@', time(), 'Запущена рассылка.\nСообщение:', message, file=LOG_FILE)
    with open(NAME_USERS_FILE) as open_file:
        users_id = list(map(int, open_file.read().split()))
    for usr in range(0, len(users_id), 100):
        write_msg(message, None, user_ids=users_id[usr: usr + 100])

    print('@', time(), 'Рассылка завершена', file=LOG_FILE)
    return write_msg('Все отправлено', user_id)


def new_message(event):
    text = event.text
    user = event.user_id

    if text == '+':
        with open(NAME_USERS_FILE, 'r') as open_file:
            user_list = open_file.read().split()

        if str(user) not in user_list:
            with open(NAME_USERS_FILE, 'a') as open_file:
                print(str(user), file=open_file)

            print(time(), '$ Подписка на рассылку\nПользователь:', name_id(user),
                                                                   '(ID:%s)' % str(user),
                                                                   file=LOG_FILE)
            return write_msg('Вы подписались на рассылку, для отписки напишите "-"', user)

        else:
            return write_msg('Вы уже подписаны на рассылку, для отписки напишите "-"', user)

    elif text == '-':
        with open(NAME_USERS_FILE, 'r') as open_file:
            user_list = open_file.read()

        if str(user) in user_list:
            with open(NAME_USERS_FILE, 'w') as open_file:
                open_file.write(text.replace(str(user) + ' ', ''))

            print(time(), '$ Отписка от рассылки\nПользователь:', name_id(user),
                                                                  '(ID:%s)' % str(user),
                                                                  file=LOG_FILE)
            return write_msg('Вы отписались от рассылки', user)

        else:
            return write_msg('Вы уже отписаны от рассылки, для подписки напишите "+"', user)

    elif text in COMMANDS:
        return write_msg(KEYBOARD[text], user)

    elif text.lower() in ['ку', 'хай', 'привет', 'салам', 'шалом', 'салам алейкум', 'начать']:
        return write_msg(START_MSG, user, keyboard=KEYBOARD)

# Команды доступные  для модераторов
    # Команда для рассылки. Пример: !рассылка <сообщение>
    elif text.lower().startswith('!рассылка'):
        msg = text.split(maxsplit=1)

        if user not in MODERS:
            return write_msg('У вас не достаточно прав.', user)

        elif len(msg) != 2:
            return write_msg('Неправильно введена команда. Пример: !рассылка <сообщение>', user)

        else:
            return send(msg[-1], user)


vk_session = VkApi(token=TOKEN)
VK = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
print(time(), 'Бот запущен.', file=LOG_FILE)
with open(NAME_USERS_FILE, 'w'):
    pass

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('_'*20+'\n# Новое сообщение. ID:', str(event.user_id), file=LOG_FILE)
            print('Пользователь:', name_id(event.user_id))
            print(time(), 'Сообщение:\n'+event.text, file=LOG_FILE)
            print('_# Ответ бота:\n', new_message(event), file=LOG_FILE)

# Creator KAMIKADZ4
