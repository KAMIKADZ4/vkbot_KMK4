# vkbot_KMK4
Бот от KAMIKADZ4 с возможностью его настройки


Документация vkbot_KMK4.py:

Функция time():
    Аргументы:
        Нет
    Описание:
        Возвращает текущее время и дату в формате 'H:M:S d.m.y'

Функция name_id():
    Аргументы:
        user_id - ID пользователя (type: int)
    Описание:
        Возвращает фамилию и имя пользователя с переданным ID в формате 'Фамилия Имя'

Функция write_msg()
    Аргументы:
        message - Текст сообщения для отправки (type: str)
        user_id - ID пользователя получателя (type: int)
        keyboard=None - Словарь клавиатуры в json формате (type: str)
        user_ids=None - Список ID пользователей получателей (type: str)
    Описание:
        Отправка сообщения указанному пользователю вк

Функция send():
    Аргументы:
        message - сообщение рассылки (type: str)
        user_id - ID пользователя запустившего рассылку(type: int)
    Описание:
        Рассылка сообщения пользователям, подписавшемся на рассылку

Функция new_message():
    Аргументы:
        event - объект класса из longpoll.listen() (type: object)
    Описание:
        Обработка сообщения от пользователя и вызов функции отправки сообщения с ответом


Документация config_KMK4.py:
    NAME_USERS_FILE - Название файла .txt с пользователями, подписанными на рассылку
    START_MSG - Первое сообщение бота при начале с ним диалога
    TOKEN - Токен группы
    MODERS - Список пользователей, с ролью модератора
    COMMANDS - Словарь с доступными командами и сообщениями ответа
    LOG_FILE - Название файла, в который будет записывать логи
    ACTIVE_COMMANDS - Список активных команд
    KEYBOARD - Клавиатура для бота в json формате


Версии проекта:
    1.0.0 - создание бота, написание документации и config_KMK4.py
    1.0.1 - небольшие изменения в выводе логов