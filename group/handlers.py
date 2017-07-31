import json
import logging
import tornado.web as web
import config
import lib.decorators as decorator


class GroupHandler(web.RequestHandler):
    @decorator.authorized(access_level='2')
    @decorator.inline
    async def get(self, what):
        logging.debug('WHAT: "{}"'.format(what))
        if what == 'add':
            self.render('add_group.html')
        elif what == 'edit':
            self.render('edit_group.html')
        else:
            self.redirect('/group/add')

    @decorator.authorized
    async def post(self, what):
        data = json.loads(self.request.body)
        if data[0] == 'ADD':
            pass
        self.write(json.dumps([]))
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH