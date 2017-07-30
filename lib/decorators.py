

def authorized(fn):
    async def wrapper(self, *args):
        if self.application.authorized(self.get_cookie('session')):
            await fn(self, *args)
        else:
            inline = self.application.inline_get(self.get_argument('inline', False))
            if inline:
                self.write('DENIED')
            else:
                self.redirect('/auth')
    return wrapper


# TODO: update the 'access=...'
def inline(fn):
    async def wrapper(self, *args):
        inline = self.application.inline_get(self.get_argument('inline', False))
        if inline:
            await fn(self, *args)
        else:
            self.render('main.html', access=Config.users[self.get_cookie('session')].access)
    return wrapper