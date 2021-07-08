import unittest
import re
from copy import copy, deepcopy

import loggers
from mixnmatchttp.containers import DefaultAttrDict, CaseInsensitiveOrderedDict

class Mergeable(DefaultAttrDict):
    __attempt_merge__ = True

class HoldsSet(DefaultAttrDict):
    __item_type__ = set

class Double(DefaultAttrDict):
    __item_type__ = int

    def __transform__(self, x):
        return x * 2

class TestDicts(unittest.TestCase):
    def test(self):
        d = CaseInsensitiveOrderedDict(FoO='bar')
        self.assertEqual(str(d), "{'FoO': 'bar'}")
        self.assertIn('fOo', d)
        self.assertEqual(d['fOo'], 'bar')
        self.assertEqual(d.getkey('fOo'), 'FoO')

class TestDefaults(unittest.TestCase):
    def test_attr_item(self):
        s = DefaultAttrDict(dict(a=1, b=2), c=3)
        s.d = 4
        s['e'] = 5
        self.assertEqual(s.a, s['a'])
        self.assertEqual(s.b, s['b'])
        self.assertEqual(s.c, s['c'])
        self.assertEqual(s.d, s['d'])
        self.assertEqual(s.e, s['e'])

    def test_defaults_a(self):
        s = DefaultAttrDict()
        s.setdefaults(a=1)
        s.setdefault('b', 2)
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        self.assertRaises(KeyError, lambda k: s[k], 'c')
        self.assertNotIn('a', s)
        self.assertNotIn('b', s)

    def test_defaults_b(self):
        s = DefaultAttrDict(a=1)
        s.setdefaults(a=2, b=2)
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        s['b'] = 3
        self.assertEqual(s['b'], 3)

    def test_equal(self):
        s = DefaultAttrDict(a=1)
        p = DefaultAttrDict(a=1)
        s.setdefaults(b=[1, 2])
        p.setdefaults(b=[1, 2])
        self.assertEqual(s, p)
        p.setdefaults(c=3)
        self.assertNotEqual(s, p)

    def test_copy(self):
        s = DefaultAttrDict(dict(a=1, b=2))
        s['c'] = [1, 2]
        c = copy(s)
        self.assertEqual(c, s)
        self.assertEqual(c['a'], 1)
        c['c'].append(3)
        self.assertEqual(c, s)
        self.assertIn(3, c['c'])
        self.assertIn(3, s['c'])
        c['a'] = 'a'
        self.assertNotEqual(c, s)

    def test_deepcopy(self):
        s = DefaultAttrDict(dict(a=1, b=2))
        s['c'] = [1, 2]
        c = deepcopy(s)
        self.assertEqual(c, s)
        self.assertEqual(c['a'], 1)
        c['c'].append(3)
        self.assertIn(3, c['c'])
        self.assertNotIn(3, s['c'])
        c['a'] = 'a'
        self.assertNotEqual(c, s)

    def test_merge(self):
        s = Mergeable(dict(a=[1, 2]), b=[1, 2, 3], c=1)
        s.a = [3, 4]
        s.b = [4, 5]
        s.c = [1, 2]
        self.assertEqual(s.a, [3, 4])  # orig was default
        self.assertEqual(s.b, [1, 2, 3, 4, 5])
        self.assertEqual(s.c, [1, 2])

    def test_update(self):
        s = DefaultAttrDict(a=1, c=3)
        p = DefaultAttrDict(a=2, d=4)
        s.setdefaults(b=2, d=5)
        p.setdefaults(b=3, c=6, e=6)
        s.update(p)
        self.assertEqual(s['a'], 2)
        self.assertEqual(s['c'], 3)
        self.assertEqual(s['d'], 4)
        self.assertEqual(s['b'], 3)
        self.assertEqual(s['e'], 6)

    def test_delete(self):
        s = DefaultAttrDict(a=1, b=2)
        del s['a']
        self.assertNotIn('a', s)

    def test_iter(self):
        s = DefaultAttrDict(a=1)
        s.b = 2
        self.assertEqual(list(s), ['a', 'b'])

    def test_add(self):
        s = DefaultAttrDict(dict(a=1, c=3), x=3, y=4)
        p = DefaultAttrDict(dict(a=2, d=4), x=2, z=5)
        u = s + p
        self.assertEqual(s.a, 1)
        self.assertEqual(s.c, 3)
        self.assertNotIn('d', s)
        self.assertEqual(s.x, 3)
        self.assertEqual(s.y, 4)
        self.assertNotIn('z', s)
        self.assertEqual(u.a, 2)
        self.assertEqual(u.c, 3)
        self.assertEqual(u.d, 4)
        self.assertEqual(u.x, 2)
        self.assertEqual(u.y, 4)
        self.assertEqual(u.z, 5)
        s += p
        self.assertEqual(s, u)

    def test_conv_a(self):
        s = HoldsSet(a=[1, 2, 1, 3])
        self.assertEqual(s.a, set([1, 2, 3]))

    def test_conv_b(self):
        s = Double(a='1', b=1.1)
        self.assertEqual(s.a, 2)
        self.assertEqual(s.b, 2)

    def test_public(self):
        dicta = dict(a=1)
        dictb = dict(b=2)
        s = DefaultAttrDict(dicta, **dictb)
        self.assertEqual(list(s.keys()), list(dictb.keys()))
        self.assertEqual(list(s.defaultkeys()), list(dicta.keys()))
        self.assertEqual(list(s.values()), list(dictb.values()))
        self.assertEqual(list(s.defaultvalues()), list(dicta.values()))
        self.assertEqual(list(s.items()), list(dictb.items()))
        self.assertEqual(list(s.defaultitems()), list(dicta.items()))


if __name__ == '__main__':
    unittest.main()
