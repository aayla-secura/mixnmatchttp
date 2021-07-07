import logging
import argparse
import os
from string import Template
from awesomedict import AwesomeDict
import yaml
from yaml import YAMLError


logger = logging.getLogger(__name__)


class Conf(argparse.Namespace):

    def __init__(self, hidden=[], settings={}):
        object.__setattr__(
            self,
            '__hidden__',
            hidden + [
                '__error_on_missing__',
                '__hidden__',
                '__data__',
                '__raw_data__'])
        self.__error_on_missing__ = True
        self.__data__ = {}
        self.__raw_data__ = {}
        self.update(**settings)

    def update(self, **settings):
        for k, v in settings.items():
            setattr(self, k, v)

    def read(self, filename):
        with open(filename, 'r') as f:
            raw_content = f.read()

        env = AwesomeDict(os.environ).set_defaults({'.*': 'null'})
        content = Template(raw_content).substitute(env)
        try:
            settings = yaml.safe_load(content)
            raw_settings = yaml.safe_load(raw_content)
        except YAMLError as e:
            exit('Invalid configuration file: {}'.format(e))

        self.update(**settings)
        self.__raw_data__.update(raw_settings)

    def write(self, filename, raw=True):
        if raw:
            data = self.__raw_data__
        else:
            data = self.__data__

        with open(filename, 'w') as f:
            yaml.dump(data, stream=f, default_flow_style=False)

    def __setattr__(self, key, value):
        if key not in self.__hidden__:
            self.__data__[key] = value
            self.__raw_data__[key] = value
        super().__setattr__(key, value)

    def __getattr__(self, key):
        if self.__error_on_missing__:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    type(self), key))
        return None
