import unittest
import re
from copy import copy

import loggers
from mixnmatchttp.utils import is_mergeable
from mixnmatchttp.conf import Conf, ConfItem
from mixnmatchttp.conf.exc import ConfError, ConfRuntimeError, \
    ConfTypeError, ConfValueError

class ConfItemB(ConfItem):
    pass

class TestConfItem(unittest.TestCase):
    def test_proxy(self):
        x = [1, 2, 3]
        i = ConfItem(x.copy())
        self.assertEqual(i, x)
        i.append(4)
        self.assertNotEqual(i, x)
        i = ConfItem(x)
        i.append(4)
        self.assertEqual(i, x)
        self.assertIn(4, x)

    def test_copy(self):
        i = ConfItemB(1)
        c = copy(i)
        self.assertIs(type(c), ConfItemB)

    def test_settings_defaults(self):
        i = ConfItem(1)
        self.assertEqual(i._self_settings.mergeable, False)
        self.assertEqual(i._self_settings.allowed_types, (int,))
        i = ConfItem(1, allowed_types=(int, float))
        self.assertEqual(i._self_settings.allowed_types,
                         (int, float))

    def test_value_check(self):
        self.assertRaises(ConfValueError, ConfItem,
                          'x', allowed_values=['a', 'b'])

    def test_type_conv(self):
        self.assertRaises(ConfTypeError, ConfItem,
                          'x', allowed_types=(int,))
        self.assertRaises(ConfTypeError, ConfItem,
                          None, allowed_types=(int,))
        i = ConfItem(1.5, allowed_types=(int,))
        self.assertEqual(i, 1)
        i = ConfItem(1, allowed_types=(str,))
        self.assertEqual(i, "1")

    def test_transform(self):
        i = ConfItem('foo/bar/', transformer=lambda x: x.replace(
            '/', '_'))
        self.assertEqual(i, 'foo_bar_')

    def test_module_check(self):
        self.assertRaises(ConfRuntimeError, ConfItem,
                          'x', requires='nonexistent')
        ConfItem('x', requires=('future',))

    def test_merge_a(self):
        ci = ConfItem([1, 2])
        cim = ConfItem([1, 2], mergeable=True)
        self.assertFalse(is_mergeable(ci, inplace=True))
        self.assertTrue(is_mergeable(cim, inplace=True))

    def test_merge_b(self):
        ci = ConfItem(1)
        cim = ConfItem(1, mergeable=True)
        self.assertFalse(is_mergeable(ci, inplace=True))
        self.assertTrue(is_mergeable(cim, inplace=True))

    def test_merge_list(self):
        lista = [1, 2]
        listb = [1, 3]
        i = ConfItem(lista)
        i.__merge__(listb)
        self.assertEqual(i, listb)
        i = ConfItem(lista, mergeable=True)
        i.__merge__(listb)
        self.assertEqual(i, lista + listb)

    def test_merge_dict(self):
        dica = {'a': 1}
        dicb = {'b': 1}
        dicu = dica.copy()
        dicu.update(dicb)
        i = ConfItem(dica)
        i.__merge__(dicb)
        self.assertEqual(i, dicb)
        i = ConfItem(dica, mergeable=True)
        i.__merge__(dicb)
        self.assertEqual(i, dicu)

class TestConf(unittest.TestCase):
    def test_update_merge_a(self):
        lista = [1, 2]
        listb = [1, 3]
        c = Conf(a=ConfItem(lista.copy(), mergeable=True),
                 b=listb.copy())
        c.update(a=listb, b=listb, c=2)
        self.assertEqual(c.a, lista + listb)
        self.assertEqual(c.b, listb)
        self.assertEqual(c.c, 2)

    def test_update_merge_b(self):
        c = Conf(a=1)
        c.update(a=2)
        self.assertEqual(c.a, 2)

    def test_add_merge(self):
        lista = [1, 2]
        listb = [1, 3]
        c = Conf(a=ConfItem(lista.copy(), mergeable=True),
                 b=listb.copy())
        c.a += listb
        c.b += lista
        # unexpected but logical and inevitable consequence of
        # mergeable is that += doubles the item
        self.assertEqual(c.a, lista + listb + lista + listb)
        self.assertEqual(c.b, listb + lista)


if __name__ == '__main__':
    unittest.main()
