#!/usr/bin/env python3
import os

from mixnmatchttp import App
from mixnmatchttp.handlers.authenticator.dbapi import \
    DBBase as UserBase
from file_server import Server, Handler


webapp = App(
    Handler,
    server_cls=Server,
    name='file_server',
    description='File browser',
    support_ssl=True,
    support_cors=True,
    support_daemon=True,
    auth_type='jwt',
    user_conf_key='user_conf',
    db_bases={'user': {'base': UserBase}})

webapp.run()
