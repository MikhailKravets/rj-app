import json
import logging
import config
import lib.decorators as decorator
import tornado.web as web


class JournalHandler(web.RequestHandler):
    @decorator.authorized(access_level='1')
    @decorator.inline
    async def get(self, what):
        logging.debug('WHAT: "{}"'.format(what))
        if what == 'add':
            self.render('add_journal.html')
        elif what == 'edit':
            self.render('edit_journal.html')
        else:
            self.redirect('/journal/add')

    @decorator.authorized(access_level='1')
    async def post(self, what):
        data = json.loads(self.request.body)
        # TODO: create adequate client/server messaging system
        self.write(json.dumps([]))
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH