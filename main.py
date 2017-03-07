import json
import logging
import tornado.web as web
import tornado.websocket as websocket
import tornado.ioloop as loop
import tornado.httpserver

from config import *
from system import User


class MainHandler(web.RequestHandler):
    def get(self):
        if self.application.authorized(self.get_cookie('session')):
            self.render('main.html')
        else:
            self.redirect('/auth')

    def post(self):
        pass

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class ProfileHandler(web.RequestHandler):
    def get(self):
        inline = self.application.inline_get(self.get_argument('inline', '0'))
        if self.application.authorized(self.get_cookie('session')):
            if inline:
                user = Config.users[self.get_cookie('session')]
                self.render('profile.html', login=user.login,
                            last=user.name[2], middle=user.name[1], first=user.name[0],
                            email=user.email,
                            sex=user.sex)
            else:
                self.render('main.html')
        else:
            if inline:
                self.write('DENIED')
            else:
                self.redirect('/auth')

    def post(self):
        pass

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class InviteHandler(web.RequestHandler):
    def get(self):
        inline = self.application.inline_get(self.get_argument('inline', '0'))
        if self.application.authorized(self.get_cookie('session')):
            if inline:
                user = Config.users[self.get_cookie('session')]
                if '3' in user.access:
                    self.render('invite.html')
                else:
                    self.write('NO ACCESS')
            else:
                self.render('main.html')
        else:
            if inline:
                self.write('DENIED')
            else:
                self.redirect('/auth')

    def post(self):
        if self.application.authorized(self.get_cookie('session')):
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
        else:
            self.write('DENIED')

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class AuthHandler(web.RequestHandler):
    def get(self):
        if self.application.authorized(self.get_cookie('session')):
            self.redirect('/')
        else:
            self.render('auth.html')

    def post(self):
        data = json.loads(self.request.body)
        if data[0] == 'LOGIN':
            result = False
            logging.debug("Data: {}".format(data))
            query = """SELECT id, login, password, first, middle, last, email, sex, access, pristine
                        FROM users
                        WHERE login = '{0}' AND (password = SHA2('{1}', 224) OR password = '{1}')"""
            query = query.format(data[1], data[2])
            for retrieved in self.application.db_manager.execute(query):
                id_user, log, passwd, fn, mn, ln, email, sex, access, p = retrieved
                session_name = Config.rand_hexline(22)
                Config.users[session_name] = User(id_user, log, passwd, (fn, mn, ln), access, sex, email)
                self.set_cookie('session', session_name)
                result = True
            if result:
                self.write('OK')
            else:
                self.write('ERROR')

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class Application(web.Application):
    def __init__(self):
        logging.basicConfig(format="%(filename)8s[line: %(lineno)s] %(levelname)3s - %(message)s", level=logging.DEBUG)
        handlers = [
            (r"/", MainHandler),
            (r"/auth", AuthHandler),
            (r"/profile", ProfileHandler),
            (r"/invite", InviteHandler)
        ]
        settings = {
            'debug': True,
            'compiled_template_cache': False,
            'static_path': Config.TEMPLATE_PATH
        }
        self.db_manager = DBManager()
        super().__init__(handlers, **settings)

    def authorized(self, session_name):
        if session_name in Config.users:
            return True
        return False

    def inline_get(self, argument):
        if argument == '1':
            return True
        else:
            return False

    def has_access(self, session, access_level):
        if self.authorized(session_name=session):
            if access_level in Config.users[session]:
                return True
        return False

    def escape_data(self, data):
        if type(data) == list:
            for i in range(1, len(data)):
                data[i] = Config.escape(data[i])
        elif type(data) == dict:
            for k in data.keys():
                data[k] = Config.escape(data[k])
        elif type(data) == str:
            data = Config.escape(data)
        return data

    def __create_god(self):
        login = 'admin'
        password = 'admin'
        first, middle, last = 'Ronald', 'The First', 'Everdone'
        email = 'creategoolemail@gmail.com'
        access = '1234'
        query = f"""INSERT INTO users (login, password, email, first, middle, last, access)
                   VALUES
                   ('{login}', SHA2('{password}', 224), '{email}', '{first}', '{middle}', '{last}', '{access}')"""
        for i in self.db_manager.execute(query):
            print(i)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(Config.PORT)
    print("Server starts")
    loop.IOLoop.current().start()
