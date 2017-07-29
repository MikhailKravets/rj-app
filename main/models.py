import sqlalchemy
from lib.databases import ModelBase


Base = ModelBase()


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    login = sqlalchemy.Column(sqlalchemy.String(85), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String(85), nullable=False)
    middle_name = sqlalchemy.Column(sqlalchemy.String(85), nullable=True)
    last_name = sqlalchemy.Column(sqlalchemy.String(85), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.String(1), nullable=False, server_default='M')
    access = sqlalchemy.Column(sqlalchemy.String(10), nullable=False, server_default='1')
    activated = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=False, server_default='1')


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, unique=True)
    feature = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    cycle = sqlalchemy.Column(sqlalchemy.String(85), nullable=False)
    code = sqlalchemy.Column(sqlalchemy.String(25), nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
