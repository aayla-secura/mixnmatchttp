from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import unittest
import _thread
from wrapt import decorator
import re

from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
    AuthHTTPRequestHandler, CachingHTTPRequestHandler, \
    ProxyingHTTPRequestHandler, methodhandler
from mixnmatchttp import endpoints
from mixnmatchttp.utils import DictNoClobber
from mixnmatchttp.servers import ThreadingHTTPServer
from http.server import HTTPServer

@decorator
def endpoint_debug_handler(handler, self, args, kwargs):
    ep = args[0]
    handler(ep)
    page = self.page_from_template(self.templates['testtemplate'],
                                   {'handler': handler.__name__,
                                    'root': ep.root,
                                    'sub': ep.sub,
                                    'args': ep.args})
    self.render(page)

class TestHTTPRequestHandler(AuthHTTPRequestHandler,
                             CachingHTTPRequestHandler,
                             ProxyingHTTPRequestHandler):

    _secrets = ('secret', '/topsecret')
    _userfile = 'test_users.txt'
    _min_pwdlen = 3
    _endpoints = DictNoClobber(  # should convert to Endpoint
        dummylogin={},
        modtest={},
        login={
            '$allowed_methods': {'POST'},
            'test_sub': {},
        },
        test={
            # passing an Endpoint instance shouldn't matter
            'post_one': endpoints.Endpoint({
                '$nargs': 1,
                '$allowed_methods': {'POST'},
            }),
            'get_opt': {
                '$nargs': endpoints.ARGS_OPTIONAL,
            },
            'get_req': {
                '$nargs': endpoints.ARGS_REQUIRED,
            },
            'get_any': {
                '$nargs': endpoints.ARGS_ANY,
            },
        },
        deep={
            '1': {
                '2': endpoints.Endpoint({
                    '3': endpoints.Endpoint(),
                    '4': {},
                }),
            },
        },
        template={
            '$allowed_methods': {'GET', 'POST'},
            '$nargs': 1,
        }
    )
    _template_pages = DictNoClobber(
        testpage={
            'data': '$BODY',
            'type': 'text/plain'
        },
    )
    _templates = DictNoClobber(
        testtemplate={
            'fields': {
                'BODY': 'This is $handler for $root @ $sub ($args)',
            },
            'page': 'testpage'
        },
        testtemplate_wrongpage={
            'fields': {
                'BODY': 'This tries to use page "foobar"',
            },
            'page': 'foobar'  # non-existent page
        },
        testtemplate_nopage={
            'fields': {
                'BODY': 'This uses the default template page',
            },
            # missing page
        },
    )

    def do_dummylogin(self, ep):
        self.set_cookie()
        self.send_response_goto()

    @endpoint_debug_handler
    def do_modtest(self, ep):
        # modify endpoint, should affect only current request
        self.endpoints['test'] = {}
        self.endpoints['test'].args = 1
        # set a header just for this request
        self.headers_to_send['X-Mod'] = 'Test'
        self.do_GET.__wrapped__()

    @endpoint_debug_handler
    def do_default(self, ep):
        pass

    @endpoint_debug_handler
    def do_deep(self, ep):
        pass

    @endpoint_debug_handler
    def do_deep_1_2_4(self, ep):
        pass

    @endpoint_debug_handler
    def do_deep_1_2_3_4(self, ep):
        # this one should never be called
        raise NotImplementedError

    def denied(self):
        '''Deny access to /forbidden'''
        if re.match('^/forbidden(/|$)', self.pathname):
            # return args are passed to
            # BaseHTTPRequestHandler.send_error in that order; both
            # messages are optional
            return (403, None, 'Access denied')
        return super().denied()

    def no_cache(self):
        '''Only allow caching of scripts'''

        return (
            not self.pathname.endswith('.js')) or super().no_cache()

    @methodhandler
    def do_GET(self):
        page = self.page_from_template(
            self.templates['testtemplate'], {'handler': 'do_GET'})
        self.render(page)

    def send_custom_headers(self):
        self.send_header('X-Foo', 'Foo')

class Requester(object):
    def __init__(self):
        pass

    def do(self, path,
            method='GET',
            match={},
            nomatch={},
            headers={},
            readonly=True):
        pass


class TestBaseMeta(unittest.TestCase):
    def test_endpoint_conversion(self):
        self.assertIsInstance(
            TestHTTPRequestHandler._endpoints,
            endpoints.Endpoint,
            msg=('BaseMeta failed to convert _endpoints to the '
                 'appropriate class'))

    def test_template_conversion(self):
        self.assertIsInstance(
            TestHTTPRequestHandler._template_pages,
            DictNoClobber,
            msg=('BaseMeta failed to convert _template_pages '
                 'to the appropriate class'))

    def test_endpoint_inheritance(self):
        self.assertIn('logout',
                      TestHTTPRequestHandler._endpoints.keys(),
                      msg=("BaseMeta failed to include "
                           "parent's endpoints"))

    def test_endpoint_inheritance_existing(self):
        self.assertIn('test_sub',
                      TestHTTPRequestHandler._endpoints[
                          'login'].keys(),
                      msg=("BaseMeta overwrote current class "
                           "endpoint with parent's endpoint"))

    def test_template_inheritance(self):
        self.assertIn('default',
                      TestHTTPRequestHandler._template_pages.keys(),
                      msg=("BaseMeta failed to include "
                           "parent's template pages"))
        # no need to test overwriting for templates as well

class TestEndpoints(unittest.TestCase):
    #  def test_max_level(self):
    #      old_max_level = endpoints.Endpoint._max_level
    #      endpoints.Endpoint._max_level = 2
    #      with self.assertRaises(endpoints.EndpointTooDeepError):
    #          endpoints.Endpoint(a={'b':{'c'}})
    #      with self.assertRaises(endpoints.EndpointTooDeepError):
    #          endpoints.Endpoint(a={'b':Endpoint(c={})})
    #      with self.assertRaises(endpoints.EndpointTooDeepError):
    #          e = endpoints.Endpoint(a={'b':{}})
    #          e['a']['b']['c'] = {}
    #      endpoints.Endpoint._max_level = old_max_level
    def setUp(self):
        self.ep = endpoints.Endpoint(a={})
        self.epA = endpoints.Endpoint(
            {
                '$disabled': False,
                '$allowed_methods': {'POST'},
            },
            a={
                '$allowed_methods': {'POST'},
                '$nargs': 1,
                'suba': {},
                'subb': {'$nargs': 2},
            })

        self.epB = endpoints.Endpoint(
            {
                '$disabled': True,
                '$nargs': 1,
            },
            a={
                '$nargs': 5,
                'subb': {'$nargs': 3},
            })

    def tearDown(self):
        self.ep.clear()
        self.epA.clear()
        self.epB.clear()

    def test_raw_ep_cant_have_children(self):
        with self.assertRaises(endpoints.EndpointError):
            endpoints.Endpoint(a={'$raw_args': True, 'sub': {}})

    def test_disabled_default_root(self):
        self.assertTrue(self.ep.disabled)

    def test_disabled_default_child(self):
        self.assertFalse(self.ep['a'].disabled)

    def test_disabled_default_root_as_child_default(self):
        ep = endpoints.Endpoint(r=self.ep)
        self.assertFalse(ep['r'].disabled)

    def test_disabled_default_root_as_child(self):
        ep = endpoints.Endpoint(r=self.epB)
        self.assertTrue(ep['r'].disabled)

    def test_equality(self):
        ep = endpoints.Endpoint(a={})
        self.assertEqual(ep, self.ep)

    def test_equality_diff_arg(self):
        ep = endpoints.Endpoint(a={})
        ep.disabled = False
        self.assertNotEqual(ep, self.ep)

    def test_equality_explicit_default_arg(self):
        ep = endpoints.Endpoint(a={})
        ep.disabled = True
        self.assertEqual(ep, self.ep)

    def test_init_from_endpoint(self):
        ep = endpoints.Endpoint(self.epA)
        self.assertFalse(ep.disabled)
        self.assertEqual(ep.allowed_methods, {'POST'})

    def test_copy(self):
        ep = self.epA.copy()
        self.assertEqual(ep, self.epA)
        self.assertEqual(ep['a'].nargs, 1)
        self.assertFalse(ep.disabled)

    def test_update_noclob(self):
        self.epA.update_noclob(self.epB)
        self.assertFalse(self.epA.disabled)
        self.assertEqual(self.epA.nargs, 1)
        self.assertEqual(self.epA.allowed_methods, {'POST'})
        self.assertEqual(self.epA['a'].allowed_methods, {'POST'})
        self.assertEqual(self.epA['a'].nargs, 1)
        self.assertIn('suba', self.epA['a'].keys())
        self.assertEqual(self.epA['a']['subb'].nargs, 2)

    def test_update_noclob_from_args_default(self):
        self.epA.update_noclob({'$nargs': 1})
        self.assertEqual(self.epA.nargs, 1)

    def test_update_noclob_from_args(self):
        self.epB.update_noclob({'$nargs': 3})
        self.assertEqual(self.epB.nargs, 1)

    def test_update_noclob_from_kwargs(self):
        self.epA.update_noclob(a={'$nargs': 5})
        self.assertEqual(self.epA['a'].nargs, 1)
        self.assertIn('suba', self.epA['a'].keys())

    def test_update_noclob_from_args_and_kwargs(self):
        self.epA.update_noclob({'$nargs': 1}, a={'$nargs': 5})
        self.assertEqual(self.epA.nargs, 1)
        self.assertEqual(self.epA['a'].nargs, 1)
        self.assertIn('suba', self.epA['a'].keys())

    def test_update(self):
        self.epA.update(self.epB)
        self.assertTrue(self.epA.disabled)
        self.assertEqual(self.epA.nargs, 1)
        self.assertEqual(self.epA.allowed_methods, {'POST'})
        self.assertEqual(self.epA['a'].allowed_methods,
                         self.epB['a'].allowed_methods)
        self.assertEqual(self.epA['a'].nargs, 5)
        self.assertNotIn('suba', self.epA['a'].keys())
        self.assertEqual(self.epA['a']['subb'].nargs, 3)

    def test_update_from_args_default(self):
        self.epA.update({'$nargs': 1})
        self.assertEqual(self.epA.nargs, 1)

    def test_update_from_args(self):
        self.epB.update({'$nargs': 3})
        self.assertEqual(self.epB.nargs, 3)

    def test_update_from_kwargs(self):
        self.epA.update(a={'$nargs': 5})
        self.assertEqual(self.epA['a'].nargs, 5)
        self.assertNotIn('suba', self.epA['a'].keys())

    def test_update_from_args_and_kwargs(self):
        self.epA.update({'$nargs': 1}, a={'$nargs': 5})
        self.assertEqual(self.epA.nargs, 1)
        self.assertEqual(self.epA['a'].nargs, 5)
        self.assertNotIn('suba', self.epA['a'].keys())

class TestReq(unittest.TestCase):
    '''Base class for tests which submit requests'''

    def setUp(self):
        self.requester = Requester()

    def tearDownClass(self):
        pass

class TestTemplates(TestReq):
    # Pass extra dynfields, missing dynfields, check Content-Type
    pass

class TestAuth(TestReq):
    # check that Secure is set on cookies over SSL TODO
    pass

class TestProxy(TestReq):
    pass

class TestMisc(TestReq):
    pass

############################################################


address = '127.0.0.1'
port = 58080
httpd = HTTPServer((address, port), TestHTTPRequestHandler)
def setUpModule():
    _thread.start_new_thread(httpd.serve_forever, ())

def tearDownModule():
    httpd.shutdown()


if __name__ == '__main__':
    unittest.main(verbosity=2)
