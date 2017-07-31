import json
import logging
import config
import lib.decorators as decorator
import tornado.web as web


class MainHandler(web.RequestHandler):
    @decorator.authorized(access_level='0')
    async def get(self):
        self.render('main.html', access=self.session['access'])

    async def post(self):
        data = json.loads(self.request.body)
        if data[0] == 'QUIT':
            # TODO: make client/server speaking protocol
            self.write('OK')
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH