#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

from uuid import uuid4 as uuid


class Poller:
    def __init__(self):
        self.update()

    @property
    def latest(self):
        return self.__latest

    def update(self):
        self.__latest = str(uuid())

    def is_match(self, tag):
        return self.__latest == tag
