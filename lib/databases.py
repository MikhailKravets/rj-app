"""
This file contains classes that simplifies the work with sqlalchemy.
"""


from lib import __SingletonMeta
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
    return DBManager(**config.MYSQL_ATTR).Base


# TODO: append adequate logging
logging.basicConfig(format="%(filename)8s[line: %(lineno)s] %(levelname)3s - %(message)s", level=logging.DEBUG)


class DBManager(metaclass=__SingletonMeta):
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
            * pymysql
        """
        driver = self.__get_driver(driver)

        url = f"mysql+{driver}://{user}:{password}@{host}/{database}?charset=utf8"
        try:
            self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        except ModuleNotFoundError as error:
            raise ModuleNotFoundError("There is no intalled any of mysql drivers!")

        logging.info(f"Mysql engine created; {driver} driver was chosen")
        self.Base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)

    def __get_driver(self, driver):
        if driver is not None:
            return driver

        try:
            import MySQLdb
            return 'mysqldb'
        except ModuleNotFoundError:
            pass

        try:
            import mysql.connector
            return 'mysqlconnector'
        except ModuleNotFoundError:
            pass

        try:
            import pymysql
            return 'pymysql'
        except ModuleNotFoundError:
            pass

        return None
