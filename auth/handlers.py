import random

import tornado.web as web

from config import *
from system import Specify


class AuthHandler(web.RequestHandler):
    async def get(self):
        if self.application.authorized(self.get_cookie('session')):
            self.redirect('/')
        else:
            if self.get_cookie('session') in Config.users:
                if Config.users[self.get_cookie('session')].pristine == 1:
                    self.redirect('/register')
                else:
                    self.render('auth.html')
            else:
                self.render('auth.html')

    async def post(self):
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
                Config.users[session_name] = Specify(id_user, log, (fn, mn, ln), access, sex, email, p)
                self.set_cookie('session', session_name)
                result = True
            if result:
                if Config.users[session_name].pristine == 1:
                    self.write('REGISTER')
                else:
                    self.write('OK')
            else:
                self.write('ERROR')
        self.finish()

    def get_template_path(self):
        return Config.TEMPLATE_PATH


class EndregHandler(web.RequestHandler):
    async def get(self):
        if self.application.authorized(self.get_cookie('session')):
            self.redirect('/')
        else:
            if self.get_cookie('session') in Config.users:
                if Config.users[self.get_cookie('session')].pristine == 0:
                    self.redirect('/')
                else:
                    data = Config.users[self.get_cookie('session')].endreg_step()
                    if data:
                        user = Config.users[self.get_cookie('session')]
                        self.render('endreg.html', first=user.first,
                                    middle=user.middle,
                                    step=user.endreg,
                                    max_step=Config.MAX_REGISTRATION_STEP,
                                    step_view=data,
                                    pict_number=str(random.randint(0, Config.MAX_REGISTRATIO_PICT_NUMBER)))
                    else:
                        self.redirect('/')
            else:
                self.redirect('/auth')
        self.finish()

    async def post(self):
        data = json.loads(self.request.body)
        result = False
        if data[0] == 'EMAIL':
            data[1] = Config.escape(data[1])
            query = """SELECT id FROM users WHERE email='{}' LIMIT 1""".format(data[1])
            duplicate = False
            for retr in self.application.db_manager.execute(query):
                duplicate = True
            if duplicate:
                result = ['ERROR', 'duplicate']
            else:
                Config.users[self.get_cookie('session')].email = data[1]
                finish = Config.users[self.get_cookie('session')].update_endreg()
                if finish:
                    result = finish
                else:
                    data = Config.users[self.get_cookie('session')].endreg_step()
                    result = ['NEXT', data]
        elif data[0] == 'PASSWORD':
            logging.debug('Password gained')
            Config.users[self.get_cookie('session')].password = data[1]
            finish = Config.users[self.get_cookie('session')].update_endreg()
            if finish:
                result = finish
            else:
                data = Config.users[self.get_cookie('session')].endreg_step()
                result = ['NEXT', data]
        self.write(json.dumps(result))
        self.finish()

    def get_template_path(self):
        return Config.TEMPLATE_PATH