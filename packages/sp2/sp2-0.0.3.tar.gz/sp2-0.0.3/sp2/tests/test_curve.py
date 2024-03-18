import numpy
import unittest
from datetime import datetime, timedelta

import sp2


class TestSp2Curve(unittest.TestCase):
    def test_basic(self):
        def g():
            return sp2.curve(typ=float, data=[(sp2.engine_start_time() + timedelta(i), i) for i in range(10)])

        res = sp2.run(g, starttime=datetime(2020, 1, 1))[0]
        self.assertEqual(len(res), 10)
        self.assertEqual([v[0] for v in res], [datetime(2020, 1, 1) + timedelta(i) for i in range(10)])
        self.assertEqual([v[1] for v in res], list(range(10)))

    def test_timedelta(self):
        def g():
            return sp2.curve(typ=float, data=[(timedelta(i), i) for i in range(10)])

        res = sp2.run(g, starttime=datetime(2020, 1, 1))[0]
        self.assertEqual(len(res), 10)
        self.assertEqual([v[0] for v in res], [datetime(2020, 1, 1) + timedelta(i) for i in range(10)])
        self.assertEqual([v[1] for v in res], list(range(10)))

    def test_numpy(self):
        def g():
            times = numpy.array([sp2.engine_start_time() + timedelta(i) for i in range(10)]).astype(numpy.datetime64)
            values = numpy.array(range(10))
            return sp2.curve(typ=int, data=(times, values))

        res = sp2.run(g, starttime=datetime(2020, 1, 1))[0]
        self.assertEqual(len(res), 10)
        self.assertEqual([v[0] for v in res], [datetime(2020, 1, 1) + timedelta(i) for i in range(10)])
        self.assertEqual([v[1] for v in res], list(range(10)))

    def test_empty_data(self):
        def g1():
            return sp2.curve(typ=int, data=[])

        def g2():
            return sp2.curve(typ=numpy.ndarray, data=[])

        def g3():
            return sp2.curve(typ=str, data=(numpy.array([]), numpy.array([])))

        def g4():
            return sp2.curve(typ=numpy.ndarray, data=(numpy.array([]), numpy.array([])))

        for g in [g1, g2, g3, g4]:
            res = sp2.run(g, starttime=datetime(2020, 1, 1))[0]
            self.assertEqual(len(res), 0)


if __name__ == "__main__":
    unittest.main()
