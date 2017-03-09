import logging

from config import Config, DBManager


class User:
    def __init__(self, id_user, login, name, access='1', sex='M', email=None, pristine=0, ws=None):
        self.id_user = id_user
        self.login = login
        self.first = name[0]
        self.middle = name[1]
        self.last = name[2]
        self.password = False
        self.access = access
        self.email = email
        self.sex = sex
        self.ws = ws
        self.pristine = pristine
        self.endreg = False if pristine == 0 else 1
        self.db = DBManager()

        self.teacher = None
        self.admin = None
        self.low = None
        self.high = None
        self.__specify()

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

    def update_settings(self, data):
        query = """UPDATE users SET """
        if 'login' in data:
            query += " login ='{0[login]}',"
        if 'email' in data:
            query += " email='{0[email]}',"
        if 'first' in data:
            query += " first='{0[first]}',"
        if 'middle' in data:
            query += " middle='{0[middle]}',"
        if 'last' in data:
            query += " last='{0[last]}',"
        if 'password' in data:
            query += " password=SHA2('{0[password]}', 224),"
        query = query[:-1]
        query += " WHERE id={1}"
        query = query.format(data, self.id_user)
        logging.debug("QUERY: {}".format(query))
        for retr in self.db.execute(query):
            if 'Integrity' in retr:
                return ['ERROR', 'duplicate']
            elif 'Operational' in retr:
                return ['ERROR', 'operational']
            elif 'Error' in retr:
                logging.debug('ERROR: {}'.format(retr))
                return ['ERROR', 'unknown']
        self.__update_session(data)
        return ['OK']

    def __specify(self):
        if '1' in self.access:
            self.teacher = Teacher(self.db)
        if '2' in self.access:
            self.low = LowModerator(self.db)
        if '3' in self.access:
            self.high = HighModerator(self.db)
        if '4' in self.access:
            self.admin = Admin(self.db)

    def __update_session(self, data):
        if 'login' in data:
            self.login = data['login']
        if 'email' in data:
            self.email = data['email']
        if 'first' in data:
            self.first = data['first']
        if 'middle' in data:
            self.middle = data['middle']
        if 'last' in data:
            self.last = data['last']


class LowModerator:
    def __init__(self, db):
        self.db = db

    def new_group(self, data):
        self.db.connection.autocommit(False)
        query = """INSERT INTO groups (name, specialty, finance_form, study_form, university, qualification)
                   VALUES
                   ('{0[name]}', '{0[specialty]}', '{0[finance_form]}',
                   '{0[study_form]}', '{0[university]}', '{0[qualification]}')"""
        query = query.format(data)
        for retr in self.db.execute(query):
            logging.debug(retr)
            if 'Integrity' in retr:
                self.db.connection.rollback()
                return ['ERROR', 'duplicate']
            elif 'Operational' in retr:
                self.db.connection.rollback()
                return ['ERROR', 'operational']
            elif 'Error' in retr:
                self.db.connection.rollback()
                return ['ERROR', 'unknown']

        last_id = self.db.cursor.lastrowid
        query = """INSERT INTO students (group_id, first, middle, last, sex, privilege, finance_form)
                   VALUES """
        for v in data['students']:
            query += "({1}, '{0[first]}', '{0[middle]}', '{0[last]}', '{0[sex]}', '{0[privilege]}', '{0[finance_form]}'), ".format(v, last_id)
        query = query[:-2]
        for retr in self.db.execute(query):
            logging.debug(retr)
            if 'Error' in retr:
                self.db.connection.rollback()
                return ['ERROR', 'unknown']
        self.db.connection.commit()
        return ['OK']


class HighModerator:
    def __init__(self, db):
        self.db = db

    def high(self):
        pass


class Teacher:
    def __init__(self, db):
        self.db = db


class Admin:
    def __init__(self, db):
        self.db = db

    def admin(self):
        pass

