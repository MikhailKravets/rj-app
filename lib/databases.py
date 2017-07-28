r"""

This file must contain classes for easy managing of databases modules.
I.e. make an opportunity to choose between mysqldb or mysql-connector.
Provide functionality for sqlalchemy with earlier (↑) created classes.

"""


import logging
from sqlalchemy.ext.declarative import declarative_base
from abc import abstractmethod

from config import Config


def ModelBase():
    r"""
    Use this method to generate sqlalchemy Base class in order to extend models.
    """
    return declarative_base()


def SQLExecutor(use_mysqldb=True):
    r"""
    This is class-like function. Such as there is a problom with installing of MySQLdb on Linux,
    it is reasonable to use mysql.connector.
    It is preferable to use MySQLdb beacue it is implemented on C while mysql.connector is
    implemented on Python.

    The function imports needed library and then return class that works with this library.
    :param use_mysqldb: boolean variable that defines whether it should be used MySQLdb or not.
    :return: One of the child of __AbstractMySQL: class object that simplifies the work with MySQL.
    """
    if use_mysqldb:
        import MySQLdb
        return __MySQLdb()
    if not use_mysqldb:
        import mysql.connector
        return __MySQLConnector()


class __AbstractMySQL:
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def raw(self, query):
        pass

    @abstractmethod
    def close(self):
        pass


# TODO: sort out this shit and delete it from config.py
# TODO: create the same but for mysql-connector
class __MySQLdb(__AbstractMySQL):
    def __init__(self):
        self.connection = MySQLdb.connect(**Config.DB, charset='utf8')
        logging.debug("CREATE CONNECTION TO DB")
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection = MySQLdb.connect(**Config.DB, charset='utf8')
        self.cursor = self.connection.cursor()

    def raw(self, query):
        try:
            self.cursor.raw(query)
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


class __MySQLConnector(__AbstractMySQL):
    def __init__(self):
        pass

    def connect(self):
        pass

    def raw(self, query):
        pass

    def close(self):
        pass

    def __del__(self):
        pass