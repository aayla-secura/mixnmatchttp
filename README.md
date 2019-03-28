# Overview

`mixnmatchttp` is a modular HTTP/S server based on [Python's http server](https://docs.python.org/3/library/http.server.html) that lets you "mix 'n' match" various functionalities. It defines several handlers, which are wrappers around `http.server.SimpleHTTPRequestHandler`, as well as a `ThreadingHttpServer` which can be used in place of Python's `http.server.HTTPServer` for multi-threading support.

# Quick start

Handlers define special endpoints and/or templates as class attributes.

Endpoints are the RESTful API of the server. A request which does not map to an endpoint is treated as a request for a file or directory (Python's http server handles it).

Template pages are parametrized response bodies. Templates specify a template page to be used with and give a dictionary of parameters and values to use with the template. Each parameter value may also contain dynamic parameters, which are given to the `BaseHTTPRequestHandler.page_from_template` method, which constructs the final page.
You can inherit from one or more of the handlers. Each parent's endpoints/templates will be copied to, without overwriting, your child class' endpoints/templates.

**Important notes:**

  * Templates and template pages should be defined as `mixnmatchttp.common.DictNoClobber`.
  * If you need to override any of the HTTP method handlers (e.g. `do_GET`), you must decorate them with `mixnmatchttp.handlers.base.methodhandler`, as shown below. And if you need to call any of the parent's HTTP method handlers you must call the original wrapped method using the `__wrapped__` attribute, as shown below.

---

Some methods that you may want to override, as well as implementing a custom endpoint and template, are shown below for `MyHandler`:

```python
import re
import ssl
from http.server import HTTPServer
from mixnmatchttp.servers import ThreadingHttpServer
from mixnmatchttp import endpoints
from mixnmatchttp.handlers import BaseHTTPRequestHandler,methodhandler
from mixnmatchttp.common import DictNoClobber

class MyHandler(BaseHTTPRequestHandler):
    _endpoints = endpoints.Endpoints(
            # Default subpoint arguments are:
            # _default = {
            #         'allowed_methods': {'GET'},
            #         'args': 0,
            #         'raw_args': False,
            #         }
            # Every endpoints has a default subpoint named ''
            default={},
            refreshme={
                '': {
                    'args': endpoints.ARGS_OPTIONAL,
                    },
                },
            debug={
                '': {
                    'allowed_methods': {'GET', 'POST'},
                    'args': 1,
                    },
                'sub': {
                    'args': endpoints.ARGS_ANY,
                    'raw_args': True, # don't canonicalize path
                    },
                },
            )
    _template_pages = DictNoClobber(
        simpletxt={
            'data':'$CONTENT',
            'type':'text/html'
            },
        simplehtml={
            'data':'''
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
            'type':'text/html'
            },
        )
    _templates = DictNoClobber(
        refresh={
            'fields':{
                'HEAD':'<meta http-equiv="refresh" content="${interval}">',
                'TITLE':'Example',
                'BODY':'<h1>Example page, will refresh every ${interval}s.</h1>',
            },
            'page': 'simplehtml',
        },
        debug={
            'fields':{
                'CONTENT':'You called endpoint /$root/$sub$args',
            },
            'page': 'simpletxt',
        },
    )

    def do_default(self, sub, args):
        '''Handler for the endpoint /default'''
        self.send_response_default()

    def do_refreshme(self, sub, args):
        if not args:
            args = '30'

        '''Handler for the endpoint /refreshme'''
        page = self.page_from_template(self.templates['refresh'],
                {'interval': args})
        self.render(page)

    def do_debug(self, sub, args):
        '''Handler for the endpoint /debug'''
        page = self.page_from_template(self.templates['debug'],
                {'root': 'debug', 'sub': sub, 'args': args})
        self.render(page)

    @methodhandler
    def do_GET(self):
        # Do something here
        super().do_GET.__wrapped__()

    def denied(self):
        '''Deny access to /forbidden'''
        if re.match('^/forbidden(/|$)', self.pathname):
            # return args are passed to BaseHTTPRequestHandler.send_error
            # in that order; both messages are optional
            return (403, None, 'Access denied')
        return super(MyHandler, self).denied()

    def no_cache(self):
      '''Only allow caching of scripts'''
      return (not self.pathname.endswith('.js')) or super(MyHandler, self).no_cache()

    def send_custom_headers(self):
      '''Send our custom headers'''
      self.send_header('X-Foo', 'Foobar')


if __name__ == "__main__":
    use_SSL = False
    keyfile = '' # path to PEM key, if use_SSL is True
    certfile = '' # path to PEM certificate, if use_SSL is True
    srv_cls = HTTPServer
    # srv_cls = ThreadingHttpServer # if using multi-threading
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
        httpd.socket.close()
```

  * A request for `/debug/sub/..//foo/../bar/./baz` will call `self.do_debug` with arguments `('sub', '..//foo/../bar/./baz')`. `self.command` will give the HTTP method.
  * A request for `/debug/foo/../bar` will canonicalize the path to `/debug/bar` (since `raw_args` for `/debug` is `False`) call `do_debug` with arguments `('', 'bar').
  * A request for `/debug/../bar` will raise `mixnmatchttp.endpoints.NotAnEndpointError` since the path will be canonicalized (as above) and result in `/bar`, and `bar` is not a valid endpoint.
  * A `POST` request for `/default` will raise `mixnmatchttp.endpoints.MethodNotAllowedError` since `/default` only allows HTTP `GET`.
  * A request for `/debug/../default` will call `do_default` with arguments `('', '').
  * A request for `/debug/foo/bar` will raise `mixnmatchttp.endpoints.ExtraArgsError` since `/debug` expect exactly one argument.
  * A request for `/debug` will raise `mixnmatchttp.endpoints.MissingArgsError` since `/debug` expect exactly one argument.
  * A request for `/refreshme` will render a page which refreshes every 30 seconds (default).
  * A request for `/refreshme/5` will render a page which refreshes every 5 seconds.

# Handlers

## AuthHTTPRequestHandler

Implements dummy authentication (no credentials required, but issues cookies). Has configurable file paths/endpoints for which authentication is required.

  * `GET /login`: Issues a random `SESSION` cookie
    - Supported URL parameters:
      + `goto`: Redirect to this URL
    - Response codes:
      + `200 OK`: Empty body
      + `302 OK`: Location is as requested via the `goto` parameter
    - Notes:
      + Sessions are forgotten on the server side upon restart
      + Cookies are issued with the `HttpOnly` flag, and if over SSL with the `Secure` flag as well
  * `GET /logout`: Clears the `SESSION` cookie from the browser and the server
    - Supported URL parameters:
      + `goto`: Redirect to this URL
    - Response codes:
      + `200 OK`: Empty body
      + `302 OK`: Location is as requested via the `goto` parameter

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
  * Authentication with credentials
  * Unlimited levels of subpoints (e.g. `/root/sub1/sub2/sub3/...`)

# Demos and source

Source code and demo scripts which build on the handlers can be found at [https://github.com/aayla-secura/mixnmatchttp](https://github.com/aayla-secura/mixnmatchttp)
