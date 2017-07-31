from lib.session import HashSession


def authorized(access_level='1'):
    async def higher_wrapper(fn):
        async def write(self):
            inline = self.get_argument('inline', False)
            if inline == '1':
                self.write('DENIED')
                self.finish()
            else:
                self.redirect('/auth')

        async def wrapper(self, *args):
            redis_session = HashSession()
            key = self.get_cookie('session')
            if key not in redis_session:
                write(self)
            else:
                self.session = redis_session[key]
                if self.session['activated'] == '0' and access_level not in self.session['access']:
                    write(self)
                await fn(self, *args)
        return wrapper
    return higher_wrapper


def inline(fn):
    async def wrapper(self, *args):
        inline = self.get_argument('inline', False)
        if inline == '1':
            await fn(self, *args)
        else:
            self.render('main.html', access=self.session['access'])
    return wrapper