from unittest import TestCase

from ..utilities import indices

__all__ = ["TestIndices"]


class TestIndices(TestCase):

    # -- -- -- -- [+0 +1 +2 +3 +4] +5 +6 +7 +8
    # -9 -8 -7 -6 [-5 -4 -3 -2 -1] -- -- -- --

    def testBasic(self):

        # Forward

        res = indices(slice(0, 5), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(0, 6), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(0, 7), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(0, 8), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-6, 5), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-6, 6), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 7), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 8), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 9), 5).range()
        exp = range(0, 5)

        self.assertEqual(res, exp)

        # Reverse

        res = indices(slice(4, -6, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(4, -7, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(4, -8, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(4, -9, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(5, -6, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(5, -7, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(6, -8, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(7, -9, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

        res = indices(slice(8, -10, -1), 5).range()
        exp = range(4, -1, -1)

        self.assertEqual(res, exp)

    def testAdvanced(self):

        # Forward

        res = indices(slice(-6, 5, 2), 5).range()
        exp = range(1, 5, 2)

        self.assertEqual(res, exp)

        res = indices(slice(-6, 5, 3), 5).range()
        exp = range(2, 5, 3)

        self.assertEqual(res, exp)

        res = indices(slice(-6, 5, 4), 5).range()
        exp = range(3, 5, 4)

        self.assertEqual(res, exp)

        res = indices(slice(-6, 5, 5), 5).range()
        exp = range(4, 5, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-6, 5, 6), 5).range()
        exp = range(5, 5, 6)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5, 2), 5).range()
        exp = range(0, 5, 2)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5, 3), 5).range()
        exp = range(1, 5, 3)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5, 4), 5).range()
        exp = range(2, 5, 4)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5, 5), 5).range()
        exp = range(3, 5, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5, 6), 5).range()
        exp = range(4, 5, 6)

        self.assertEqual(res, exp)

        res = indices(slice(-7, 5, 7), 5).range()
        exp = range(5, 5, 7)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 2), 5).range()
        exp = range(1, 5, 2)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 3), 5).range()
        exp = range(0, 5, 3)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 4), 5).range()
        exp = range(1, 5, 4)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 5), 5).range()
        exp = range(2, 5, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 6), 5).range()
        exp = range(3, 5, 6)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 7), 5).range()
        exp = range(4, 5, 7)

        self.assertEqual(res, exp)

        res = indices(slice(-8, 5, 8), 5).range()
        exp = range(5, 5, 8)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 2), 5).range()
        exp = range(0, 5, 2)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 3), 5).range()
        exp = range(2, 5, 3)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 4), 5).range()
        exp = range(0, 5, 4)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 5), 5).range()
        exp = range(1, 5, 5)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 6), 5).range()
        exp = range(2, 5, 6)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 7), 5).range()
        exp = range(3, 5, 7)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 8), 5).range()
        exp = range(4, 5, 8)

        self.assertEqual(res, exp)

        res = indices(slice(-9, 5, 9), 5).range()
        exp = range(5, 5, 9)

        self.assertEqual(res, exp)

        # Reverse

        res = indices(slice(5, -6, -2), 5).range()
        exp = range(3, -1, -2)

        self.assertEqual(res, exp)

        res = indices(slice(5, -6, -3), 5).range()
        exp = range(2, -1, -3)

        self.assertEqual(res, exp)

        res = indices(slice(5, -6, -4), 5).range()
        exp = range(1, -1, -4)

        self.assertEqual(res, exp)

        res = indices(slice(5, -6, -5), 5).range()
        exp = range(0, -1, -5)

        self.assertEqual(res, exp)

        res = indices(slice(5, -6, -6), 5).range()
        exp = range(-1, -1, -6)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -2), 5).range()
        exp = range(4, -1, -2)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -3), 5).range()
        exp = range(3, -1, -3)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -4), 5).range()
        exp = range(2, -1, -4)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -5), 5).range()
        exp = range(1, -1, -5)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -6), 5).range()
        exp = range(0, -1, -6)

        self.assertEqual(res, exp)

        res = indices(slice(6, -6, -7), 5).range()
        exp = range(-1, -1, -7)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -2), 5).range()
        exp = range(3, -1, -2)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -3), 5).range()
        exp = range(4, -1, -3)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -4), 5).range()
        exp = range(3, -1, -4)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -5), 5).range()
        exp = range(2, -1, -5)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -6), 5).range()
        exp = range(1, -1, -6)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -7), 5).range()
        exp = range(0, -1, -7)

        self.assertEqual(res, exp)

        res = indices(slice(7, -6, -8), 5).range()
        exp = range(-1, -1, -8)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -2), 5).range()
        exp = range(4, -1, -2)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -3), 5).range()
        exp = range(2, -1, -3)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -4), 5).range()
        exp = range(4, -1, -4)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -5), 5).range()
        exp = range(3, -1, -5)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -6), 5).range()
        exp = range(2, -1, -6)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -7), 5).range()
        exp = range(1, -1, -7)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -8), 5).range()
        exp = range(0, -1, -8)

        self.assertEqual(res, exp)

        res = indices(slice(8, -6, -9), 5).range()
        exp = range(-1, -1, -9)

        self.assertEqual(res, exp)

    def testBad(self):

        # We make no guarantees about the range's indices - all that is
        # guarenteed is that the range will have a length of 0 (done for
        # performance reasons).

        # start = stop, step > 0
        res = len(indices(slice(0, 0, 1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # start = stop, step < 0
        res = len(indices(slice(0, 0, -1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # start > stop, step > 0
        res = len(indices(slice(4, -6, 1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # start < stop, step < 0
        res = len(indices(slice(0, 5, -1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # OK, but start > upper bound, step > 0
        res = len(indices(slice(10, 15 + 1, 1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # OK, but stop > upper bound, step < 0
        res = len(indices(slice(15, 10 - 1, -1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # OK, but stop < lower bound, step > 0
        res = len(indices(slice(-15, -10 - 1, 1), 5).range())
        exp = 0

        self.assertEqual(res, exp)

        # OK, but start < lower bound, step < 0
        res = len(indices(slice(-10, -15 - 1, -1), 5).range())
        exp = 0

        self.assertEqual(res, exp)
