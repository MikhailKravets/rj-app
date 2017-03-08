import logging

from config import Config, DBManager


class User:
    def __init__(self, id_user, login, name, access='1', sex='M', email=None, pristine=0, ws=None):
        self.id_user = id_user
        self.login = login
        self.name = name
        self.password = False
        self.access = access
        self.email = email
        self.sex = sex
        self.ws = ws
        self.pristine = pristine
        self.endreg = False if pristine == 0 else 1
        self.db = DBManager()

    def endreg_step(self):
        if not self.endreg:
            return None
        else:
            if self.endreg <= Config.MAX_REGISTRATION_STEP:
                with open(Config.PATH_CONTENT + 'endreg{}.html'.format(self.endreg), 'rb') as endf:
                    return endf.read().decode('utf8')
            else:
                return None

    def update_endreg(self):
        if self.endreg == Config.MAX_REGISTRATION_STEP:
            if self.db:
                logging.debug("Finish this shit")
                self.email = Config.escape(self.email)
                self.password = Config.escape(self.password)
                query = """UPDATE users SET email='{}', password=SHA2('{}', 224), pristine=0 WHERE id={}"""
                query = query.format(self.email, self.password, self.id_user)
                logging.debug("QUery: {}".format(query))
                for retr in self.db.execute(query):
                    logging.debug('Res: {}'.format(retr))
                    if 'Integrity' in retr:
                        return ['ERROR', 'duplicate']
                self.pristine = 0
            return ['FINISH']
        else:
            self.endreg += 1