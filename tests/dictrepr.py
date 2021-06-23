import unittest
import re
from collections import UserDict

import loggers
from mixnmatchttp.types import DictRepr


class NoData(DictRepr):
    dict_prop = None
    skip = '^_'

class WithData(DictRepr):
    dict_prop = 'data'
    skip = '^_'

class NoDataNoSkip(DictRepr):
    dict_prop = None
    skip = None

class WithDataNoSkip(DictRepr):
    dict_prop = 'data'
    skip = None

class Dic(UserDict):
    def only(self, regex):
        return {k: v for k, v in self.items() if re.match(regex, k)}

    def but(self, regex):
        return {k: v for k, v in self.items() if not re.match(regex, k)}

class Test(unittest.TestCase):
    dic = Dic(a=1, _a=1, b=2, _b=2, c=3, _c=3, d=4, _d=4)

    def test_nodata(self):
        d = NoData(a=1, _a=1)
        d.b = 2
        d._b = 2
        d['c'] = 3
        d['_c'] = 3
        d['d'] = 4
        d['_d'] = 4
        attrs = Dic(d.__dict__).but('_DictRepr__|data$')
        #  print(d)
        #  print(attrs)
        #  return
        self.assertDictEqual(self.dic.data, attrs)
        self.assertDictEqual(self.dic.only('[a-d]$'), dict(d))

    def test_withdata(self):
        d = WithData(a=1, _a=1)
        d.b = 2
        d._b = 2
        d['c'] = 3
        d['_c'] = 3
        d.data['d'] = 4
        d.data['_d'] = 4
        attrs = Dic(d.__dict__).but('_DictRepr__|data$')
        #  print(d)
        #  print(attrs)
        #  return
        self.assertDictEqual(self.dic.but('_?d$'), attrs)
        self.assertDictEqual(self.dic.but('_[a-c]$'), dict(d))

    def test_nodata_noskip(self):
        d = NoDataNoSkip(a=1, _a=1)
        d.b = 2
        d._b = 2
        d['c'] = 3
        d['_c'] = 3
        d['d'] = 4
        d['_d'] = 4
        attrs = Dic(d.__dict__).but('_DictRepr__|data$')
        #  print(d)
        #  print(attrs)
        #  return
        self.assertDictEqual(self.dic.data, attrs)
        self.assertDictEqual(self.dic.data, dict(d))

    def test_withdata_noskip(self):
        d = WithDataNoSkip(a=1, _a=1)
        d.b = 2
        d._b = 2
        d['c'] = 3
        d['_c'] = 3
        d.data['d'] = 4
        d.data['_d'] = 4
        attrs = Dic(d.__dict__).but('_DictRepr__|data$')
        #  print(d)
        #  print(attrs)
        #  return
        self.assertDictEqual(self.dic.but('_?d$'), attrs)
        self.assertDictEqual(self.dic.data, dict(d))


if __name__ == '__main__':
    unittest.main()
