r"""

This file must contain classes for easy managing of databases modules.

It can work either with MySQLdb library or mysql.connector. Just use
``SQLExecutor(...)`` function. By default it choose MySQLdb because
it is implemented on C and therefore is faster than mysql.connector
but you can choose mysql.connector by setting the argument ``use_mysqldb=False``

"""


import logging
from sqlalchemy.ext.declarative import declarative_base
from abc import abstractmethod

from config import Config


def ModelBase():
    r"""
    Use this function in order to construct your own object-relational models.

    :return: sqlalchemy declarative base link
    """
    return declarative_base()


def SQLExecutor(use_mysqldb=True):
    r"""
    This function returns one of the ``AbstractMySQL`` child class object
    (depending on the library it should use).

    Sometimes there is a problem with installing of MySQLdb on Linux, so it is
    reasonable to use mysql.connector. But it is preferable to use MySQLdb because it is
    implemented on C while mysql.connector is implemented on Python.

    :param use_mysqldb: set this variable to ``False`` if you want to work with mysql.connector.
    :return: One of the child of __AbstractMySQL: class object that simplifies the work with MySQL.
    """
    if use_mysqldb:
        import MySQLdb
        return __MySQLdb()
    if not use_mysqldb:
        import mysql.connector
        return __MySQLConnector()


class AbstractMySQL:
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
class __MySQLdb(AbstractMySQL):
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


class __MySQLConnector(AbstractMySQL):
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