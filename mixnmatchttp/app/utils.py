import os
import sys
import errno
import argparse

class AppendUniqueArgAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            curr = getattr(namespace, self.dest)
        except AttributeError:
            setattr(namespace, self.dest, values)
        else:
            if values not in curr:
                curr.append(values)


def exit(error, rc=None):
    if isinstance(error, Exception):
        try:
            rc = error.errno
        except AttributeError:
            pass
    if rc is None:
        rc = -1
    if rc == 0:
        out = sys.stdout
    else:
        out = sys.stderr
    out.write('{}\n'.format(error))
    sys.exit(rc)

def read_line(prompt):
    sys.stdout.write('{}: '.format(prompt))
    sys.stdout.flush()
    return sys.stdin.readline().rstrip('\r\n')

def make_dirs(path, is_file=False, mode=0o755):
    if path is None:
        return
    if is_file:
        path = os.path.dirname(os.path.abspath(path))
    try:
        os.makedirs(path, mode=mode, exist_ok=True)
    # let other exceptions through
    except FileExistsError:
        exit(NotADirectoryError(
            errno.ENOTDIR, os.strerror(errno.ENOTDIR), path))

def ensure_exists(path, is_file=True):
    if path is None:
        return
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
