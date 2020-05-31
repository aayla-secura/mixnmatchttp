from ._py2 import *

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
