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
        del elem
        elem1 = DBManager(**self.db_attributes)
        self.assertNotEqual(h1, hash(elem1))