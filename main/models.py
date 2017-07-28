import sqlalchemy
from lib.databases import ModelBase


Base = ModelBase()


class User(Base):
    __table_name__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    middle_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    access = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    activated = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=False)


class Discipline(Base):
    __table_name = 'disciplines'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    feature = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    cycle = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    code = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Teacher(Base):
    __table_name = 'teachers'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
