import tornado.web as web

from config import *


class JournalHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    def get(self, what):
        user = Config.users[self.get_cookie('session')]
        if '1' in user.access:
            logging.debug('WHAT: "{}"'.format(what))
            if what == 'add':
                self.render('add_journal.html')
            elif what == 'edit':
                self.render('edit_journal.html')
            else:
                self.redirect('/journal/add')
        else:
            self.write('405')

    @Decorator.authorized
    def post(self, what):
        if '1' in Config.users[self.get_cookie('session')].access:
            data = json.loads(self.request.body)
            if data[0] == 'CHOICE':
                result = Config.users[self.get_cookie('session')].choice_load(Config.users[self.get_cookie('session')].id_user, self.application.escape_data(data[1]))
            elif data[0] == 'STEP':
                result = Config.users[self.get_cookie('session')].journ_step(data[1])
                if result:
                    result[2] = self.render_string(result[2], **result[3]).decode('utf8')
                    del result[3]
                else:
                    result = ['END']
            elif data[0] == 'ADD':
                Config.users[self.get_cookie('session')].increment_journ_step(data[1])
                result = Config.users[self.get_cookie('session')].journ_step(data[1])
                result[2] = self.render_string(result[2], **result[3]).decode('utf8')
            self.write(json.dumps(result))
        else:
            self.write('405')

    def get_template_path(self):
        return Config.TEMPLATE_PATH