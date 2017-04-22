import tornado.web as web

from config import *


class DisciplineHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    def get(self, what):
        user = Config.users[self.get_cookie('session')]
        if '3' in user.access:
            logging.debug('WHAT: "{}"'.format(what))
            if what == 'add':
                self.render('add_discipline.html')
            elif what == 'edit':
                self.render('edit_discipline.html')
            else:
                self.redirect('/discipline/add')
        else:
            self.write('405')

    @Decorator.authorized
    def post(self, what):
        if '3' in Config.users[self.get_cookie('session')].access:
            data = json.loads(self.request.body)
            if data[0] == 'ADD':
                result = Config.users[self.get_cookie('session')].add_discipline(self.application.escape_data(data[1]))
            self.write(json.dumps(result))
        else:
            self.write('405')

    def get_template_path(self):
        return Config.TEMPLATE_PATH