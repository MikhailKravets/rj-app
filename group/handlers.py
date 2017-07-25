import tornado.web as web

from config import *


class GroupHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    async def get(self, what):
        user = Config.users[self.get_cookie('session')]
        if '2' in user.access:
            logging.debug('WHAT: "{}"'.format(what))
            if what == 'add':
                self.render('add_group.html')
            elif what == 'edit':
                self.render('edit_group.html')
            else:
                self.redirect('/group/add')
        else:
            self.write('405')

    @Decorator.authorized
    async def post(self, what):
        if '2' in Config.users[self.get_cookie('session')].access:
            data = json.loads(self.request.body)
            if data[0] == 'ADD':
                data[1] = self.application.escape_data(data[1])
                data[1]['students'] = self.application.escape_data(data[1]['students'])
                result = Config.users[self.get_cookie('session')].new_group(data[1])
            self.write(json.dumps(result))
        else:
            self.write('405')
        self.finish()

    def get_template_path(self):
        return Config.TEMPLATE_PATH