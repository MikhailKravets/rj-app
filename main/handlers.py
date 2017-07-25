import tornado.web as web

from config import *


class MainHandler(web.RequestHandler):
    @Decorator.authorized
    async def get(self):
        self.render('main.html', access=Config.users[self.get_cookie('session')].access)

    async def post(self):
        data = json.loads(self.request.body)
        if data[0] == 'QUIT':
            try:
                del Config.users[self.get_cookie('session')]
            except KeyError:
                logging.debug('User is already quited')
            self.write('OK')
        self.finish()

    def get_template_path(self):
        return Config.TEMPLATE_PATH