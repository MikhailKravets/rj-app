import json
import logging
import tornado.web as web
import tornado.websocket as websocket
import tornado.ioloop as loop
import tornado.httpserver

from config import *


class MainHandler(web.RequestHandler):
    def get(self):
        user_id = self.application.authorized(self.get_cookie('session'))
        if user_id:
            self.render('main.html')
        else:
            self.redirect('/auth')

    def post(self):
        pass

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class AuthHandler(web.RequestHandler):
    def get(self):
        self.render('auth.html')

    def post(self):
        pass

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class Application(web.Application):
    def __init__(self):
        logging.basicConfig(format="%(filename)8s[line: %(lineno)s] %(levelname)3s - %(message)s", level=logging.DEBUG)
        handlers = [
            (r"/", MainHandler),
            (r"/auth", AuthHandler)
        ]
        settings = {
            'debug': True,
            'compiled_template_cache': False,
            'static_path': Config.TEMPLATE_PATH
        }
        self.db_manager = DBManager()
        super().__init__(handlers, **settings)

    def authorized(self, session_name):
        return Session.get(session_name)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(Config.PORT)
    print("Server starts")
    loop.IOLoop.current().start()