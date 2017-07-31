import json
import logging
import tornado.web as web
import config
import lib.decorators as decorator


class InviteHandler(web.RequestHandler):
    @decorator.authorized(access_level='3')
    @decorator.inline
    async def get(self):
        self.render('invite.html')

    @decorator.authorized(access_level='3')
    async def post(self):
        data = json.loads(self.request.body)
        if data[0] == 'INVITE':
            pass
            self.write(json.dumps([]))
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH