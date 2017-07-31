import os


PATH = os.getcwd()
TEMPLATE_PATH = PATH + '/templates'
PATH_SESSIONS = PATH + '/tmp/'
PATH_CONTENT = TEMPLATE_PATH + '/content/'
PATH_SVG = PATH_CONTENT + 'svg/'

PORT = 81

REDIS_ATTR = {
    'host': 'localhost',
    'port': 6379
}

MYSQL_ATTR = {
    'user': 'rjournal',
    'password': 'rjournal',
    'host': 'localhost',
    'database': 'rjdb'
}


MAX_REGISTRATION_STEP = 2
MAX_REGISTRATION_PICT_NUMBER = 5
