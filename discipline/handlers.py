import json
import logging
import config
import lib.decorators as decorator
import tornado.web as web


class DisciplineHandler(web.RequestHandler):
    @decorator.authorized(access_level='3')
    @decorator.inline
    async def get(self, what):
        logging.debug('WHAT: "{}"'.format(what))
        if what == 'add':
            self.render('add_discipline.html')
        elif what == 'edit':
            self.render('edit_discipline.html')
        else:
            self.redirect('/discipline/add')

    @decorator.authorized(access_level='3')
    async def post(self, what):
        data = json.loads(self.request.body)
        if data[0] == 'ADD':
            pass
        self.write(json.dumps([]))
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH