#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

from sqlalchemy import Table, Column, ForeignKey, \
    Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from .api import BaseAuthHTTPRequestHandler, \
    User, Role, Session


DBBase = declarative_base()


class DBUser(DBBase, User):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    roles = relationship(
        'DBRole', lazy='joined', secondary='association_user_role')

class DBRole(DBBase, Role):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    users = relationship(
        'DBUser', lazy='joined', secondary='association_user_role')

class DBSession(DBBase, Session):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(
        'DBUser', lazy='joined',
        backref=backref('sessions', lazy='joined', uselist=True))
    token = Column(String(250), nullable=False, unique=True)
    expiry = Column(DateTime)


Table(
    'association_user_role', DBBase.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('user_id', Integer, ForeignKey('user.id')))
