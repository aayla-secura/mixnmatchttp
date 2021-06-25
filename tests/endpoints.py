import unittest
import re
from copy import copy

import loggers
from mixnmatchttp.endpoints import Endpoint, ParsedEndpoint, \
    ARGS_REQUIRED, ARGS_ANY, ARGS_OPTIONAL
from mixnmatchttp.endpoints.exc import EndpointError, \
    MethodNotAllowedError, ExtraArgsError, MissingArgsError, NotAnEndpointError
from mixnmatchttp.types import DefaultAttrs

class Test(unittest.TestCase):
    def _test_settings(self, parse=False):
        e = Endpoint(
            child={
                'grandchildA': {
                    'foo': {},
                    '*': {},
                },
                'grandchildB': {
                    '*': {'$varname': 'var'},
                    '$disabled': True,
                },
                '$allowed_methods': {'GET', 'POST'},
            },
            raw={
                '$raw_args': True,
            },
            **{'$disabled': False}
        )
        if parse:
            e = ParsedEndpoint(
                e, None, None, None, None, None, None)

        self.assertEqual(e.disabled, False)
        self.assertEqual(e.raw_args, False)
        self.assertIn('child', e)
        self.assertIn('grandchildA', e['child'])
        self.assertIn('grandchildB', e['child'])
        self.assertEqual(e['child']['grandchildA'].disabled, False)
        self.assertEqual(e['child']['grandchildB'].disabled, True)
        self.assertEqual(e['child']['grandchildA']['*'].varname,
                         'grandchildA')
        self.assertEqual(e['child']['grandchildB']['*'].varname,
                         'var')
        self.assertEqual(e['raw'].nargs, ARGS_ANY)

    def test_settings(self):
        self._test_settings()

    def test_settings_parsed(self):
        self._test_settings(True)

    def test_copy(self):
        e = Endpoint(
            foo={
                '$raw_args': True,
            })
        c = copy(e)
        self.assertIs(e.parent, c.parent)
        self.assertEqual(e._settings, c._settings)
        self.assertIsNot(e._settings, c._settings)
        self.assertNotEqual(e._id, c._id)

    def test_checks(self):
        self.assertRaises(EndpointError, Endpoint, dict(
            child={
                'child': {},
                '$raw_args': True,
            }))

    def test_parse_nargs(self):
        h = DefaultAttrs(
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            one={
                '$nargs': 1,
            },
            any={
                '$nargs': ARGS_ANY,
            },
            req={
                '$nargs': ARGS_REQUIRED,
            },
            opt={
                '$nargs': ARGS_OPTIONAL,
            },
        )

        h.raw_pathname = '/one'
        self.assertRaises(MissingArgsError, e.parse, h)
        h.raw_pathname = '/one/foo'
        e.parse(h)
        h.raw_pathname = '/one/foo/bar'
        self.assertRaises(ExtraArgsError, e.parse, h)

        h.raw_pathname = '/any'
        e.parse(h)
        h.raw_pathname = '/any/foo'
        e.parse(h)
        h.raw_pathname = '/any/foo/bar'
        e.parse(h)

        h.raw_pathname = '/req'
        self.assertRaises(MissingArgsError, e.parse, h)
        h.raw_pathname = '/req/foo'
        e.parse(h)
        h.raw_pathname = '/req/foo/bar'
        e.parse(h)

        h.raw_pathname = '/opt'
        e.parse(h)
        h.raw_pathname = '/opt/foo'
        e.parse(h)
        h.raw_pathname = '/opt/foo/bar'
        self.assertRaises(ExtraArgsError, e.parse, h)

        h.raw_pathname = '/'
        self.assertRaises(NotAnEndpointError, e.parse, h)
        h.raw_pathname = '/bar'
        self.assertRaises(NotAnEndpointError, e.parse, h)

    def test_parse_allowed_methods_a(self):
        path = '/foo'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='POST',
        )
        e = Endpoint(foo={})
        self.assertRaises(MethodNotAllowedError, e.parse, h)

    def test_parse_allowed_methods_b(self):
        path = '/foo'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo={
                '$allowed_methods': {'POST'},
            })
        self.assertRaises(MethodNotAllowedError, e.parse, h)

    def test_parse_raw_args(self):
        path = '/foo/bar/http/baz/bla'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo={
                '$raw_args': True,
            })
        ep = e.parse(h)
        self.assertEqual(ep.args, path[5:].split('/'))

    def test_parse_path_root(self):
        path = '/'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo={},
            **{'$disabled': False},
        )
        ep = e.parse(h)
        self.assertEqual(ep.root, '/')
        self.assertEqual(ep.sub, '')

    def test_parse_path_double_slash_a(self):
        path = '///foo//bar/'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            do_foo=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo=dict(bar={}),
        )
        ep = e.parse(h)
        self.assertEqual(ep.root, '/foo')
        self.assertEqual(ep.sub, 'bar')

    def test_parse_path_traverse_a(self):
        path = '/foo/../bar/'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            do_bar=lambda x: None,
            command='GET',
        )
        e = Endpoint(bar={})
        ep = e.parse(h)
        self.assertEqual(ep.root, '/bar')
        self.assertEqual(ep.sub, '')
        self.assertEqual(ep.args, [])

    def test_parse_path_traverse_b(self):
        path = '/foo/../bar/'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            do_foo=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo={
                '$raw_args': True,
            },
            bar={},
        )
        ep = e.parse(h)
        self.assertEqual(ep.root, '/foo')
        self.assertEqual(ep.sub, '')
        self.assertEqual(ep.args, ['..', 'bar', ''])

    def test_parse_path_double_slash_b(self):
        path = '///foo//bar/'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            do_foo=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo={
                '$raw_args': True,
            },
        )
        ep = e.parse(h)
        self.assertEqual(ep.root, '/foo')
        self.assertEqual(ep.sub, '')
        self.assertEqual(ep.args, ['', 'bar', ''])

    def test_parse_prefix(self):
        path = '/api/foo'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix='/api'),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(foo={})
        ep = e.parse(h)
        self.assertEqual(ep.root, '/')
        self.assertEqual(ep.sub, 'foo')

    def test_parse_varname(self):
        path = '/user/john/docs/2/view'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            user={
                '*': dict(
                    docs={
                        '*': {
                            '$varname': 'docID',
                            '$nargs': ARGS_OPTIONAL,
                        }})})
        ep = e.parse(h)
        self.assertEqual(ep.params, dict(user='john', docID='2'))
        self.assertEqual(ep.args, ['view'])

    def test_parse_handler_select(self):
        def hndef():
            pass

        def hna():
            pass

        def hnb():
            pass

        def hnc():
            pass

        path = '/user/john/docs/2/view'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=hndef,
            command='POST',
        )
        e = Endpoint(
            user={
                '*': dict(
                    docs={
                        '*': {
                            '$varname': 'docID',
                            '$allowed_methods': 'POST',
                            '$nargs': ARGS_OPTIONAL,
                        }})})

        h.do_user = hna
        ep = e.parse(h)
        self.assertEqual(ep.root, '/user')
        self.assertEqual(ep.sub, 'docs')
        self.assertEqual(ep.handler.__name__, hna.__name__)
        self.assertIs(ep.handler, hna)

        h.do_user_docs = hnb
        ep = e.parse(h)
        self.assertEqual(ep.handler.__name__, hnb.__name__)
        self.assertIs(ep.handler, hnb)

        h.do_POST_user_docs = hnc
        ep = e.parse(h)
        self.assertEqual(ep.handler.__name__, hnc.__name__)
        self.assertIs(ep.handler, hnc)


if __name__ == '__main__':
    unittest.main()
