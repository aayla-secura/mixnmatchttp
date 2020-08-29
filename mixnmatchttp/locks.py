import logging
import threading
import time
from functools import wraps


logger = logging.getLogger(__name__)


class LockTimeoutError(Exception):
    def __init__(self, name, *args):
        super().__init__(
            'Timed out waiting for lock {!s}'.format(name), *args)

class ContextDecorator:
    # From https://coderwall.com/p/0lk6jg/
    # python-decorators-vs-context-managers-have-your-cake-and-eat-it
    def __enter__(self):
        return self

    def __exit__(self, typ, val, traceback):
        pass

    def __call__(self, f):
        if self.raise_on_error is None:
            self.raise_on_error = True

        @wraps(f)
        def wrapper(*args, **kw):
            with self as acquired:
                if acquired:
                    return f(*args, **kw)
        return wrapper

class named_lock(ContextDecorator):
    # use a class-level condition for safe manipulating of the class
    # locks and lock_conditions dictionary in non-atomic operations
    busy = threading.Condition(threading.Lock())
    locks = {}
    locks_busy = {}

    def __init__(self, timeout, raise_on_error=None, name=None):
        self.timeout = timeout
        self.name = name
        self.raise_on_error = raise_on_error
        self.lock = None
        self.lock_busy = None

    def __enter__(self):
        with self.busy:
            self.lock_busy = self.locks_busy.get(self.name, None)
            if self.lock_busy is None:
                self.lock_busy = threading.Condition(threading.Lock())
                self.locks_busy[self.name] = self.lock_busy
                self.locks[self.name] = threading.Lock()
            self.lock = self.locks[self.name]

        self.lock_busy.acquire()
        current_time = start_time = time.time()
        while current_time < start_time + self.timeout:
            if self.lock.acquire(False):
                self.lock_busy.release()
                return True
            else:
                logger.debug('Waiting')
                self.lock_busy.wait(
                    self.timeout - current_time + start_time)
                logger.debug('Woke up')
                current_time = time.time()
        self.lock_busy.release()
        if self.raise_on_error:
            raise LockTimeoutError(self.name)
        logger.error(
            'Timed out waiting for lock {!s}'.format(self.name))
        return False

    def __exit__(self, typ, val, traceback):
        if self.lock.locked():
            self.lock.release()
            with self.lock_busy:
                self.lock_busy.notify_all()
