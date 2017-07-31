import json
import logging
import tornado.web as web
import config
import lib.decorators as decorator


class GroupHandler(web.RequestHandler):
    @decorator.authorized
    @decorator.inline
    async def get(self, what):
        if '2' in self.session['access']:
            logging.debug('WHAT: "{}"'.format(what))
            if what == 'add':
                self.render('add_group.html')
            elif what == 'edit':
                self.render('edit_group.html')
            else:
                self.redirect('/group/add')
        else:
            self.write('405')

    @decorator.authorized
    async def post(self, what):
        if '2' in self.session['access']:
            data = json.loads(self.request.body)
            if data[0] == 'ADD':
                pass
            self.write(json.dumps([]))
        else:
            self.write('405')
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH