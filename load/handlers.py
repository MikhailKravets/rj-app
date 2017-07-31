import json
import logging
import config
import lib.decorators as decorator
import tornado.web as web


class LoadHandler(web.RequestHandler):
    @decorator.authorized(access_level='2')
    @decorator.inline
    async def get(self, what):
        logging.debug('WHAT: "{}"'.format(what))
        if what == 'add':
            self.render('add_load.html')
        elif what == 'edit':
            self.render('edit_load.html')
        else:
            self.redirect('/group/add')

    @decorator.authorized(access_level='2')
    async def post(self, what):
        data = json.loads(self.request.body)
        # TODO: make adequate client/server speaking system
        self.write(json.dumps([]))
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH