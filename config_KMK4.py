# -*- coding: UTF-8 -*-
NAME_USERS_FILE = 'users_KMK4.txt'
START_MSG = 'START_MSG'
TOKEN = 'TOKEN'
MODERS = [235120872]
COMMANDS = {'!discord': None,
            '!twitch': None,
            '!instagram': None,
            '!youtube': None,
            '!донат': None,
            '!steam': None}
LOG_FILE = None
ACTIVE_COMMANDS = [i for i in COMMANDS.keys() if COMMANDS[i] is not None]

if len(ACTIVE_COMMANDS) == 0:
    KEYBOARD = '{"buttons":[],"one_time":true}'
else:
    lis = ['{"action": {"type": "text", "label": "%s"}, "color": "positive"}' % \
           i for i in ACTIVE_COMMANDS]
    KEYBOARD = '{"one_time": false, "buttons": [[%s]]}' % ', '.join(lis)