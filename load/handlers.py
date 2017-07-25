import tornado.web as web

from config import *


class LoadHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    async def get(self, what):
        user = Config.users[self.get_cookie('session')]
        if '2' in user.access:
            logging.debug('WHAT: "{}"'.format(what))
            if what == 'add':
                self.render('add_load.html')
            elif what == 'edit':
                self.render('edit_load.html')
            else:
                self.redirect('/group/add')
        else:
            self.write('405')
            self.finish()

    @Decorator.authorized
    async def post(self, what):
        if '2' in Config.users[self.get_cookie('session')].access:
            data = json.loads(self.request.body)

            if data[0] == 'ADD':
                result = Config.users[self.get_cookie('session')].new_load(self.application.escape_data(data[1]))
            elif data[0] == 'CHOICE':
                result = Config.users[self.get_cookie('session')].choice(self.application.escape_data(data))
            self.write(json.dumps(result))
        else:
            self.write('405')
        self.finish()

    def get_template_path(self):
        return Config.TEMPLATE_PATH