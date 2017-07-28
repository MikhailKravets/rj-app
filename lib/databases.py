r"""

This file contains classes that simplifies the work with sqlalchemy.

From official documentation:

The MySQL dialect uses mysql-python as the default DBAPI. There are many MySQL DBAPIs available, including MySQL-connector-python and OurSQL:

# default

``engine = create_engine('mysql://scott:tiger@localhost/foo')``

# mysql-python

``engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')``

# MySQL-connector-python

``engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')``

# OurSQL

``engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')``

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

# TODO: anyway we need to explicitly choose the right engine (mysqldb or mysqlconnector) for sqlalchemy