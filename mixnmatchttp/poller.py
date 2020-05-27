#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

from .utils import datetime_from_timestamp
from uuid import uuid4 as uuid


class Poller:
    def __init__(self):
        self.update()

    @property
    def latest(self):
        return self.__latest

    @property
    def last_change(self):
        return self.__last_change

    def update(self):
        self.__last_change = datetime_from_timestamp(
            0, to_utc=False, relative=True)
        self.__latest = str(uuid())

    def is_match(self, tag):
        return self.__latest == tag
