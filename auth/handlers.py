import json

import config
import random
import tornado.web as web
from lib.session import HashSession
from main.models import User


class AuthHandler(web.RequestHandler):
    async def get(self):
        redis_session = HashSession()
        key = self.get_cookie('session')

        if key in redis_session:
            user_data = redis_session[key]
            if user_data['activated'] == '0':
                self.redirect('/register')
            else:
                self.redirect('/')
        else:
            self.render('auth.html')

    async def post(self):
        data = json.loads(self.request.body)
        # TODO: create adequate client/server speaking protocol
        if data[0] == 'LOGIN':
            pass
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH


class EndregHandler(web.RequestHandler):
    async def get(self):
        redis_session = HashSession()
        key = self.get_cookie('session')

        if key in redis_session:
            user_data = redis_session[key]
            if user_data['activated'] == '1':
                self.redirect('/')
            else:
                # TODO: after inventing adequate client/server speaking protocol, create registration
                # data = Config.users[self.get_cookie('session')].endreg_step()
                # if data:
                #     user = Config.users[self.get_cookie('session')]
                #     self.render('endreg.html', first=user.first,
                #                 middle=user.middle,
                #                 step=user.endreg,
                #                 max_step=Config.MAX_REGISTRATION_STEP,
                #                 step_view=data,
                #                 pict_number=str(random.randint(0, Config.MAX_REGISTRATION_PICT_NUMBER)))
                pass
        else:
            self.redirect('/auth')
        self.finish()

    async def post(self):
        data = json.loads(self.request.body)
        result = False
        if data[0] == 'EMAIL':
            pass
        elif data[0] == 'PASSWORD':
            pass
        self.write(json.dumps(result))
        self.finish()

    def get_template_path(self):
        return config.TEMPLATE_PATH