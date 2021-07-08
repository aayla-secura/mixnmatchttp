import unittest

import loggers
from mixnmatchttp.templates import TemplateContainer

class Test(unittest.TestCase):
    def test_err(self):
        self.assertRaises(TypeError, TemplateContainer,
                          t=dict(mimetype='text/plain'))
        self.assertRaises(TypeError, TemplateContainer,
                          t=dict(data='text/plain'))
        self.assertRaises(TypeError, TemplateContainer, t={})
        self.assertRaises(ValueError, TemplateContainer, t=None)

    def test(self):
        tcont = TemplateContainer(
            t=dict(
                mimetype='text/plain', data='> $foo $bar <'),
            f='templates')
        t = tcont['t']
        self.assertEqual(str(t.substitute(foo='bar')), '> bar $bar <')
        self.assertEqual(str(t.substitute_all(foo='bar')), '> bar  <')
        self.assertEqual(
            t.substitute(foo='bar').encode().data, b'> bar $bar <')
        f = tcont['f']['foo.html']
        self.assertEqual(str(f)[:9], '<!DOCTYPE')
        self.assertIn('FOO', str(f.substitute_all(body='FOO')))
        self.assertIn('${title}', str(f.substitute(body='FOO')))
        self.assertNotIn('${title}', str(f.substitute_all(body='FOO')))
        self.assertEqual(f.mimetype, 'text/html')


if __name__ == '__main__':
    unittest.main()
