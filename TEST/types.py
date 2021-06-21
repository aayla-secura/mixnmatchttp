import unittest
import re

import loggers
from mixnmatchttp.types import Settings

class Test(unittest.TestCase):

    def test_inherit(self):
        s = Settings(a=1)
        s['_a'] = 1
        s.setdefaults(b=2)
        s.setdefault('c', 3)
        self.assertEqual(s['a'], 1)
        self.assertEqual(s['b'], 2)
        self.assertEqual(s.get('c'), 3)
        self.assertRaises(KeyError, lambda k: s[k], 'd')
        self.assertIn('a', s)
        self.assertIn('_a', s)
        self.assertNotIn('b', s)


if __name__ == '__main__':
    unittest.main()
