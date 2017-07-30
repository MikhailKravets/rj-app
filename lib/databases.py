"""

This file contains classes that simplifies the work with sqlalchemy.

"""


import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config


def ModelBase():
    """
    This method is just wrapper for DBManager.Base attribute

    :return: sqlalchemy declarative_base link
    """
    return DBManager(**config.DB_ATTR).Base


class __Meta(type):
    """
    This is the metaclass for DBManager class. Such as sqlalchemy creates
    its own connection pool, it would be wise to implement singleton pattern.
    """
    __obj = None

    def __call__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = cls.__new__(cls, *args, **kwargs)
            cls.__obj.clear = cls.clear
            cls.__obj.__init__(*args, **kwargs)
        return cls.__obj

    def clear(cls):
        del cls.__obj


# TODO: append adequate logging
logging.basicConfig(format="%(filename)8s[line: %(lineno)s] %(levelname)3s - %(message)s", level=logging.DEBUG)


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

            * mysqldb
            * mysqlconnector

        """
        waterfall = False
        if driver is None:
            waterfall = True
            driver = 'mysqldb'

        url = f"mysql+{driver}://{user}:{password}@{host}/{database}"
        try:
            self.engine = sqlalchemy.create_engine(url)
        except ModuleNotFoundError as error:
            pass
            if waterfall:
                logging.info("Try to find mysql.connector")
                try:
                    driver = 'mysqlconnector'
                    url = f"mysql+{driver}://{user}:{password}@{host}/{database}"
                    self.engine = sqlalchemy.create_engine(url)
                except ModuleNotFoundError as error:
                    pass
        if self.engine is None:
            raise ModuleNotFoundError("There is no intalled any of mysql drivers!")
        logging.info(f"Mysql engine created; {driver} driver was chosen")
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
