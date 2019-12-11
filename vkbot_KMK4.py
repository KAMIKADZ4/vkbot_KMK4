# -*- coding: UTF-8 -*-
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from datetime import datetime
from config_KMK4 import (TOKEN, MODERS, KEYBOARD,
                         START_MSG, NAME_USERS_FILE,
                         COMMANDS, ACTIVE_COMMANDS, LOG_FILE)

__author__ = 'KAMIKADZ4'
__version__ = '1.0.0'


def time():
    return datetime.strftime(datetime.now(), '%H:%M:%S %d.%m.%y')


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
    with open(NAME_USERS_FILE) as file:
        users_id = list(map(int, file.read().split()))
    for usr in range(0, len(users_id), 100):
        write_msg(message, None, user_ids=users_id[usr: usr + 100])

    print('@', time(), 'Рассылка завершена', file=LOG_FILE)
    return write_msg('Все отправлено', user_id)


def new_message(event):
    text = event.text
    user = event.user_id

    if text == '+':
        with open(NAME_USERS_FILE, 'r') as file:
            user_list = file.read().split()

        if str(user) not in user_list:
            with open(NAME_USERS_FILE, 'a') as file:
                print(str(user), file=file)

            print(time(), name_id(user), '(ID:%s) подписан на рассылку'%str(user), file=LOG_FILE)
            return write_msg('Вы подписались на рассылку, для отписки напишите "-"', user)

        else:
            return write_msg('Вы уже подписаны на рассылку, для отписки напишите "-"', user)

    elif text == '-':
        with open(NAME_USERS_FILE, 'r') as file:
            user_list = file.read()

        if str(user) in user_list:
            with open(NAME_USERS_FILE, 'w') as file:
                file.write(text.replace(str(user) + ' ', ''))

            print(time(), name_id(user), '(ID:%s) отписан от рассылки'%str(user), file=LOG_FILE)
            return write_msg('Вы отписались от рассылки', user)

        else:
            return write_msg('Вы уже отписаны от рассылки, для подписки напишите "+"', user)

    elif text.lower() in ACTIVE_COMMANDS:
        return write_msg(COMMANDS[text.lower()], user)

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
            print(time(), 'Сообщение:\n'+event.text, file=LOG_FILE)
            print('!__ Ответ бота:\n', new_message(event), file=LOG_FILE)

# Creator KAMIKADZ4
