r"""

This file contains classes that simplifies the work with sqlalchemy.

"""


import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from abc import abstractmethod

from config import Config


def ModelBase():
    """
    Use this function in order to construct your own object-relational models.

    :return: sqlalchemy declarative base link
    """
    return declarative_base()


class __Meta(type):
    """
    This is the metaclass for DBManager class. Such as sqlalchemy creates
    its own connection pool, it would be wise to implement singleton pattern.
    """
    __obj = None

    def __call__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = cls.__new__(cls, *args, **kwargs)
            cls.__obj.__init__(*args, **kwargs)
        return cls.__obj


# TODO: append adequate logging
class DBManager(metaclass=__Meta):
    """
    This class implements singleton pattern in order to have one sqlalchemy engine.
    By default **DBManager** will look up the mysqldb driver but if it is not found
    **DBManager** will try to use mysql.connector.
    """
    def __init__(self, user, password, host, database, driver=None):
        """
        You can explicitly indicate which mysql driver to use via driver variable

        :param user: user name
        :param password: user password
        :param host:
        :param database: database name
        :param driver: mysql driver name. This variable is None by default;
        it means that **DBManager** will automatically choose mysql driver.
        Firstly, it will try to use mysqldb. If it is not found it will
        try to use mysql.connector.

        The variable can be set to next values:

            #. mysqldb
            #. mysqlconnector

        """
        waterfall = False
        if driver is None:
            waterfall = True
            driver = 'mysqldb'

        url = f"mysql+{driver}://{user}:{password}@{host}/{database}"
        try:
            self.engine = sqlalchemy.create_engine(url)
        except Exception as error:
            print(error)
            if waterfall:
                try:
                    driver = 'mysqlconnector'
                    url = f"mysql+{driver}://{user}:{password}@{host}/{database}"
                    self.engine = sqlalchemy.create_engine(url)
                except Exception as error:
                    print(error)
        if self.engine is None:
            print("IT IS COMPLETELY NONE. CRITICAL ERROR")
        print("EXCELLENT")
