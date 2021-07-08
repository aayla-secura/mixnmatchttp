import unittest

import loggers
from mixnmatchttp.utils import is_time_like, is_timestamp_like, \
    curr_datetime, curr_timestamp


class Test(unittest.TestCase):
    def test_is_time(self):
        self.assertFalse(is_time_like(None))
        self.assertFalse(is_time_like(1))
        self.assertFalse(is_time_like('x'))
        self.assertTrue(is_time_like('1/1'))
        self.assertTrue(is_time_like('Fri, 09 Jul 2021 10:07:13 NZST'))

    def test_is_timestamp(self):
        self.assertFalse(is_timestamp_like(-1))
        self.assertTrue(is_timestamp_like(0))
        self.assertTrue(is_timestamp_like(curr_timestamp()))
        self.assertTrue(is_timestamp_like(curr_timestamp(to_ms=True)))

        # TODO


if __name__ == '__main__':
    unittest.main()
