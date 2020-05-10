# Overview

`mixnmatchttp` is a modular HTTP/S server based on [Python's http
server](https://docs.python.org/3/library/http.server.html) that lets you "mix
'n' match" various functionalities. It defines several request handlers, which
are wrappers around `http.server.SimpleHTTPRequestHandler`, as well as
a `ThreadingHTTPServer` which can be used in place of Python's
`http.server.HTTPServer` for multi-threading support.

# Quick start

Request handlers define special endpoints and/or templates as class attributes.

Endpoints are the RESTful API of the server. A request which does not map to an
endpoint is treated as a request for a file or directory (Python's http server
handles it, unless your class overrides the `do_(GET|POST|...)` methods).
A request which does map to an endpoint will call an endpoint handler: a method
of your class by the name `do_[{HTTP method}]_{underscope-separated path}`
with "path" being the most-specific (longest) path for which a method is
defined and the HTTP method part being optional. Handlers are looked from
most specific to less specific. E.g. a GET to `/foo/bar/baz` will look for
`do_GET_foo_bar_baz`, then `do_foo_bar_baz`, then `do_GET_foo_bar`, then
`do_foo_bar`, then `do_GET_FOO`, then `do_foo`, and finally `do_default`.
`do_default` is defined in `BaseHTTPRequestHandler` but your class may want
to override it.

Endpoints can also be variable, or parametrized, e.g. `/person/{name}/age`,
where `{name}` can be anything. This maps to a handler `do_person_age`.

Template pages are parametrized response bodies. Templates specify a template
page to be used with and give a dictionary of parameters and values to use with
the template. Each parameter value may also contain dynamic parameters, which
are given to the `BaseHTTPRequestHandler.page_from_template` method, which
constructs the final page.

You can inherit from one or more of the `*HTTPRequestHandlers`. Each parent's
endpoints/templates will be copied to, without overwriting, your child class'
endpoints/templates.

---

**Important notes:**

  * If you need to override any of the HTTP method handlers (e.g. `do_GET`),
    you must decorate them with `mixnmatchttp.handlers.base.methodhandler`, as
    shown in the demo below. And if you need to call any of the parent's HTTP
    method handlers you must call the original wrapped method using the
    `__wrapped__` attribute, as shown in the demo.

---

## Defining endpoints

Endpoints, templates and template pages constructors have the same signature as
for a dictionary. Endpoints are of type `mixnmatchttp.endpoints.Endpoint`,
while templates and template pages are of type
`mixnmatchttp.utils.DictNoClobber`. However, you can define them as
a dictionary, or any type which has a dictionary-like interface, and
`BaseHTTPRequestHandler`'s meta class will convert them to the appropriate
class.

For example you can define endpoints like so:

```python
class MyHandler(BaseHTTPRequestHandler):
    _endpoints = mixnmatchttp.endpoints.Endpoint(
            some_sub={
                '$allowed_methods': {'GET', 'POST'},
                '$nargs': 1,
                'some_sub_sub': {
                    '$nargs': endpoints.ARGS_ANY,
                    '$raw_args': True, # don't canonicalize rest of path
                    }
                },
            some_other_sub={})
```

or like so:

```python
class MyHandler(BaseHTTPRequestHandler):
    _endpoints = mixnmatchttp.endpoints.Endpoint({
            'some_sub': {
                '$allowed_methods': {'GET', 'POST'},
                '$nargs': 1,
                'some_sub_sub': {
                    '$nargs': endpoints.ARGS_ANY,
                    '$raw_args': True, # don't canonicalize rest of path
                    }
                },
            },
            some_other_sub={})
```

or like so:

```python
class MyHandler(BaseHTTPRequestHandler):
    _endpoints = {
            'some_sub': {
                '$allowed_methods': {'GET', 'POST'},
                '$nargs': 1,
                'some_sub_sub': {
                    '$nargs': endpoints.ARGS_ANY,
                    '$raw_args': True, # don't canonicalize rest of path
                    }
                },
            'some_other_sub': {}
            }
```


Any keyword arguments or dictionary keys starting with `$` correspond to an
attribute (without the `$`) which specifies how an endpoint can be called.
All other keyword arguments/keys become child endpoints of the parent; their
value should be another `Endpoint` (or any dictionary-like object).

Default endpoint attributes are:

```python
disabled=False|True            # specifies if the enpoint cannot be called directly;
                               # False for child endpoints but True for root endpoint
allowed_methods={'GET','HEAD'} # a set of allowed HTTP methods; HEAD is added to the
                               # set if 'GET' is present
nargs=0                        # how many slash-separated arguments the endpoint can take;
                               # can be a number of any of:
                               #   mixnmatchttp.endpoints.ARGS_OPTIONAL for 0 or 1
                               #   mixnmatchttp.endpoints.ARGS_ANY      for any number
                               #   mixnmatchttp.endpoints.ARGS_REQUIRED for 1 or more
                               # !!only reliable if raw_args is False!!
raw_args=False                 # whether arguments should not be canonicalized,
                               # e.g. /foo/..//bar/./baz will not be turned to /bar/baz
varname=None                   # the name of the parameter to record, default is parent
                               # endpoint's name; only valid for parametrized endpoints
```

Child endpoints are enabled by default, the root endpoint is disabled by
default; if you want it enabled, either manually change the `disabled`
attribute, or construct it like so:

```python
class MyHandler(BaseHTTPRequestHandler):
    _endpoints = {
        'some_sub': { ... },
        '$disabled': False, # a request for / will now call do_ or do_default
                            # instead of do_(GET|POST|...)
        }
```

## Handling parsed endpoints

When a path resolves to an endpoint, `ep`, the corresponding endpoint handler
(`do_???`) will be passed a single argument:
a `mixnmatchttp.endpoints.ParsedEndpoint` (inherits from
`mixnmatchttp.endpoints.Endpoint`) initialized from the original `ep` with the
following additional attributes:

  * `httpreq`: the instance of `BaseHTTPRequestHandler` for this request
  * `handler`: the `httpreq`'s method selected as a handler
  * `root`: longest path of the endpoint (with a leading `/`) corresponding to
    a defined handler, i.e.  if the path is `/foo/bar` and `do_foo` is
    selected, `root` will be `/foo`; if using `do_default`, `root` is empty (`''`).
  * `sub`: rest of the path of the endpoint without a leading `/`, e.g. `bar` or `foo/bar`
  * `args`: everything following the endpoint's path without a leading `/`
  * `argslen`: the number of arguments it was called with (length of array from `/` separated `args`)
  * `params`: a dictionary with parameters from endpoint mapped to the path

## Example: Implementing a server

Some methods that you may want to override, as well as implementing a custom
endpoint and template, are shown below for `MyHandler`:

```python
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import re
import ssl
import sys

from http.server import HTTPServer
from mixnmatchttp.servers import ThreadingHTTPServer
from mixnmatchttp import endpoints
from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
    methodhandler
from mixnmatchttp.utils import DictNoClobber

class MyHandler(BaseHTTPRequestHandler):
    _endpoints = endpoints.Endpoint(
        foobar={},  # will use do_default handler
        refreshme={
            '$nargs': endpoints.ARGS_OPTIONAL,
        },
        parameter={
            # this way /parameter will raise "missing arg"
            '$nargs': 1,
            # this way /parameter will be treated by the GET handler
            # '$disabled': True,
            '*': {
                '$nargs': 1,
                'special': {},  # will use do_parameter__special
            },
        },
        debug={
            # these are for when /debug is called
            '$allowed_methods': {'GET', 'POST'},
            'sub': {  # will use do_*debug handler
                # these are for when /debug/sub is called
                '$nargs': endpoints.ARGS_ANY,
                '$raw_args': True,  # don't canonicalize rest of path
            },
            '*': {
                'debug': {
                    '*': {
                        '$varname': 'debug2'
                    },
                },
            },
        },
    )
    _template_pages = DictNoClobber(
        simpletxt={
            'data': '$CONTENT',
            'type': 'text/html'
        },
        simplehtml={
            'data': '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8" />
    $HEAD
    <title>$TITLE</title>
    </head>
    <body>
    $BODY
    </body>
    </html>
            ''',
            'type': 'text/html'
        },
    )
    _templates = DictNoClobber(
        refresh={
            'fields': {
                'HEAD': ('<meta http-equiv="refresh" '
                         'content="${interval}">'),
                'TITLE': 'Example',
                'BODY': ('<h1>Example page, will refresh every '
                         '${interval}s.</h1>'),
            },
            'page': 'simplehtml',
        },
        debug={
            'fields': {
                'CONTENT': ('${info}You called endpoint $root, sub = '
                            '$sub, args = $args, params = $params'),
            },
            'page': 'simpletxt',
        },
    )

    def do_refreshme(self):
        interval = self.ep.args
        if not interval:
            interval = '30'

        '''Handler for the endpoint /refreshme'''
        page = self.page_from_template(self.templates['refresh'],
                                       {'interval': interval})
        self.render(page)

    def do_parameter(self):
        self.render({
            'data': (
                '{} = {}'.format(self.ep.params['parameter'],
                                 self.ep.args)
            ).encode('utf-8'),
            'type': 'text/plain'})

    def do_parameter_special(self):
        self.render({'data': b'A very special parameter!',
                     'type': 'text/plain'})

    def do_debug(self):
        '''Handler for non-POST to the endpoint /debug'''
        # set a header just for this request
        self.save_header('X-Debug', 'Foo')
        page = self.page_from_template(
            self.templates['debug'],
            {'info': '', 'root': self.ep.root, 'sub': self.ep.sub,
             'args': self.ep.args, 'params': self.ep.params})
        self.render(page)

    def do_POST_debug(self):
        '''Handler for POST to the endpoint /debug'''
        # set a header just for this request
        self.save_header('X-Debug', 'Foo')
        page = self.page_from_template(
            self.templates['debug'],
            {'info': 'POST! ',
             'root': self.ep.root, 'sub': self.ep.sub,
             'args': self.ep.args, 'params': self.ep.params})
        self.render(page)

    def do_default(self):
        '''Default endpoints handler'''
        page = self.page_from_template(
            self.templates['debug'],
            {'info': 'This is do_default. ',
             'root': self.ep.root, 'sub': self.ep.sub,
             'args': self.ep.args, 'params': self.ep.params})
        self.render(page)

    # Don't forget this decorator!
    @methodhandler
    def do_GET(self):
        # Do something here, then call parent's undecorated method
        super().do_GET.__wrapped__()

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

        return (not self.pathname.endswith('.js')) or super().no_cache()

    def send_custom_headers(self):
        '''Send our custom headers'''

        self.send_header('X-Foo', 'Foobar')


if __name__ == '__main__':
    use_SSL = False
    keyfile = ''  # path to PEM key, if use_SSL is True
    certfile = ''  # path to PEM certificate, if use_SSL is True
    srv_cls = HTTPServer
    # srv_cls = ThreadingHTTPServer # if using multi-threading
    address = '127.0.0.1'
    port = 58080

    httpd = srv_cls((address, port), MyHandler)
    if use_SSL:
        httpd.socket = ssl.wrap_socket(
            httpd.socket,
            keyfile=keyfile,
            certfile=certfile,
            server_side=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
```

  * A request for `/debug/sub/..//foo/../bar/./baz` will call `self.do_debug` with `ep`, a copy of `MyHandler._endpoints['debug']['sub']`. `ep.root` will be "debug", `ep.sub` will be "sub", `ep.args` will be "..//foo/../bar/./baz". `self.command` will give the HTTP method.
  * A request for `/debug/foo/../bar` will canonicalize the path to `/debug/bar` (since `raw_args` for `/debug` is `False`) call `do_debug` with `ep`, a copy of `MyHandler._endpoints['debug']`. `ep.root` will be "debug", `ep.sub` will be "", `ep.args` will be "bar".
  * A request for `/debug/../bar` will raise `mixnmatchttp.endpoints.NotAnEndpointError` since the path will be canonicalized (as above) and result in `/bar`, and `bar` is not a valid endpoint.
  * A `POST` request for `/foobar` will raise `mixnmatchttp.endpoints.MethodNotAllowedError` since `/foobar` only allows HTTP `GET`.
  * A request for `/debug/../foobar` will call parent's `do_default` with `ep`, a copy of `MyHandler._endpoints['foobar']`. `ep.root` will be "", `ep.sub` will be "foobar", `ep.args` will be "".
  * A request for `/debug/foo/bar` will raise `mixnmatchttp.endpoints.ExtraArgsError` since `/debug` expect exactly one argument.
  * A request for `/debug/bla/debug/foo` will call `do_debug` with `ep`, a copy of `MyHandler._endpoints['debug']['*']['debug']['*']`. `ep.root` will be "debug", `ep.sub` will be "debug", `ep.args` will be "", and `ep.params` will be `{'debug': 'bla', 'debug2': 'foo'}`.
  * A request for `/parameter` or `/parameter/foo` will raise `mixnmatchttp.endpoints.MissingArgsError` since `/foo` expect exactly one argument.
  * A request for `/parameter/foo/bar` will call `do_parameter` with `ep`, a copy of `MyHandler._endpoints['parameter']['*']`. `ep.root` will be "/parameter", `ep.sub` will be "foo", `ep.args` will be "" and `params['parameter']` will be "foo". The page will display "foo = bar"
  * A request for `/parameter/foo/special` will call `do_parameter_special` with `ep`, a copy of `MyHandler._endpoints['parameter']['*']['special']`. `ep.root` will be "/parameter/foo/special", `ep.sub` will be "", `ep.args` will be "" and `params['parameter']` will be "foo". The page will display "A very special parameter!"
  * A request for `/refreshme` will render a page which refreshes every 30 seconds (default).
  * A request for `/refreshme/5` will render a page which refreshes every 5 seconds.

# Handlers

## AuthCookieHTTPRequestHandler and AuthJWTHTTPRequestHandler

Implements username:password authentication via form or JSON `POST` request. Has configurable file paths/endpoints for which authentication is required.

These classes store users and sessions in memory via `BaseAuthInMemoryHTTPRequestHandler`. It's recommended you implement your own class that inherits `BaseAuthCookieHTTPRequestHandler` or `BaseAuthJWTHTTPRequestHandler` and that defines the relevant methods to save, retrieve and update users and sessions (see `BaseAuthInMemoryHTTPRequestHandler`).

Users can be loaded from a file with the `load_users_from_file` method. For JWT auth, a public/private key pair can be loaded with the `set_JWT_keys` method.

  * `GET|POST /login`: username and password authentication
    - Supported URL parameters:
      + `goto`: Redirect to this URL
    - Required body or URL parameters (unless no userfile was given, in which case it always authenticates):
      + `username`: Username (duh)
      + `password`: Password (duh)
    - Response codes:
      + `200 OK`: Authentication successful; issues a `SESSION` cookie or sends a JWT `access_token` and a randon `refresh_token`
      + `401 Unauthorized`: Username or password invalid;
      + `302 Found`: (For cookies only) Location is as requested via the `goto` parameter
    - Notes:
      + Cookies are issued with the `HttpOnly` flag, and if over SSL with the `Secure` flag as well; Can optionally set SameSite
      + Cookie, JWT and refresh token lifetimes (as well as other settings) are configurable via class attributes, see pydoc.
  * `GET|POST /logout`: Clears the `SESSION` cookie from the browser and the server (if using cookies), or removes the refresh token (if given)
    - Supported URL parameters:
      + `goto`: Redirect to this URL
    - Optional body parameters (for JWT only):
      + `refresh_token`: Current refresh token to be expired server-side
    - Response codes:
      + `200 OK`: Empty body
      + `302 Found`: Location is as requested via the `goto` parameter
    - Notes:
      + The `POST` method is supported only for JWT auth
  * `GET|POST /changepwd`: Changes the password for a given username
    - Supported URL parameters:
      + `goto`: Redirect to this URL
    - Required body or URL parameters:
      + `username`: Username (duh)
      + `password`: Current password
      + `new_password`: New password (duh)
    - Optional body parameters (for JWT only):
      + `refresh_token`: Current refresh token to be expired server-side
    - Response codes:
      + `200 OK`: Success; password is changed, current `SESSION` cookie or `refresh_token` is invalidated and a new session is given
      + `401 Unauthorized`: Username or password invalid
      + `302 Found`: (For cookies only) Location is as requested via the `goto` parameter

## CachingHTTPRequestHandler

Allows saving of content as a named page for later request, or displaying the encoded (URL or base64) request content as a page in response.

  * `POST /echo`: Render the requested content
    - Supported URL parameters:
      + `data`: The encoded content of the page to be rendered (required)
      + `type`: The content type of the rendered page (defaults to text/plain)
    - Supported formats:
      + `application/json` with `base64` encoded data
      + `application/x-www-form-urlencoded` (with URL encoded data)
    - Response codes:
      + `200 OK`: The body and `Content-Type` are as requested
      + `400 Bad Request`: Cannot decode data or find the data parameter
  * `POST /cache/{name}`: Temporarily save the requested content (in memory only)
    - Supported URL parameters and formats are the same as for `POST /echo`
    - Response codes:
      + `204 No Content`: Page cached
      + `500 Server Error`: Maximum cache memory reached, or page `{name}` already cached
    - Notes:
      + Once saved, a page cannot be overwritten (until the server is shutdown) even if it is cleared from memory (see `/cache/clear`)
  * `GET /cache/{name}`: Retrieve a previously saved page
    - Response codes:
      + `200 OK`: The body and `Content-Type` are as requested during caching
      + `500 Server Error`: No such cached page, or page cleared from memory
  * `GET /cache/clear/{name}`: Clear a previously saved page to free memory
    - Response codes:
      + `204 No Content`: Page cleared
  * `GET /cache/clear`: Clear all previously saved pages to free memory
    - Response codes:
      + `204 No Content`: All pages cleared
  * `GET /cache/new`: Get a random UUID
    - Response codes:
      + `200 OK`: Body contains a randomly generated UUID; use in `POST /cache/{uuid}`

## ProxyingHTTPRequestHandler

Redirects (with `307`) to any address given in the URL.

  * `GET /goto/{address}`: Redirect to this (URI-decoded) address
    - Response codes:
      + `302 Found`: Location is the address which follows `/goto/`; if domain is not given (i.e. address does not start with `schema://` or `//`) it is taken from the `Referer`, `Origin`, `X-Forwarded-Host`, `X-Forwarded-For` or `Forwarded`
      + `200 OK`: Empty body; this happens if address was relative (no domain) and neither of the aforementioned headers was given
    - Notes:
      + Unlike the address given as a `goto` parameter to some of the other endpoints, the address here is not URI-decoded
      + The `{address}` is not parsed at all, its path is not canonicalized unlike calls to other endpoints. I.e. `/login///foo.baz/../..//cache` will call `/cache`, but `/goto///foo.baz/../..//cache` will redirect to `//foo.baz/../..//cache` (remote host `foo.baz` with path `../..//cache`)

# Known issues

  * Clearing of cache is not done safely in mutli-threaded context. You may experience issues under heavy load. *Solution*: Wait for fix...
  * When running as a signle thread (default), the server sometimes hangs. It seems to be an issue whereby some browsers don't close the socket. *Solution*: Run the server in multi-thread mode (`-t` option).
  * Occasionally a `BrokenPipeError` is thrown. It happens with some browsers which close the socket abruptly. *Solution*: Just ignore it.

# Coming soon

  * MT-safe saving and clearing of cache

## Possibly coming at some point

  * Database lookup of users
  * Password policy

# Demos and source

Source code and demo scripts which build on the handlers can be found at [https://github.com/aayla-secura/mixnmatchttp](https://github.com/aayla-secura/mixnmatchttp)
