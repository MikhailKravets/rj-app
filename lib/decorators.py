from lib.session import HashSession


def authorized(fn):
    async def wrapper(self, *args):
        redis_session = HashSession()
        key = self.get_cookie('session')
        if key not in redis_session:
            inline = self.get_argument('inline', False)
            if inline == '1':
                self.write('DENIED')
            else:
                self.redirect('/auth')

        else:
            self.session = redis_session[key]
            if self.session['activated'] == '0':
                self.redirect('/auth')
            await fn(self, *args)
    return wrapper


def inline(fn):
    async def wrapper(self, *args):
        inline = self.get_argument('inline', False)
        if inline == '1':
            await fn(self, *args)
        else:
            self.render('main.html', access=self.session['access'])
    return wrapper