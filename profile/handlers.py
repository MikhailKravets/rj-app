import tornado.web as web

from config import *


class ProfileHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    def get(self):
        user = Config.users[self.get_cookie('session')]
        self.render('profile.html', login=user.login,
                    last=user.last, middle=user.middle, first=user.first,
                    email=user.email,
                    sex=user.sex)

    def post(self):
        pass

    def get_template_path(self):
        return Config.TEMPLATE_PATH