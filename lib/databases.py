"""

This file must contain classes for easy managing of databases modules.\n
I.e. make an opportunity to choose between mysqldb or mysql-connector.\n
Provide functionality for sqlalchemy with earlier (↑) created classes.

"""


import MySQLdb
import logging

from config import Config


# TODO: sort out this shit and delete it from config.py
# TODO: create the same but for mysql-connector
class _MySQLdbManager:
    def __init__(self):
        self.connection = MySQLdb.connect(**Config.DB, charset='utf8')
        logging.debug("CREATE CONNECTION TO DB")
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection = MySQLdb.connect(**Config.DB, charset='utf8')
        self.cursor = self.connection.cursor()

    def execute(self, query):
        try:
            self.cursor.execute(query)
            yield from self.cursor.fetchall()
        except MySQLdb.IntegrityError as error:
            logging.error('MySQL integrity error: {}'.format(error))
            yield 'IntegrityError'
        except MySQLdb.OperationalError as error:
            logging.error('MySQL operational error: {}'.format(error))
            yield 'OperationalError'
        except MySQLdb.Error as error:
            logging.error('MySQL error: {}'.format(error))
            yield 'Error'

    def close(self):
        try:
            self.connection.close()
        except MySQLdb.ProgrammingError:
            pass

    def __del__(self):
        self.connection.close()