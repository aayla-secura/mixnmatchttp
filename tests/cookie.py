import unittest
import re
from copy import copy

import loggers
from mixnmatchttp.cookie import Cookie

class Test(unittest.TestCase):
    def test_invalid_flags(self):
        self.assertRaises(ValueError, Cookie, '')
        self.assertRaises(ValueError, Cookie, 'Foo', foo='/foo')
        self.assertRaises(ValueError, Cookie, 'Foo', **{'max-age': 'x'})
        self.assertRaises(ValueError, Cookie, 'Foo', expires='x')

    def test_bool_flags(self):
        c = Cookie('Foo', 'bar', path='/foo', secure=True,
                   httponly=False)
        self.assertEqual(str(c), 'Foo=bar; Path=/foo; Secure')

    def test_expires(self):
        c = Cookie('Foo', 'bar', Expires=0)
        self.assertEqual(
            str(c), 'Foo=bar; Expires=Thu, 01 Jan 1970 00:00:00 UTC')
        c.expires = None
        self.assertEqual(str(c), 'Foo=bar')


if __name__ == '__main__':
    unittest.main()
