import json

import logging

import config
import lib.decorators as decorator
import tornado.web as web


class DisciplineHandler(web.RequestHandler):
    @decorator.authorized
    @decorator.inline
    async def get(self, what):
        if '3' in self.session['access']:
            logging.debug('WHAT: "{}"'.format(what))
            if what == 'add':
                self.render('add_discipline.html')
            elif what == 'edit':
                self.render('edit_discipline.html')
            else:
                self.redirect('/discipline/add')
        else:
            self.write('405')
            self.finish()

    @decorator.authorized
    async def post(self, what):
        if '3' in self.session['access']:
            data = json.loads(self.request.body)
            if data[0] == 'ADD':
                pass
            self.write(json.dumps([]))
        else:
            self.write('405')
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH