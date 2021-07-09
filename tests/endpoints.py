import unittest
import re
from copy import copy, deepcopy

import loggers
from mixnmatchttp.endpoints import Endpoint, ParsedEndpoint, \
    EndpointArgs, ARGS_REQUIRED, ARGS_ANY, ARGS_OPTIONAL
from mixnmatchttp.endpoints.exc import EndpointError, \
    MethodNotAllowedError, ExtraArgsError, MissingArgsError, NotAnEndpointError
from mixnmatchttp.containers import DefaultAttrs

class CSEndpoint(Endpoint):
    case_sensitive = True

class Test(unittest.TestCase):
    def _test_settings(self, parse=False):
        e = Endpoint(
            child={
                'grandchildA': {
                    'foo': {},
                    '*': {},
                    #  '$allow': ['GET'],
                },
                'grandchildB': {
                    '*': {'$varname': 'var'},
                    '$disabled': True,
                },
                '$allow': {'GET', 'POST'},
            },
            raw={
                '$raw_args': True,
            },
            foo={
                #  '$allow': ['POST'],
            },
            **{'$disabled': False}
        )
        if parse:
            e = ParsedEndpoint(
                e, None, None, None, None, [], None)

        self.assertEqual(e.disabled, False)
        self.assertEqual(e.raw_args, False)
        self.assertIn('child', e)
        self.assertIn('grandchildA', e['child'])
        self.assertIn('grandchildB', e['child'])
        self.assertEqual(e['child']['grandchildA'].disabled, False)
        self.assertEqual(e['child']['grandchildA'].allow,
                         {'GET', 'HEAD'})
        self.assertEqual(e['child']['grandchildB'].disabled, True)
        self.assertEqual(e['child']['grandchildA']['*'].varname,
                         'grandchildA')
        self.assertEqual(e['child']['grandchildB']['*'].varname,
                         'var')
        #  self.assertEqual(e['foo'].allow, {'POST'})
        self.assertEqual(e['raw'].nargs, ARGS_ANY)

    def test_settings(self):
        self._test_settings()

    def test_settings_parsed(self):
        self._test_settings(True)

    def test_copy_a(self):
        e = Endpoint(
            foo={
                '$raw_args': True,
            })
        c = copy(e)
        self.assertEqual(e, c)
        self.assertEqual(e._settings, c._settings)
        self.assertIsNot(e._settings, c._settings)
        self.assertNotEqual(e._id, c._id)

    def test_copy_b(self):
        e = Endpoint(
            foo=Endpoint(
                bar={}
            ))
        c = copy(e)
        self.assertIs(e['foo'], c['foo'])
        self.assertIs(e['foo'].parent, e)

    def test_deepcopy(self):
        e = Endpoint(
            foo=Endpoint(
                bar={}
            ))
        c = deepcopy(e)
        self.assertIsNot(e['foo'], c['foo'])
        self.assertIs(e['foo'].parent, e)
        self.assertIs(c['foo'].parent, c)

    def test_checks(self):
        self.assertRaises(EndpointError, Endpoint, dict(
            child={
                'child': {},
                '$raw_args': True,
            }))

    def test_get_from_path(self):
        e = Endpoint(foo=dict(bar={}))
        self.assertIs(e.get_from_path('/foo/bar'), e['foo']['bar'])
        self.assertIs(e.get_from_path('/foo'), e['foo'])

    def test_case_insensitive(self):
        e = Endpoint(foo=dict(Bar={}))
        self.assertIs(e.get_from_path('/foo/bar'), e['foo']['bar'])
        self.assertIs(e.get_from_path('/FOo'), e['foo'])

    def test_case_sensitive(self):
        h = DefaultAttrs(
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = CSEndpoint(Foo=dict(bar={}))
        self.assertIn('Foo', e)
        self.assertNotIn('foo', e)
        self.assertIn('bar', e['Foo'])

        h.raw_pathname = '/foo'
        self.assertRaises(NotAnEndpointError, e.parse, h)
        h.raw_pathname = '/Foo'
        e.parse(h)

        h.raw_pathname = '/Foo/bar'
        e.parse(h)

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

    def test_parse_allow_a(self):
        path = '/foo'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='POST',
        )
        e = Endpoint(foo={})
        self.assertRaises(MethodNotAllowedError, e.parse, h)

    def test_parse_allow_b(self):
        path = '/foo'
        h = DefaultAttrs(
            raw_pathname=path,
            conf=DefaultAttrs(api_prefix=''),
            do_default=lambda x: None,
            command='GET',
        )
        e = Endpoint(
            foo={
                '$allow': {'POST'},
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
                            '$allow': 'POST',
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

    def test_args(self):
        ARGS_ONE = EndpointArgs(1)
        ARGS_NONE = EndpointArgs(0)
        self.assertRaises(
            MissingArgsError, ARGS_REQUIRED.validate, [])
        self.assertRaises(
            MissingArgsError, ARGS_ONE.validate, [])
        self.assertRaises(
            ExtraArgsError, ARGS_ONE.validate, ['a', 'b'])
        self.assertRaises(
            ExtraArgsError, ARGS_NONE.validate, ['a'])
        self.assertRaises(
            ExtraArgsError, ARGS_OPTIONAL.validate, ['a', 'b'])
        ARGS_OPTIONAL.validate(['a'])
        ARGS_OPTIONAL.validate([])
        ARGS_REQUIRED.validate(['a'])
        ARGS_REQUIRED.validate(['a', 'b'])
        ARGS_ANY.validate([])
        ARGS_ANY.validate(['a', 'b'])
        ARGS_ONE.validate(['a'])
        ARGS_NONE.validate([])


if __name__ == '__main__':
    unittest.main()
