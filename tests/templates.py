import unittest

import loggers
from mixnmatchttp.templates import Templates
from mixnmatchttp.templates.exc import TemplateError

class Test(unittest.TestCase):
    def test_err(self):
        self.assertRaises(TemplateError, Templates,
                          t=dict(type='text/plain'))
        self.assertRaises(TemplateError, Templates,
                          t=dict(data='text/plain'))
        self.assertRaises(TemplateError, Templates, t={})
        self.assertRaises(TemplateError, Templates, t=None)

    def test(self):
        tcont = Templates(t=dict(
            type='text/plain', data='> $foo $bar <'))
        t = tcont['t']
        self.assertEqual(str(t.substitute(foo='bar')), '> bar  <')


if __name__ == '__main__':
    unittest.main()
