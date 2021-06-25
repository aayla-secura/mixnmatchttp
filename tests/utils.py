import unittest
import re

import loggers
from mixnmatchttp.utils import merge

class Test(unittest.TestCase):

    def test_merge_dic(self):
        da = dict(a=1, c=1)
        db = dict(a=2, b=3)
        dab = da.copy()
        dab.update(db)
        dba = db.copy()
        dba.update(da)
        self.assertDictEqual(dab, merge(da, db))
        self.assertDictEqual(dba, merge(db, da))

    def test_merge_list(self):
        la = list([1, 2])
        lb = list([3, 4])
        lab = la + lb
        lba = lb + la
        self.assertListEqual(lab, merge(la, lb))
        self.assertListEqual(lba, merge(lb, la))

    def test_merge_tuple(self):
        ta = tuple([1])
        tb = tuple([1, 2])
        tab = ta + tb
        tba = tb + ta
        self.assertTupleEqual(tab, merge(ta, tb))
        self.assertTupleEqual(tba, merge(tb, ta))

    def test_merge_set(self):
        sa = set([1, 2])
        sb = set([1, 3])
        sab = sa.union(sb)
        self.assertSetEqual(sab, merge(sa, sb))

    def test_merge_inplace(self):
        ta = tuple([1])
        tb = tuple([1, 2])
        self.assertRaises(TypeError, merge, ta, tb, inplace=True)
        la = list([1, 2])
        lb = list([3, 4])
        lab = la + lb
        merge(la, lb, inplace=True)
        self.assertListEqual(lab, la)


if __name__ == '__main__':
    unittest.main()
