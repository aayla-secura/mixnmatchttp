from ._py2 import *

import os
import sys
import errno
from signal import signal, SIGTERM, SIGINT, SIG_DFL
import ssl
import re
import urllib
from time import sleep
import tempfile
import logging
from copy import copy
import argparse
from string import Template
import json
from awesomedict import AwesomeDict
from ._py2 import _JSONDecodeError

# optional features
try:
    from daemon.daemon import DaemonContext
    from daemon.pidfile import TimeoutPIDLockFile
except ImportError:
    pass

from http.server import HTTPServer

from .utils import randstr, is_str
from .servers import ThreadingHTTPServer
from .db import DBConnection, is_base, parse_db_url
from .handlers.authenticator.dbapi import DBBase


MY_PKG_NAME = __name__.split('.')[0]


class WebApp(object):
    '''TODO'''

    def __init__(self,
                 reqhandler,
                 description='',
                 support_ssl=True,
                 support_cors=True,
                 support_daemon=False,
                 auth_type='cookie',
                 db_bases={},
                 log_fmt=None):
        '''TODO

        reqhandler will be replaced
        '''

        if support_daemon:
            try:
                DaemonContext
            except NameError:
                exit('You need the python-daemon package '
                     'to use daemon mode.')
        for name, d in db_bases.items():
            if not is_str(name):
                exit('db_bases keys should be strings')
            if name.replace(' ', '') != name:
                exit('db_bases keys cannot contain spaces.')
            if 'base' not in d:
                exit("db_bases items should contain a 'base' key.")
            if not is_base(d['base']):
                exit('db_bases base should be a declarative base.')
        self._is_configured = False
        self._delete_tmp_userfile = False
        # access.log is for http.server (which writes to stderr)
        self.access_log = None
        self.httpd = self.url = self.pidlockfile = None
        self.reqhandler = reqhandler
        self.auth_type = auth_type
        self.db_bases = db_bases
        self.log_fmt = log_fmt
        if self.log_fmt is None:
            self.log_fmt = \
                '[%(asctime)s] %(name)s (%(threadName)s): %(message)s'
        self.conf = Conf(skip=['action',
                               'config',
                               'save_config',
                               'debug_log',
                               'add_users'])

        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description=description)
        if support_daemon:
            self.parser.add_argument(
                'action', nargs='?',
                choices=['start', 'stop', 'restart', 'status'],
                default='start',
                help='Action to take on the running daemon.')
        listen_parser = self.parser.add_argument_group(
            'Listen options')
        listen_parser.add_argument(
            '-a', '--address', dest='address',
            default='127.0.0.1', metavar='IP',
            help='Address of interface to bind to.')
        listen_parser.add_argument(
            '-p', '--port', dest='port', metavar='PORT', type=int,
            help=('HTTP port to listen on. Default is 80 if not '
                  'over SSL or 443 if over SSL.'))

        if support_ssl:
            ssl_parser = self.parser.add_argument_group('SSL options')
            ssl_parser.add_argument(
                '-s', '--ssl', dest='ssl', default=False,
                action='store_true', help='Use SSL.')
            ssl_parser.add_argument(
                '--no-ssl', dest='ssl', action='store_false',
                help=("Don't use SSL. This is the default, but can "
                      "be used to override configuration file "
                      "setting."))
            ssl_parser.add_argument(
                '--cert', dest='certfile', metavar='FILE',
                help='PEM file containing the server certificate.')
            ssl_parser.add_argument(
                '--key', dest='keyfile', metavar='FILE',
                help=('PEM file containing the private key for the '
                      'server certificate.'))

        if auth_type:
            auth_parser = self.parser.add_argument_group(
                'Authentication options')
            if auth_type == 'jwt':
                auth_parser.add_argument(
                    '--jwt-key', dest='jwt_key', metavar='PASSWORD',
                    help=('A password to use for symmetric signing '
                          'of JWT or a passphrase used to decrypt '
                          'the private key (for asymmetric '
                          'algorithms). If none is given and the '
                          'algorithm is symmetric, then a random '
                          'one is generated (meaning all JWT keys '
                          'become invalid upon restart). If none is '
                          'given and the algorithm is asymmetric, '
                          'the key must be decrypted. If "-" is '
                          'supplied, then it is read from stdin.'))
                auth_parser.add_argument(
                    '--jwt-priv-key', dest='jwt_priv_key',
                    help=('A private PEM key for use with asymmetric '
                          'JWT encodings.'))
                auth_parser.add_argument(
                    '--jwt-algo', dest='jwt_algo',
                    help=('The algorithm used to encode JWTs. '
                          'Default is HS256 is no private key is '
                          'given, otherwise RS256.'))
            auth_parser.add_argument(
                '--userfile', dest='userfile', metavar='FILE',
                help=('File containing one username:password[:roles] '
                      'per line. roles is an optional comma-'
                      'separated list of roles.'))
            auth_parser.add_argument(
                '--add-users', dest='add_users', action='store_true',
                default=False,
                help=('Prompt to create users. Entries will be '
                      'appended to --userfile if given. '
                      '--userfile-plain determines if the passwords '
                      'are hashed before written to the --userfile.'))
            auth_parser.add_argument(
                '--userfile-plain', dest='userfile_hashed',
                default=True, action='store_false',
                help='The passwords in userfile are in cleartext.')
            auth_parser.add_argument(
                '--userfile-hashed', dest='userfile_hashed',
                action='store_true',
                help=('The passwords in userfile are hashed. This is '
                      'the default, but can be used to override '
                      'configuration file setting.'))
            auth_parser.add_argument(
                '--hash-type', dest='userfile_hash_type', nargs='?',
                const=None, default=None,
                choices=reqhandler._supported_hashes,
                help=('The hashing algorithm to use. Specifying this '
                      'option without an argument overrides the one '
                      'in the configuration file and resets the '
                      'hashing to none (plaintext).'))

        if support_cors:
            cors_parser = self.parser.add_argument_group(
                'CORS options')
            cors_parser.add_argument(
                '-X', '--enable-cors', dest='cors',
                default=False, action='store_true',
                help='Enable CORS support.')
            cors_parser.add_argument(
                '--disable-cors', dest='cors', action='store_false',
                help=('Disable CORS support. This is the default, '
                      'but can be used to override configuration '
                      'file setting.'))
            cors_origin_parser = \
                cors_parser.add_mutually_exclusive_group()
            cors_origin_parser.add_argument(
                '--allowed-origins', dest='cors_origins',
                default=['*'], metavar='Origin', nargs='*',
                help='Allowed origins for CORS requests.')
            cors_origin_parser.add_argument(
                '--allow-any-origin', dest='cors_origins',
                action='store_const', const=['{ECHO}'],
                help=('Allow any origin, i.e. echo back '
                      'the requesting origin.'))
            cors_parser.add_argument(
                '--allowed-headers', dest='cors_headers',
                default=['Accept', 'Accept-Language',
                         'Content-Language', 'Content-Type',
                         'Authorization'],
                metavar='Header: Value', nargs='*',
                help='Headers allowed for CORS requests.')
            cors_parser.add_argument(
                '--allowed-methods', dest='cors_methods',
                default=['POST', 'GET', 'OPTIONS', 'HEAD'],
                metavar='Method', nargs='*',
                help=('Methods allowed for CORS requests. OPTIONS '
                      'to one of the special endpoints always '
                      'return the allowed methods of that endpoint.'))
            cors_parser.add_argument(
                '--allow-credentials', dest='cors_creds',
                default=False, action='store_true',
                help='Allow sending credentials with CORS requests')
            cors_parser.add_argument(
                '--disallow-credentials', dest='cors_creds',
                action='store_false',
                help=('Do not allow sending credentials with CORS '
                      'requests. This is the default, but can be '
                      'used to override configuration file setting.'))

        if db_bases:
            db_parser = self.parser.add_argument_group(
                'Database options')
            for name in self.db_bases.keys():
                db_parser.add_argument(
                    '--{}-dburl'.format(name),
                    dest='{}_dburl'.format(name),
                    metavar=('dialect://[username:password@]'
                             'host/database'),
                    help='URL of the {} database.'.format(name))

        misc_http_parser = self.parser.add_argument_group(
            'Other HTTP options')
        misc_http_parser.add_argument(
            '-H', '--headers', dest='headers',
            default=[], metavar='Header: Value', nargs='*',
            help='Additional headers to include in the response.')

        misc_server_parser = self.parser.add_argument_group(
            'Logging and process options')
        if support_daemon:
            misc_server_parser.add_argument(
                '-P', '--pidfile', dest='pidfile', metavar='FILE',
                default='/var/run/pyhttpd.pid',
                help='Path to pidfile when running in daemon mode.')
            misc_server_parser.add_argument(
                '-d', '--daemon', dest='daemonize',
                default=False, action='store_true',
                help='Run as a daemon.')
            misc_server_parser.add_argument(
                '-f', '--foreground', dest='daemonize',
                action='store_false',
                help=('Run in foreground. This is the default, '
                      'but can be used to override configuration '
                      'file setting.'))
        misc_server_parser.add_argument(
            '-c', '--config', dest='config', metavar='FILE',
            help=('Configuration file. Command-line options take '
                  'precedence.'))
        misc_server_parser.add_argument(
            '--save-config', dest='save_config',
            default=False, action='store_true',
            help='Update or create the configuration file.')
        misc_server_parser.add_argument(
            '-r', '--webroot', dest='webroot', metavar='DIR',
            default='/var/www/html',
            help=('Directory to serve files from. '
                  'Current working directory will be changed to it.'))
        misc_server_parser.add_argument(
            '--multithread', dest='multithread',
            default=True, action='store_true',
            help=('Use multi-threading support. This is the default, '
                  'but can be used to override configuration '
                  'file setting.'))
        misc_server_parser.add_argument(
            '--no-multithread', dest='multithread',
            action='store_false',
            help='Disable multi-threading support.')
        if support_daemon:
            misc_server_parser.add_argument(
                '-l', '--logdir', dest='logdir', metavar='DIR',
                help=('Directory that will hold the log files. '
                      'Default when running in daemon mode is '
                      '/var/log/pyhttpd. Default in foreground mode '
                      'is to print print all output to the console.'))
        else:
            misc_server_parser.add_argument(
                '-l', '--logdir', dest='logdir', metavar='DIR',
                help=('Directory that will hold the log files. '
                      'Default is to print print all output to '
                      'the console.'))
        misc_server_parser.add_argument(
            '--log', dest='log', nargs='+',
            action='append', default=[], metavar='PACKAGE [FILENAME]',
            help=('Enable logging output for the given package. '
                  'FILENAME will be stored in --logdir if given '
                  '(otherwise ignored and output goes to the '
                  'console). Default is <PACKAGE>.log. Only INFO '
                  'level messages go in FILENAME, WARNING and ERROR '
                  'go to error.log (or stderr if no --logdir). '
                  'Note that printing of request lines to '
                  'access.log (or stderr) is always enabled. '
                  'This option can be given multiple times.'))
        misc_server_parser.add_argument(
            '--request-log', dest='request_log', nargs='?',
            const='request.log', metavar='[FILENAME]',
            help=('Enable logging of full requests. FILENAME '
                  'defaults to request.log if not given.'))
        misc_server_parser.add_argument(
            '--debug-log', dest='debug_log', nargs='+',
            action='append', default=[], metavar='PACKAGE [FILENAME]',
            help=('Enable debugging output for the given package. '
                  'FILENAME defaults to debug.log. Note that this '
                  'option is not saved in the configuration file. '
                  'Otherwise the behaviour is similar as --log.'))

    def configure(self):
        '''TODO'''

        if self._is_configured:
            raise RuntimeError("'configure' can be called only once.")

        args = self.parser.parse_args()
        #### Load/save/update config file
        if args.config is not None:
            try:
                self.update_config(args.config)
            except FileNotFoundError as e:
                if not args.save_config:
                    exit(e)
        # update without overriding values loaded from the conf file
        # with non-explicitly set values (defaults)
        self.parser.parse_args(namespace=self.conf)
        # do not raise AttributeError but return None for command-line
        # options which are not supported
        self.conf._error_on_missing = False
        self.action = self.conf.action
        if self.action is None:
            self.action = 'start'
        if self.conf.save_config:
            if self.conf.config is None:
                exit('--save-config requires --config.')
            self.save_config(self.conf.config)

        #### Preliminary checks and directory creation
        if self.conf.port is None:
            self.conf.port = 443 if self.conf.ssl else 80
        if self.conf.ssl:
            if self.conf.certfile is None \
                    or self.conf.keyfile is None:
                exit('--certfile and --keyfile must be given')
        if self.conf.daemonize or self.action != 'start':
            make_dirs(self.conf.pidfile, is_file=True)
            self.pidlockfile = TimeoutPIDLockFile(
                os.path.abspath(self.conf.pidfile), 3)
            if self.action in ['stop', 'status']:
                self.conf.daemonize = False
        if self.action in ['start', 'restart']:
            self._prepare_for_start()

        self.url = '{proto}://{addr}:{port}'.format(
            proto='https' if self.conf.ssl else 'http',
            addr=self.conf.address,
            port=self.conf.port)
        self._is_configured = True

    def update_config(self, conffile):
        '''TODO'''

        with open(conffile, 'r') as f:
            content_raw = f.read()
        # return an empty value for missing env variables
        env = AwesomeDict(os.environ).set_defaults({'.*': ''})
        content = Template(content_raw).substitute(env)
        try:
            settings = json.loads(content)
        except _JSONDecodeError as e:
            exit('Invalid configuration file: {}'.format(e))
        self.conf._update(settings)

    def save_config(self, conffile):
        '''TODO'''

        f = open(conffile, 'w')
        json.dump(self.conf._to_dict(), f, indent=2)
        f.close()

    def run(self):
        '''TODO'''

        if not self._is_configured:
            self.configure()
        if self.action == 'restart':
            self._stop()
            self.action = 'start'
        getattr(self, '_{}'.format(self.action))()

    def _prepare_for_start(self):
        def send_custom_headers(reqself):
            super(self.reqhandler, reqself).send_custom_headers()
            return self._send_cors_headers(reqself)

        #### Preliminary checks and directory creation
        if self.conf.logdir is None and self.conf.daemonize:
            self.conf.logdir = '/var/log/pyhttpd'
        if self.conf.logdir is not None:
            self.conf.logdir = os.path.abspath(
                self.conf.logdir).rstrip('/')
            make_dirs(self.conf.logdir, mode=0o700)
        # check webroot
        self.conf.webroot = self.conf.webroot.rstrip('/')
        #  self.conf.webroot = self.conf.webroot.strip('/')
        #  if not os.path.abspath(self.conf.webroot).startswith(
        #          os.getcwd()):
        #      exit('The given webroot is outside the current root')
        ensure_exists(self.conf.webroot, is_file=False)
        # check userfile
        if self.conf.userfile is not None \
                and not self.conf.add_users:
            ensure_exists(self.conf.userfile, is_file=True)
        for name in self.db_bases.keys():
            url = getattr(self.conf, '{}_dburl'.format(name))
            if not url:
                exit(('You must specify the {}_dburl '
                      'configuration option or the --{}-dburl '
                      'command-line option.').format(name, name))
            conn = parse_db_url(url)
            if not conn:
                exit('Invalid database URL: {}'.format(url))
            if conn['dialect'] == 'sqlite' and \
                    conn['database'] not in [':memory:', None]:
                make_dirs(conn['database'], is_file=True)

        #### Create the new request handler class
        attrs = {}
        if self.conf.cors:
            attrs.update({
                'send_custom_headers': send_custom_headers})
        if self.auth_type is not None:
            attrs.update({
                '_is_SSL': self.conf.ssl,
                '_pwd_type': self.conf.userfile_hash_type})
        self.reqhandler = type(
            '{}Custom'.format(self.reqhandler.__name__),
            (self.reqhandler,), attrs)

        #### Read users from stdin
        if self.conf.add_users:
            # if userfile is not given, use a temporary file
            if self.conf.userfile is None:
                self._delete_tmp_userfile = True
                self.conf.userfile = \
                    tempfile.NamedTemporaryFile(
                        mode='a', delete=False)
            else:
                self.conf.userfile = open(self.conf.userfile, 'a')
            sys.stdout.write('Creating users\n')
            transformer = None
            if self.conf.userfile_hash_type is not None \
                    and self.conf.userfile_hashed:
                # we need to hash the passwords here, since userfile
                # may already contain existing hashes
                transformer = getattr(
                    self.reqhandler,
                    '_transform_password_{}'.format(
                        self.conf.userfile_hash_type))
            while True:
                username = read_line('Enter username (blank to quit)')
                if not username:
                    break
                raw_password = read_line(
                    'Enter password (blank for random)')
                roles = read_line('Enter comma-separated roles')
                if not raw_password:
                    raw_password = randstr(16, skip=':')
                if transformer is not None:
                    password = transformer(raw_password)
                else:
                    password = raw_password
                self.conf.userfile.write(
                    '{}:{}:{}\n'.format(username, password, roles))
                sys.stdout.write(
                    'Created user {} with password {}\n'.format(
                        username, raw_password))
            self.conf.userfile.close()
            # close the file, so load_users_from_file can start
            # reading it from the start
            self.conf.userfile = self.conf.userfile.name

        #### JWT keys
        if self.auth_type == 'jwt':
            if self.conf.jwt_algo is None:
                if self.conf.jwt_priv_key is None:
                    self.conf.jwt_algo = 'HS256'
                else:
                    self.conf.jwt_algo = 'RS256'
            if self.conf.jwt_key is None \
                    and self.conf.jwt_algo.startswith('HS'):
                self.conf.jwt_key = randstr(16)
            elif self.conf.jwt_key == '-':
                self.conf.jwt_key = read_line('Enter JWT passphrase')
            self.reqhandler.set_JWT_keys(
                passphrase=self.conf.jwt_key,
                algorithm=self.conf.jwt_algo,
                privkey=self.conf.jwt_priv_key)

    def _start(self):
        if self.conf.logdir is not None:
            self.access_log = open('{}/{}'.format(
                self.conf.logdir, 'access.log'), 'ab')

        sys.stderr.write('Starting server on {}\n'.format(self.url))
        #### Daemonize
        if self.conf.daemonize:
            assert self.access_log is not None
            if self.pidlockfile.is_locked():
                exit('PID file {} already locked'.format(
                    self.pidlockfile.path))
            daemon = DaemonContext(
                working_directory=os.getcwd(),
                umask=0o077,
                pidfile=self.pidlockfile,
                signal_map={SIGTERM: None},  # let me handle signals
                stderr=self.access_log)
            daemon.open()

        #### Setup logging
        log_dest = {
            'REQUEST': [],
            'DEBUG': self.conf.debug_log,
            'INFO': self.conf.log,
            'ERROR': self.conf.log}
        if self.conf.logdir is not None:
            log_dest['INFO'].append([__name__, 'event.log'])
        if self.conf.request_log is not None:
            log_dest['REQUEST'].append(
                [MY_PKG_NAME, self.conf.request_log])
        self.loggers = get_loggers(log_dest,
                                   logdir=self.conf.logdir,
                                   fmt=self.log_fmt)

        #### Connect to the databases
        # This has to be done after daemonization because the sockets
        # may be closed
        for name, d in self.db_bases.items():
            base = d['base']
            url = getattr(self.conf, '{}_dburl'.format(name))
            session_kargs = d.get('session_args', {})
            engine_kargs = d.get('engine_args', {})
            cache = d.get('cache', False)
            DBConnection(base,
                         url,
                         session_kargs=session_kargs,
                         engine_kargs=engine_kargs)
            if cache:  # ETag support
                self.reqhandler.enable_client_cache(name, base)

        #### Load users
        if self.conf.userfile is not None:
            self.reqhandler.load_users_from_file(
                self.conf.userfile,
                plaintext=not self.conf.userfile_hashed)
            if self._delete_tmp_userfile:
                os.remove(self.conf.userfile)

        #### Create the server
        # This has to be done after daemonization because it binds to
        # the listening port at creation time
        srv_cls = HTTPServer
        if self.conf.multithread:
            srv_cls = ThreadingHTTPServer
        self.httpd = srv_cls((self.conf.address, self.conf.port),
                             self.reqhandler)
        if self.conf.ssl:
            self.httpd.socket = ssl.wrap_socket(
                self.httpd.socket,
                keyfile=self.conf.keyfile,
                certfile=self.conf.certfile,
                server_side=True)

        #### Setup signal handlers
        signal(SIGTERM, self._term_sighandler)
        signal(SIGINT, self._term_sighandler)

        #### Redirect stderr to access.log
        if self.conf.logdir is not None and not self.conf.daemonize:
            # running in foreground, but logging to logdir, redirect
            # stderr to access.log as http.server writes to stderr
            os.dup2(self.access_log.fileno(), sys.stderr.fileno())

        #### Change working directory and run
        os.chdir(self.conf.webroot)
        self._log_event('Starting server on {}'.format(self.url))
        self.httpd.serve_forever()

    def _stop(self):
        pid = self._get_pid(break_stale=True)
        if pid is None:
            return
        if pid <= 0:
            # tried that... to see what exception will be raised...
            # none was raised
            sys.stderr.write('Invalid PID: {}\n'.format(pid))
        try:
            os.kill(pid, SIGTERM)
        except OSError as e:
            exit('Failed to terminate process {}: {}'.format(
                pid, e), e.errno)
        # wait
        max_wait = 5
        interval = 0.5
        curr_wait = 0
        try:
            while self._is_pid_running():
                if curr_wait >= max_wait:
                    exit('Failed to terminate process {}'.format(pid))
                sleep(interval)
                curr_wait += interval
        except KeyboardInterrupt:
            pass

    def _status(self):
        pid = self._get_pid()
        if pid is None:
            exit('Server is not running', 1)
        if not self._is_pid_running():
            exit('Server is not running, pidfile is old', -1)
        exit('Server is running, pid = {}'.format(pid), 0)

    def _log_event(self, message):
        try:
            self.loggers[__name__]
        except KeyError:
            return
        self.loggers[__name__].info(message)

    def _term_sighandler(self, signo, stack_frame):
        self._log_event('Stopping server on {}'.format(self.url))
        self.httpd.server_close()
        self._log_event('Stopped server on {}'.format(self.url))

        if self.access_log is not None:
            self.access_log.close()
        sys.exit(0)

    def _send_cors_headers(self, reqself):
        def get_cors(what):
            res = getattr(self.conf, 'cors_{}'.format(what))
            if isinstance(res, list):
                return ', '.join(res)
            return res

        for h in self.conf.headers:
            reqself.send_header(*re.split(': *', h, maxsplit=1))
        cors_origins = get_cors('origins')
        if cors_origins is not None:
            cors_origins = urllib.parse.unquote_plus(
                cors_origins)
        if cors_origins == '{ECHO}':
            cors_origins = reqself.headers.get('Origin')
            if not cors_origins:
                cors_origins = '*'
        cors_headers = get_cors('headers')
        cors_methods = get_cors('methods')
        cors_creds = get_cors('creds')
        if cors_origins:
            reqself.send_header('Access-Control-Allow-Origin',
                                cors_origins)
        if cors_headers:
            reqself.send_header('Access-Control-Allow-Headers',
                                cors_headers)
        if cors_methods:
            reqself.send_header('Access-Control-Allow-Methods',
                                cors_methods)
        if cors_creds:
            reqself.send_header('Access-Control-Allow-Credentials',
                                'true')

    def _get_pid(self, break_stale=False):
        if self.pidlockfile is None:
            sys.stderr.write('No PID file supplied\n')
            return None
        if not self.pidlockfile.is_locked():
            #  sys.stderr.write(
            #      'PID file {} not locked\n'.format(
            #          self.pidlockfile.path))
            return None
        if not self._is_pid_running() and break_stale:
            sys.stderr.write(
                'PID file {} is old, removing\n'.format(
                    self.pidlockfile.path))
            self.pidlockfile.break_lock()
            return None
        return self.pidlockfile.read_pid()

    def _is_pid_running(self):
        '''Adapted from daemon.runner'''

        pid = self.pidlockfile.read_pid()
        if pid is not None:
            try:
                os.kill(pid, SIG_DFL)
            except ProcessLookupError:
                return False
            except OSError as e:
                # Under Python 2, process lookup error is an OSError.
                if e.errno == errno.ESRCH:
                    # The specified PID does not exist.
                    return False
            return True
        return False

class LogHandler(object):
    def emit(self, record):
        if record.levelno < self.__class__._min_level \
                or record.levelno > self.__class__._max_level:
            return
        super().emit(record)

class FileHandler(LogHandler, logging.FileHandler):
    pass

class StreamHandler(LogHandler, logging.StreamHandler):
    pass

class ErrorFileHandler(FileHandler):
    _min_level = logging.WARNING
    _max_level = logging.ERROR

class ErrorStreamHandler(StreamHandler):
    _min_level = logging.WARNING
    _max_level = logging.ERROR

class InfoFileHandler(FileHandler):
    _min_level = logging.INFO
    _max_level = logging.INFO

class InfoStreamHandler(StreamHandler):
    _min_level = logging.INFO
    _max_level = logging.INFO

class DebugFileHandler(FileHandler):
    _min_level = logging.DEBUG
    _max_level = logging.DEBUG

class DebugStreamHandler(StreamHandler):
    _min_level = logging.DEBUG
    _max_level = logging.DEBUG

class RequestDebugFileHandler(FileHandler):
    _min_level = 1
    _max_level = 1

class RequestDebugStreamHandler(StreamHandler):
    _min_level = 1
    _max_level = 1

class Conf(object):
    _error_on_missing = True

    def __init__(self, skip=[], settings={}):
        self._skip = copy(skip)
        self._skip.extend(['_skip', '_error_on_missing'])
        self._update(settings)

    def _update(self, settings):
        for k, v in settings.items():
            setattr(self, k, v)

    def _to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k not in self._skip}

    def __getattr__(self, key):
        if self._error_on_missing or key.startswith('_'):
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    type(self), key))
        return None

def exit(error, rc=None):
    if isinstance(error, Exception):
        try:
            rc = error.errno
        except AttributeError:
            pass
    if rc is None:
        rc = -1
    sys.stderr.write('{}\n'.format(error))
    sys.exit(rc)

def read_line(prompt):
    sys.stdout.write('{}: '.format(prompt))
    sys.stdout.flush()
    return sys.stdin.readline().strip('\n').strip('\r')

def get_loggers(destinations_map, logdir=None, fmt=None):
    def unpack_dest(pkg, *files):
        return pkg, files

    log_formatter = None
    if fmt is not None:
        log_formatter = logging.Formatter(
            fmt=fmt, datefmt='%d/%b/%Y %H:%M:%S')
    loggers = {}
    logger_classes = {
        'REQUEST': (RequestDebugStreamHandler,
                    RequestDebugFileHandler, 'request.log'),
        'DEBUG': (DebugStreamHandler, DebugFileHandler, 'debug.log'),
        'INFO': (InfoStreamHandler, InfoFileHandler, None),
        'ERROR': (ErrorStreamHandler, ErrorFileHandler, 'error.log')}

    for level, destinations in destinations_map.items():
        for dest in destinations:
            pkg, files = unpack_dest(*dest)
            if not files:
                files = [None]
            for filename in files:
                streamHandler, fileHandler, def_filename = \
                    logger_classes[level]
                if logdir is None:
                    handler = streamHandler(
                        sys.stderr
                        if level == 'ERROR' else sys.stdout)
                else:
                    if filename is None:
                        filename = def_filename
                    if filename is None:
                        if '/' in pkg:
                            raise ValueError(
                                ('{} cannot be used as a '
                                 'filename').format(pkg))
                        filename = '{}.log'.format(pkg)
                    handler = fileHandler('{}/{}'.format(
                        logdir, filename))
                if log_formatter is not None:
                    handler.setFormatter(log_formatter)
                logger = logging.getLogger(pkg)
                logger.addHandler(handler)
                logger.setLevel(1)  # the handler filters
                loggers[pkg] = logger
    return loggers

def make_dirs(path, is_file=False, mode=0o755):
    if path is None:
        return
    if is_file:
        path = os.path.dirname(os.path.abspath(path))
    # under python2, makedirs doesn't accept exist_ok...
    #  try:
    #      os.makedirs(path, mode=mode, exist_ok=True)
    #  # let other exceptions through
    #  except FileExistsError:
    #      exit(NotADirectoryError(
    #          errno.ENOTDIR, os.strerror(errno.ENOTDIR), path))
    if os.path.exists(path) and not os.path.isdir(path):
        exit(NotADirectoryError(
            errno.ENOTDIR, os.strerror(errno.ENOTDIR), path))
    if not os.path.exists(path):
        os.makedirs(path, mode=mode)

def ensure_exists(path, is_file=True):
    if not os.path.exists(path):
        exit(FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path))
    if is_file:
        if os.path.isdir(path):
            exit(IsADirectoryError(
                errno.EISDIR, os.strerror(errno.EISDIR), path))
    else:
        if not os.path.isdir(path):
            exit(NotADirectoryError(
                errno.ENOTDIR, os.strerror(errno.ENOTDIR), path))
