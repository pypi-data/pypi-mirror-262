import unittest
from datetime import datetime, timedelta

import sp2


class TestPipeApplyRun(unittest.TestCase):
    def test_run(self):
        data = [(datetime(2020, 1, 1), 2), (datetime(2020, 1, 2), 3)]
        out = sp2.curve(int, data).run(starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3))
        self.assertEqual(out, data)

    def test_apply(self):
        inp = sp2.curve(int, [(datetime(2020, 1, 1), 2), (datetime(2020, 1, 2), 3)])
        out = inp.apply(lambda x: x**3).run(starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3))
        target = [(datetime(2020, 1, 1), 8), (datetime(2020, 1, 2), 27)]
        self.assertListEqual(out, target)

        f = lambda x, y: x**y
        out = inp.apply(f, 3).run(starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3))
        self.assertListEqual(out, target)

        out = inp.apply((f, float), y=3.0).run(starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3))
        self.assertListEqual(out, target)

    def test_pipe(self):
        inp = sp2.curve(int, [(datetime(2020, 1, 1), 2), (datetime(2020, 1, 2), 3)])
        out = inp.pipe(sp2.delay, timedelta(1)).run(starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3))
        target = [(datetime(2020, 1, 2), 2), (datetime(2020, 1, 3), 3)]
        self.assertListEqual(out, target)

        out = inp.pipe(sp2.delay, delay=timedelta(1)).run(starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3))
        self.assertListEqual(out, target)

        out = inp.pipe((sp2.sample, "x"), trigger=sp2.timer(timedelta(hours=12))).run(
            starttime=datetime(2020, 1, 1), endtime=datetime(2020, 1, 3)
        )
        target = [
            (datetime(2020, 1, 1, 12), 2),
            (datetime(2020, 1, 2), 3),
            (datetime(2020, 1, 2, 12), 3),
            (datetime(2020, 1, 3), 3),
        ]
        self.assertListEqual(out, target)

    def test_no_bool(self):
        # This was an issue
        with self.assertRaisesRegex(ValueError, "boolean evaluation of an edge is not supported"):
            _ = sp2.const(1) in [1]


if __name__ == "__main__":
    unittest.main()
