import logging
import tornado.web as web
import tornado.websocket as websocket
import tornado.ioloop as loop
import tornado.httpserver

from config import Config


class MainHandler(web.RequestHandler):
    def get(self):
        self.render('main.html')

    def post(self):
        pass

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class Application(web.Application):
    def __init__(self):
        logging.basicConfig(format="%(filename)8s[line: %(lineno)s] %(levelname)3s - %(message)s", level=logging.DEBUG)
        handlers = [
            (r"/", MainHandler)
        ]
        settings = {
            'debug': True,
            'compiled_template_cache': False,
            'static_path': Config.TEMPLATE_PATH
        }
        super().__init__(handlers, **settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(Config.PORT)
    print("Server starts")
    loop.IOLoop.current().start()