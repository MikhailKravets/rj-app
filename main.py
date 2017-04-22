import json
import logging
import random

import tornado.web as web
import tornado.websocket as websocket
import tornado.ioloop as loop
import tornado.httpserver

from config import *
from system import Specify

from main.handlers import MainHandler
from auth.handlers import AuthHandler, EndregHandler
from profile.handlers import ProfileHandler
from invite.handlers import InviteHandler
from settings.handlers import SettingsHandler
from group.handlers import GroupHandler
from load.handlers import LoadHandler
from discipline.handlers import DisciplineHandler
from journal.handlers import JournalHandler


class Application(web.Application):
    def __init__(self):
        logging.basicConfig(format="%(filename)8s[line: %(lineno)s] %(levelname)3s - %(message)s", level=logging.DEBUG)
        handlers = [
            (r"/", MainHandler),
            (r"/auth", AuthHandler),
            (r"/register", EndregHandler),
            (r"/profile", ProfileHandler),
            (r"/invite", InviteHandler),
            (r"/settings", SettingsHandler),
            (r"/group/([a-z]*)", GroupHandler),
            (r"/load/([a-z]*)", LoadHandler),
            (r"/discipline/([a-z]*)", DisciplineHandler),
            (r"/journal/([a-z]*)", JournalHandler)
        ]
        settings = {
            'debug': True,
            'compiled_template_cache': False,
            'static_path': Config.TEMPLATE_PATH
        }
        self.db_manager = DBManager()
        super().__init__(handlers, **settings)

    def authorized(self, session_name):
        if session_name in Config.users:
            if Config.users[session_name].pristine != 1:
                return True
        return False

    def inline_get(self, argument):
        if argument == '1':
            return True
        else:
            return False

    def has_access(self, session, access_level):
        if self.authorized(session_name=session):
            if access_level in Config.users[session]:
                return True
        return False

    def escape_data(self, data):
        if type(data) == list:
            for i in range(1, len(data)):
                try:
                    data[i] = Config.escape(data[i])
                except Exception as error:
                    logging.debug("Escaping error list: {}".format(error))
        elif type(data) == dict:
            for k in data.keys():
                try:
                    data[k] = Config.escape(data[k])
                except Exception as error:
                    logging.debug("Escaping error dict: {}".format(error))
        elif type(data) == str:
            data = Config.escape(data)
        return data

    def __create_god(self):
        login = 'admin'
        password = 'admin'
        first, middle, last = 'Ronald', 'The First', 'Everdone'
        email = 'creategoolemail@gmail.com'
        access = '1234'
        query = f"""INSERT INTO users (login, password, email, first, middle, last, access)
                   VALUES
                   ('{login}', SHA2('{password}', 224), '{email}', '{first}', '{middle}', '{last}', '{access}')"""
        for i in self.db_manager.execute(query):
            print(i)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(Config.PORT)
    print("Server starts")
    loop.IOLoop.current().start()
