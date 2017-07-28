r"""

This file contains classes that simplifies the work with sqlalchemy

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