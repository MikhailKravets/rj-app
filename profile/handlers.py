import json
import logging
import config
import lib.decorators as decorator
import tornado.web as web


class ProfileHandler(web.RequestHandler):
    @decorator.authorized(access_level='1')
    @decorator.inline
    async def get(self):
        # TODO: ask Mysql for user information
        self.render('profile.html', login='',
                    last='', middle='', first='',
                    email='',
                    sex='')

    async def post(self):
        pass

    def get_template_path(self):
        return config.TEMPLATE_PATH