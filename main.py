import config

import logging

import tornado.web as web
import tornado.ioloop as loop
import tornado.httpserver

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
            'static_path': config.TEMPLATE_PATH
        }
        super().__init__(handlers, **settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.PORT)
    print("Server starts")
    loop.IOLoop.current().start()
