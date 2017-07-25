import json
import os
import random as r
import time
import MySQLdb
import logging


class Config:
    PATH = os.getcwd()
    TEMPLATE_PATH = PATH + '/templates'
    PATH_SESSIONS = PATH + '/tmp/'
    PATH_CONTENT = TEMPLATE_PATH + '/content/'
    PATH_SVG = PATH_CONTENT + 'svg/'

    PORT = 81

    DB = {
        'host': 'localhost',
        'user': 'rjournal',
        'passwd': 'rjournal',
        'db': 'rjdb'
    }

    users = {} # dict that contains connected users

    MAX_REGISTRATION_STEP = 2
    MAX_REGISTRATION_PICT_NUMBER = 5

    @staticmethod
    def escape(string):
        return MySQLdb.escape_string(string).decode('utf8')

    @staticmethod
    def rand_hexline(length, millis_time=True):
        if millis_time:
            current_time = round(time.time()*1000)
            name = hex(current_time)[2:]
        else:
            name = ""
        for i in range(length):
            j = r.randint(0, 1)
            if j == 0:
                name += chr(r.randrange(48, 57))
            else:
                name += chr(r.randrange(97, 102))
        return name


class Decorator:
    @staticmethod
    def authorized(fn):
        async def wrapper(self, *args):
            if self.application.authorized(self.get_cookie('session')):
                await fn(self, *args)
            else:
                inline = self.application.inline_get(self.get_argument('inline', False))
                if inline:
                    self.write('DENIED')
                else:
                    self.redirect('/auth')
        return wrapper

    @staticmethod
    def inline(fn):
        async def wrapper(self, *args):
            inline = self.application.inline_get(self.get_argument('inline', False))
            if inline:
                await fn(self, *args)
            else:
                self.render('main.html', access=Config.users[self.get_cookie('session')].access)
        return wrapper


# TODO: Remove this and connect Redis for sessions instead
class Session:
    @staticmethod
    def create(obj):
        name = Config.rand_hexline(22)
        file = open(Config.PATH_SESSIONS + name, 'w')
        file.write(json.dumps(obj))
        file.close()
        return name

    @staticmethod
    def modify(name, obj):
        try:
            file = open(Config.PATH_SESSIONS + name, 'w')
            file.write(json.dumps(obj))
            file.close()
        except FileNotFoundError:
            return False

    @staticmethod
    def delete(name):
        os.remove(Config.PATH_SESSIONS + name)

    @staticmethod
    def get(name):
        try:
            file = open(Config.PATH_SESSIONS + name, 'r')
            obj = json.loads(file.read())
            file.close()
            return obj
        except ValueError:
            return None
        except TypeError:
            return None
        except FileNotFoundError:
            return None
        except PermissionError:
            return None
        except IsADirectoryError:
            return None


# TODO: sort out this shit. Use sqlalchemy
class DBManager:
    def __init__(self):
        self.connection = MySQLdb.connect(**Config.DB, charset='utf8')
        logging.debug("CREATE CONNECTION TO DB")
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection = MySQLdb.connect(**Config.DB, charset='utf8')
        self.cursor = self.connection.cursor()

    def execute(self, query):
        try:
            self.cursor.execute(query)
            yield from self.cursor.fetchall()
        except MySQLdb.IntegrityError as error:
            logging.error('MySQL integrity error: {}'.format(error))
            yield 'IntegrityError'
        except MySQLdb.OperationalError as error:
            logging.error('MySQL operational error: {}'.format(error))
            yield 'OperationalError'
        except MySQLdb.Error as error:
            logging.error('MySQL error: {}'.format(error))
            yield 'Error'

    def close(self):
        try:
            self.connection.close()
        except MySQLdb.ProgrammingError:
            pass

    def __del__(self):
        self.connection.close()
