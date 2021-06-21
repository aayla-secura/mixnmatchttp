import unittest
import re

import loggers
from mixnmatchttp.conf import Conf, ConfItem

class Test(unittest.TestCase):

    def test_inherit(self):
        c = Conf(
            i=ConfItem(1, allowed_types=(int, float)),
        )
        self.assertEqual(c.i, 1)
        self.assertIn('allowed_types', c.i._self_settings)
        self.assertNotIn('can_be_merged', c.i._self_settings)
        self.assertEqual(c.i._self_settings['can_be_merged'], False)
        c.i = 2
        self.assertEqual(c.i, 2)
        self.assertEqual(c.i._self_settings['allowed_types'], (int, float))
        c.i = ConfItem(3)
        self.assertEqual(c.i._self_settings['allowed_types'], (int, float))
        self.assertEqual(c.i, 3)

    def test_merge(self):
        c = Conf(
            d=ConfItem([1, 2]),
            y=ConfItem([1, 2], can_be_merged=True),
            n=ConfItem([1, 2], can_be_merged=False)
        )
        c.d = [3]
        c.y = [3]
        c.n = [3]
        self.assertListEqual(c.d, [3])
        self.assertListEqual(c.y, [1, 2, 3])
        self.assertListEqual(c.n, [3])

    def test_type(self):
        item = ConfItem([('a', 2)], allowed_types=(dict,))
        self.assertDictEqual(item, {'a': 2})
        self.assertRaises(TypeError, ConfItem, 1, allowed_types=(dict,))

    def test_modules(self):
        item = ConfItem(1, required_modules=['collections'])
        self.assertRaises(RuntimeError, ConfItem, 1, required_modules=['x'])


if __name__ == '__main__':
    unittest.main()
