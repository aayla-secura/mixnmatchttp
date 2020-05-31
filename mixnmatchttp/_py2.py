#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

try:  # python3
    FileNotFoundError
except NameError:  # python 2
    FileExistsError = \
        FileNotFoundError = \
        IsADirectoryError = \
        NotADirectoryError = IOError

# optional, not imported with *
try:  # python3
    from json import JSONDecodeError as _JSONDecodeError
except ImportError:  # python2
    _JSONDecodeError = ValueError
try:
    # python2
    from collections import _abcoll
except ImportError:
    # python3
    from collections import abc as _abcoll
