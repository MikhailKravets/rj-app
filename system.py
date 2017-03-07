from config import Config


class User:
    def __init__(self, id_user, login, password, name, access='1', sex='M', email=None, pristine=0, ws=None):
        self.id_user = id_user
        self.login = login
        self.name = name
        self.password = password
        self.access = access
        self.email = email
        self.sex = sex
        self.ws = ws
        self.pristine = pristine
        self.endreg = False if pristine == 0 else 1

    def endreg_step(self):
        if not self.endreg:
            return None
        else:
            if self.endreg <= Config.MAX_REGISTRATION_STEP:
                with open(Config.PATH_CONTENT + 'endreg{}.html'.format(self.endreg), 'rb') as endf:
                    return endf.read().decode('utf8')
            else:
                # TODO: update here DB
                return None

    def update_endreg(self):
        self.endreg += 1