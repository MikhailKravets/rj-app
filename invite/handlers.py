import tornado.web as web

from config import *


class InviteHandler(web.RequestHandler):
    @Decorator.authorized
    @Decorator.inline
    def get(self):
        user = Config.users[self.get_cookie('session')]
        if '3' in user.access:
            self.render('invite.html')
        else:
            self.write('405')

    @Decorator.authorized
    def post(self):
        if '3' in Config.users[self.get_cookie('session')].access:
            data = json.loads(self.request.body)
            if data[0] == 'INVITE':
                insert = data[1]
                insert = self.application.escape_data(insert)
                insert['password'] = Config.rand_hexline(6, millis_time=False)
                logging.debug(f"INVITE {insert}")
                query = """INSERT INTO users (login, password, first, middle, last, access, sex)
                           VALUES
                           ('{0[login]}', '{0[password]}', '{0[first]}', '{0[middle]}', '{0[last]}', '{0[access]}', '{0[sex]}')"""
                query = query.format(insert)
                logging.debug(query)

                result = ['OK', insert['password']]
                for retr in self.application.db_manager.execute(query):
                    if 'Integrity' in retr:
                        result = ['ERROR', 'duplicate']
                    elif 'Error' in retr:
                        result = ['ERROR', 'inner_error']
                self.write(json.dumps(result))
        else:
            self.write('405')

    def get_template_path(self):
        return Config.TEMPLATE_PATH