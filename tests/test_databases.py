import unittest
from lib.databases import DBManager


class TestDBManager(unittest.TestCase):
    def setUp(self):
        self.db_attributes = {
            'user': 'rjournal',
            'password': 'rjournal',
            'host': 'localhost',
            'database': 'rjdb'
        }

    def test_singleton(self):
        elem = DBManager(**self.db_attributes)
        elem1 = DBManager(**self.db_attributes)
        self.assertEqual(elem, elem1)

    def test_del_singleton(self):
        elem = DBManager(**self.db_attributes)
        h1 = hash(elem)
        elem.clear()
        elem1 = DBManager(**self.db_attributes)
        self.assertNotEqual(h1, hash(elem1))

    def test_add_query(self):
        """
        Test sqlalchemy where User.password is native Mysql SHA2 function.
        I guess it must be changed on Python's one
        """
        from main.models import User
        user = User(login='delete', password='delete', first_name='Геннадий', last_name='Блок')
        db = DBManager(**self.db_attributes)
        session = db.Session()
        session.add(user)
        user2 = session.query(User).filter(User.login == user.login).first()
        session.commit()

        if self.assertEqual(user, user2):
            self.assertIsNotNone(user.id)
