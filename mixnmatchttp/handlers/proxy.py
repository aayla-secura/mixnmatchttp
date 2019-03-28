#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from builtins import str
from builtins import filter
from future import standard_library
standard_library.install_aliases()
import logging
import re

from .. import endpoints
from ..common import param_dict
from .base import BaseHTTPRequestHandler

_logger = logging.getLogger(__name__)

class ProxyingHTTPRequestHandler(BaseHTTPRequestHandler):
    _endpoints = endpoints.Endpoints(
            goto={
                # call it as /goto?{params for this server}/{URI-decoded address};
                # include the ? after /goto even if not giving parameters,
                # otherwise any parameters in the address would be
                # consumed
                '': {
                    'allowed_methods': {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'},
                    'args': endpoints.ARGS_ANY,
                    'raw_args': True,
                    },
                },
            )

    def do_goto(self, sub, args):
        '''Redirects to the path following /goto/
        
        If the path does not include a domain, it is taken from the
        following headers, in this order:
        - Referer
        - Origin
        - X-Forwarded-Host
        - X-Forwarded-For
        - Forwarded
        '''

        # check if path includes domain
        if re.match('(https?:)?//[^/]', args):
            self.send_response_goto(code=307, url=args)
            return

        def send_redir(host, proto='', pref='', **kwargs):
            if args[:1] == '/':
                # relative to root => ignore prefix path
                pref = ''
            elif pref[-1:] != '/':
                # otherwise make sure there's a trailing slash for prefix
                pref += '/'
            if proto and proto[-1] != ':':
                proto += ':'
            path = ''.join([proto, '//', host, pref, args])
            _logger.debug('Redirecting to {}'.format(path))
            self.send_response_goto(code=307, url=path)

        fwd = dict()
        # otherwise check Referer and Origin
        try:
            # a valid Origin shouldn't have a path, but nevermind
            fwd = re.match(
                    '^(?P<proto>https?:|)//(?P<host>[^/]+)(?P<pref>/?.*)',
                    list(filter(None, [
                        self.headers.get('Referer'),
                        self.headers.get('Origin'),
                        ]))[0]).groupdict()
        except (IndexError, AttributeError):
            # otherwise check X-Forwarded-*
            _logger.debug('Checking Origin and X-Forwarded-*')
            try:
                fwd['host'] = list(filter(None, [
                    self.headers.get('X-Forwarded-Host'),
                    self.headers.get('X-Forwarded-For')
                    ]))[0]
            except IndexError:
                # otherwise check Forwarded
                _logger.debug('Checking Forwarded')
                fwdstr = self.headers.get( 'Forwarded')
                if fwdstr is None:
                    fwdstr = ''
                fwd = param_dict(fwdstr.replace('for=', 'host='))
            else:
                # one of X-Forwarded-* may have matched
                fwd['proto'] = self.headers.get('X-Forwarded-Proto')
                if fwd['proto'] is None:
                    fwd['proto'] = ''

        try:
            _logger.debug('fwd: {}'.format(fwd))
            send_redir(**fwd)
        except TypeError:
            _logger.debug("Couldn't figure out host to redirect to...")
            self.send_response_default()
