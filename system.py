import logging

from config import Config, DBManager


class _Interface:
    def __init__(self, obj, id_user, login, name, access, sex, email, pristine, ws):
        self.obj = obj
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
        self.db = None #DBManager()

    def init_db(self):
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
                for retr in self.db.execute(query):
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

    # low moder
    def new_group(self, data):
        self.obj.new_group(data)

    def new_load(self, data):
        self.obj.new_load(data)

    def choice(self, data):
        self.obj.choice_load(data)

    # high moder
    def add_discipline(self, data):
        self.obj.add_discipline(data)

    # teacher
    def choice_load(self, id_user, data_like):
        self.obj.choice_load(id_user, data_like)

    def journ_step(self, data_like):
        self.obj.journ_step(data_like)

    # admin


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

    def specify(self):
        tup = self.id_user, self.login, (self.first, self.middle, self.last), self.access, self.sex, self.email, self.pristine, self.ws
        obj = self
        if '1' in self.access:
            obj = Teacher(obj, *tup)
        if '2' in self.access:
            obj = LowModerator(obj, *tup)
        if '3' in self.access:
            obj = HighModerator(obj, *tup)
        if '4' in self.access:
            obj = Admin(obj, *tup)
        obj.init_db()
        return obj


class LowModerator(_Interface):
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
                self.db.connection.autocommit(True)
                return ['ERROR', 'duplicate']
            elif 'Operational' in retr:
                self.db.connection.rollback()
                self.db.connection.autocommit(True)
                return ['ERROR', 'operational']
            elif 'Error' in retr:
                self.db.connection.rollback()
                self.db.connection.autocommit(True)
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
        self.db.connection.autocommit(True)
        return ['OK']

    def new_load(self, data):
        self.db.connection.autocommit(False)
        query = """INSERT INTO loads
                   (teacher_id, discipline_id, group_id, semester, year,
                    lecture, practice, labor, seminar,
                    self_lecture, self_practice, self_labor, self_seminar)
                    VALUES
                    ((SELECT id FROM users WHERE CONCAT(last, ' ', first, ' ', middle) = '{0[teacher]}'),
                     (SELECT id FROM disciplines WHERE name='{0[discipline]}'),
                     (SELECT id FROM groups WHERE name='{0[group]}'),
                     {0[semester]}, {0[year]},
                     {0[lecture]}, {0[practice]}, {0[labor]}, {0[seminar]},
                     {0[self_lecture]}, {0[self_practice]}, {0[self_labor]}, {0[self_seminar]})"""
        query = query.format(data)

        for retr in self.db.execute(query):
            if 'Error' in retr:
                self.db.connection.rollback()
                self.db.connection.autocommit(True)
                return ['ERROR', 'unknown']

        query = """SELECT COUNT(id) FROM loads WHERE
                    teacher_id=(SELECT id FROM users WHERE CONCAT(last, ' ', first, ' ', middle) = '{0[teacher]}')
                    AND
                    discipline_id=(SELECT id FROM disciplines WHERE name='{0[discipline]}')
                    AND
                    group_id=(SELECT id FROM groups WHERE name='{0[group]}')
                    AND
                    semester={0[semester]}"""
        query = query.format(data)

        length = 0
        for retr in self.db.execute(query):
            length = retr[0]
        logging.debug('LENGTH: {}'.format(length))
        if length > 1:
            self.db.connection.rollback()
            self.db.connection.autocommit(True)
            return ['ERROR', 'multiple']
        else:
            self.db.connection.commit()
            self.db.connection.autocommit(True)
            return ['OK']

    def choice(self, data):
        if data[1] == 'teacher':
            return self.__teacher_choice(data[2])
        elif data[1] == 'group':
            return self.__group_choice(data[2])
        elif data[1] == 'discipline':
            return self.__discipline_choice(data[2])
        else:
            return ['ERROR', 'unknown']

    def __teacher_choice(self, data):
        query = """SELECT CONCAT(last, ' ', first, ' ', middle) as n, email
                   FROM users
                   WHERE access LIKE '%1%' AND (CONCAT(last, ' ', first, ' ', middle) LIKE '%{0}%')
                   ORDER BY n LIMIT 10"""
        query = query.format(data)
        return self.__exec_choice(query)

    def __group_choice(self, data):
        query = """SELECT name as n, specialty
                   FROM groups
                   WHERE name LIKE '%{0}%'
                   ORDER BY n LIMIT 10"""
        query = query.format(data)
        return self.__exec_choice(query)

    def __discipline_choice(self, data):
        query = """SELECT name, code FROM disciplines
                   WHERE name LIKE '%{0}%' ORDER BY name LIMIT 10"""
        query = query.format(data)
        return self.__exec_choice(query)

    def __exec_choice(self, query):
        result = []
        for retr in self.db.execute(query):
            if 'Error' in retr:
                return ['ERROR']
            else:
                result.append({'first': retr[0], 'second': retr[1]})
        return ['OK', result]


class HighModerator(_Interface):
    def add_discipline(self, data):
        query = """INSERT INTO disciplines (name, feature, cycle, code)
                   VALUES ('{0[name]}', '{0[feature]}', '{0[cycle]}', '{0[code]}')"""
        query = query.format(data)
        logging.debug("Query: {}".format(query))
        for retr in self.db.execute(query):
            if 'Integrity' in retr:
                self.db.connection.rollback()
                return ['ERROR', 'duplicate']
            elif 'Error' in retr:
                self.db.connection.rollback()
                return ['ERROR', 'unknown']
        #self.db.connection.commit()
        return ['OK']


class Teacher(_Interface):
    def __init__(self, obj, *tup):
        super().__init__(obj, *tup)
        self.module_amount = 1
        self.semester = 0
        self.program_id = 0
        self.new_time = None
        self.new_marks = None
        self.add_dictionary = {}
        self.NEW_JOURN_STEP = 1
        self.MAX_JOURN_STEPS = 2

    def choice_load(self, id_user, data_like):
        query = """SELECT d.name, l.semester, l.id
                   FROM disciplines AS d
                   INNER JOIN loads as l ON d.id=l.discipline_id
                   WHERE d.name LIKE '%{}%'
                   AND
                   l.teacher_id={}
                   AND
                   l.id NOT IN (SELECT load_id FROM journal_hours)""".format(data_like, id_user)
        logging.debug("HERE: {}".format(self.NEW_JOURN_STEP))
        return self.__exec_choice(query)

    def update_journ_step(self, data):
        if self.NEW_JOURN_STEP == 1:
            self.add_dictionary = data
        elif self.NEW_JOURN_STEP == 2:
            pass
        self.NEW_JOURN_STEP += 1

    def journ_step(self, data):
        logging.debug("DATA: {}".format(data))
        if 'id' in data:
            id_load = data['id']
            if self.program_id != id_load:
                self.NEW_JOURN_STEP = 1
                self.program_id = id_load
        if self.NEW_JOURN_STEP <= Config.MAX_REGISTRATION_STEP:
            logging.debug("AND HERE: {}".format(self.NEW_JOURN_STEP))
            render_object, cl_model = self.__render_step(self.NEW_JOURN_STEP, self.program_id)
            return [self.NEW_JOURN_STEP, self.MAX_JOURN_STEPS,
                    '{}journ{}.html'.format(Config.PATH_CONTENT, self.NEW_JOURN_STEP), render_object, cl_model]
        else:
            return None

    def __render_step(self, step, load_id):
        if step == 1:
            query = """SELECT semester,
                       lecture, practice, labor, seminar,
                       self_lecture, self_practice, self_labor, self_seminar
                       FROM loads
                       WHERE id={}""".format(load_id)
            for retr in self.db.execute(query):
                if 'Error' not in retr:
                    return {
                        'semester': retr[0],
                        'lecture': retr[1],
                        'practice': retr[2],
                        'labor': retr[3],
                        'seminar': retr[4],
                        'self_lecture': retr[5],
                        'self_practice': retr[6],
                        'self_labor': retr[7],
                        'self_seminar': retr[8],
                        'audit': retr[1] + retr[2] + retr[3] + retr[4],
                        'selfh': retr[8] + retr[7] + retr[6] + retr[5],
                    }, {
                        'lecture': retr[1],
                        'practice': retr[2],
                        'labor': retr[3],
                        'seminar': retr[4],
                        'self_lecture': retr[5],
                        'self_practice': retr[6],
                        'self_labor': retr[7],
                        'self_seminar': retr[8],
                    }
            return None, None
        elif step == 2:
            rend = {
                'visit': 0,
                'lecture': 0,
                'practice': 0,
                'labor': 0,
                'seminar': 0,
                'AKR': 0,
                'DKR': 0,
                'MK': 0,

                'visit2': 0,
                'lecture2': 0,
                'practice2': 0,
                'labor2': 0,
                'seminar2': 0,
                'AKR2': 0,
                'DKR2': 0,
                'MK2': 0
            }
            if self.add_dictionary['lecture'] == '' or self.add_dictionary['lecture'] == '0': rend['lecture'] = -1
            if self.add_dictionary['practice'] == '' or self.add_dictionary['practice'] == '0': rend['practice'] = -1
            if self.add_dictionary['labor'] == '' or self.add_dictionary['labor'] == '0': rend['labor'] = -1
            if self.add_dictionary['seminar'] == '' or self.add_dictionary['seminar'] == '0': rend['seminar'] = -1
            if self.add_dictionary['lecture2'] == '' or self.add_dictionary['lecture2'] == '0': rend['lecture2'] = -1
            if self.add_dictionary['practice2'] == '' or self.add_dictionary['practice2'] == '0': rend['practice2'] = -1
            if self.add_dictionary['labor2'] == '' or self.add_dictionary['labor2'] == '0': rend['labor2'] = -1
            if self.add_dictionary['seminar2'] == '' or self.add_dictionary['seminar2'] == '': rend['seminar2'] = -1

            if self.add_dictionary['module_amount'] == '1':
                rend['wc1'] = 1
                rend['wc2'] = 0
            else:
                rend['wc1'] = 0.5
                rend['wc2'] = 0.5
            return rend, None

    def __exec_choice(self, query):
        result = []
        for retr in self.db.execute(query):
            if 'Error' in retr:
                return ['ERROR']
            else:
                result.append({'first': retr[0], 'second': retr[1], 'third': retr[2]})
        return ['OK', result]


class Admin(_Interface):
    pass

