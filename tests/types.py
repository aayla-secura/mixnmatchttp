import unittest
import re

import loggers
from mixnmatchttp.types import ObjectWithDefaults, DictWithDefaults

class TestObjectWithDefaults(unittest.TestCase):
    def test_attr_item(self):
        s = ObjectWithDefaults(dict(a=1, b=2), c=3)
        s.d = 4
        s['e'] = 5
        self.assertEqual(s.a, s['a'])
        self.assertEqual(s.b, s['b'])
        self.assertEqual(s.c, s['c'])
        self.assertEqual(s.d, s['d'])
        self.assertEqual(s.e, s['e'])

    def test_defaults(self):
        s = ObjectWithDefaults(dict(a=1, b=2))
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, 2)
        self.assertRaises(AttributeError, lambda _: s.c, 'ignored')
        self.assertRaises(KeyError, lambda k: s[k], 'c')
        self.assertNotIn('a', s)
        self.assertNotIn('b', s)

    def test_equal(self):
        s = ObjectWithDefaults(dict(a=1, b=[1, 2]), a=1)
        p = ObjectWithDefaults(dict(a=1, b=[1, 2]), a=1)
        self.assertEqual(s, p)
        p = ObjectWithDefaults(dict(a=1, c=[1, 2]), a=1)
        self.assertNotEqual(s, p)

    def test_iter(self):
        s = ObjectWithDefaults(a=1)
        s.b = 2
        self.assertEqual(list(s), ['a', 'b'])

    def test_add(self):
        s = ObjectWithDefaults(dict(a=1, c=3), x=3, y=4)
        p = ObjectWithDefaults(dict(a=2, d=4), x=2, z=5)
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

class TestDictWithDefaults(unittest.TestCase):
    def test_defaults_a(self):
        s = DictWithDefaults()
        s.setdefaults(a=1)
        s.setdefault('b', 2)
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        self.assertRaises(KeyError, lambda k: s[k], 'c')
        self.assertNotIn('a', s)
        self.assertNotIn('b', s)

    def test_defaults_b(self):
        s = DictWithDefaults(a=1)
        s.setdefaults(a=2, b=2)
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        s['b'] = 3
        self.assertEqual(s['b'], 3)

    def test_equal(self):
        s = DictWithDefaults(a=1)
        p = DictWithDefaults(a=1)
        s.setdefaults(b=[1, 2])
        p.setdefaults(b=[1, 2])
        self.assertEqual(s, p)
        p.setdefaults(c=3)
        self.assertNotEqual(s, p)

    def test_copy(self):
        s = DictWithDefaults(a=1)
        s['b'] = [1, 2]
        c = s.copy()
        self.assertEqual(c, s)
        self.assertEqual(c['a'], 1)
        c['b'].append(3)
        self.assertEqual(c, s)
        self.assertIn(3, c['b'])
        self.assertIn(3, s['b'])
        c['a'] = 'a'
        self.assertNotEqual(c, s)

    def test_deepcopy(self):
        s = DictWithDefaults(a=1)
        s['b'] = [1, 2]
        d = s.copy(deep=True)
        d['b'].append(4)
        self.assertIn(4, d['b'])
        self.assertNotIn(4, s['b'])

    def test_update(self):
        s = DictWithDefaults(a=1, c=3)
        p = DictWithDefaults(a=2, d=4)
        s.setdefaults(b=2, d=5)
        p.setdefaults(b=3, c=6, e=6)
        s.update(p)
        self.assertEqual(s['a'], 2)
        self.assertEqual(s['c'], 3)
        self.assertEqual(s['d'], 4)
        self.assertEqual(s['b'], 3)
        self.assertEqual(s['e'], 6)


if __name__ == '__main__':
    unittest.main()
