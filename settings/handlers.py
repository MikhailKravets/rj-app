import json
import logging
import config
import lib.decorators as decorator
import tornado.web as web


class SettingsHandler(web.RequestHandler):
    @decorator.authorized(access_level='1')
    @decorator.inline
    async def get(self):
        # TODO: ask Mysql for user's data
        self.render('settings.html', login='',
                    last='', middle='', first='',
                    email='')

    @decorator.authorized
    async def post(self):
        data = json.loads(self.request.body)
        if data[0] == 'UPDATE':
            # TODO: invent normal client/server speaking protocol
            pass
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH