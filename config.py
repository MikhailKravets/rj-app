import json
import os
import random as r
import time
import MySQLdb


class Config:
    PATH = 'c:/rj'
    TEMPLATE_PATH = PATH + '/templates'
    PATH_SESSIONS = PATH + '/tmp/'
    PATH_SVG = TEMPLATE_PATH + '/content/svg/'

    PORT = 83

    DB = {
        'host': 'localhost',
        'user': 'rjournal',
        'passwd': 'rjournal',
        'db': 'rjdb'
    }

    users = {} # dict that contains connected users

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


class DBManager:
    def __init__(self):
        self.connection = MySQLdb.connect(**Config.DB)
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection = MySQLdb.connect(**Config.DB)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        yield from self.cursor.fetchall()

    def close(self):
        try:
            self.connection.close()
        except MySQLdb.ProgrammingError:
            pass

    def __del__(self):
        self.connection.close()