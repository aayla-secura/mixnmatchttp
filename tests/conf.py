import unittest
import re

import loggers
from mixnmatchttp.handlers.conf import Conf, ConfItem, \
    ConfError, ConfRuntimeError, ConfTypeError

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

    def test_settings_defaults(self):
        i = ConfItem(1)
        self.assertEqual(i._self_settings.mergeable, False)
        self.assertEqual(i._self_settings.allowed_types, (int,))
        i = ConfItem(1, allowed_types=(int, float))
        self.assertEqual(i._self_settings.allowed_types,
                         (int, float))

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

    def test_merge_list(self):
        lista = [1, 2]
        listb = [1, 3]
        i = ConfItem(lista)
        i._ConfItem__update(listb)
        self.assertEqual(i, listb)
        i = ConfItem(lista, mergeable=True)
        i._ConfItem__update(listb)
        self.assertEqual(i, lista + listb)

    def test_merge_dict(self):
        dica = {'a': 1}
        dicb = {'b': 1}
        dicu = dica.copy()
        dicu.update(dicb)
        i = ConfItem(dica)
        i._ConfItem__update(dicb)
        self.assertEqual(i, dicb)
        i = ConfItem(dica, mergeable=True)
        i._ConfItem__update(dicb)
        self.assertEqual(i, dicu)


if __name__ == '__main__':
    unittest.main()
