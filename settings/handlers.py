import tornado.web as web

from config import *


class SettingsHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    def get(self):
        user = Config.users[self.get_cookie('session')]
        self.render('settings.html', login=user.login,
                    last=user.last, middle=user.middle, first=user.first,
                    email=user.email)

    @Decorator.authorized
    def post(self):
        data = json.loads(self.request.body)
        if data[0] == 'UPDATE':
            retr = Config.users[self.get_cookie('session')].update_settings(data[1])
            self.write(json.dumps(retr))

    def get_template_path(self):
        return Config.TEMPLATE_PATH