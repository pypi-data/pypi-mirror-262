import unittest
from datetime import datetime, timedelta

import sp2


class TestSp2DataFrame(unittest.TestCase):
    def test_basic(self):
        df = sp2.DataFrame()
        df["a"] = sp2.count(sp2.timer(timedelta(seconds=1)))
        df["b"] = sp2.count(sp2.timer(timedelta(seconds=0.5))) * 10

        self.assertEqual(df.columns, ["a", "b"])
        starttime = datetime(2021, 4, 26)
        endtime = starttime + timedelta(minutes=1)
        pd = df.to_pandas(starttime, endtime)
        self.assertEqual(len(pd), 120)

    def test_math_ops(self):
        df = sp2.DataFrame()
        df["a"] = sp2.merge(sp2.count(sp2.timer(timedelta(seconds=1))), sp2.const(1))
        df["b"] = sp2.merge(sp2.count(sp2.timer(timedelta(seconds=0.5))), sp2.const(1))
        df["add"] = df["a"] + df["b"]
        df["sub"] = df["a"] - df["b"]
        df["mul"] = df["a"] * df["b"]
        df["div"] = df["a"] / df["b"]
        df["pow"] = df["a"] ** 2
        df["gt"] = df["a"] > df["b"]
        df["ge"] = df["a"] >= df["b"]
        df["lt"] = df["a"] < df["b"]
        df["le"] = df["a"] <= df["b"]
        df["eq"] = df["a"] == df["b"]
        df["ne"] = df["a"] != df["b"]

        starttime = datetime(2021, 4, 26)
        endtime = starttime + timedelta(minutes=1)
        pd = df.to_pandas(starttime, endtime)

        pd2 = pd[["a", "b"]].ffill()
        self.assertTrue(pd["add"].astype(float).equals(pd2["a"] + pd2["b"]))
        self.assertTrue(pd["sub"].astype(float).equals(pd2["a"] - pd2["b"]))
        self.assertTrue(pd["mul"].astype(float).equals(pd2["a"] * pd2["b"]))
        self.assertTrue(pd["div"].astype(float).equals(pd2["a"] / pd2["b"]))
        self.assertTrue(pd["pow"].astype(float).equals(pd["a"] ** 2))

        self.assertTrue(pd["gt"].equals(pd2["a"] > pd2["b"]))
        self.assertTrue(pd["ge"].equals(pd2["a"] >= pd2["b"]))
        self.assertTrue(pd["lt"].equals(pd2["a"] < pd2["b"]))
        self.assertTrue(pd["le"].equals(pd2["a"] <= pd2["b"]))
        self.assertTrue(pd["eq"].equals(pd2["a"] == pd2["b"]))
        self.assertTrue(pd["ne"].equals(pd2["a"] != pd2["b"]))

        # Test adding two DFs
        df = sp2.DataFrame()
        df2 = sp2.DataFrame()
        df["a"] = sp2.merge(sp2.count(sp2.timer(timedelta(seconds=1))), sp2.const(1))
        df["b"] = sp2.merge(sp2.count(sp2.timer(timedelta(seconds=1))), sp2.const(1))
        df2["b"] = sp2.merge(sp2.count(sp2.timer(timedelta(seconds=1))), sp2.const(1))
        df2["a"] = sp2.merge(sp2.count(sp2.timer(timedelta(seconds=1))), sp2.const(1))

        df3 = df + df2
        expected = df.to_pandas(starttime, endtime) + df2.to_pandas(starttime, endtime)
        pd3 = df3.to_pandas(starttime, endtime)
        self.assertTrue(pd3.equals(expected))

        # Adding df with subset of columns should throw
        df2 = df2[["a"]]
        with self.assertRaisesRegex(ValueError, "Shape mismatch"):
            _ = df + df2

        # Adding constant
        df3 = df + 10
        expected = df.to_pandas(starttime, endtime) + 10
        pd3 = df3.to_pandas(starttime, endtime)
        self.assertTrue(pd3.equals(expected))

        # Adding list of values
        df3 = df + [10, 20]
        expected = df.to_pandas(starttime, endtime) + [10, 20]
        pd3 = df3.to_pandas(starttime, endtime)
        self.assertTrue(pd3.equals(expected))

        # shape mistamtch
        with self.assertRaisesRegex(ValueError, "Shape mismatch"):
            _ = df + [1]

    def test_get_and_set_item(self):
        df = sp2.DataFrame()
        df["a"] = sp2.const(1)
        df["b"] = sp2.const(2)
        df["c"] = sp2.const(3)

        df2 = df[["a", "c"]]
        self.assertEqual(df2.columns, ["a", "c"])
        df2[["g", "h"]] = df2
        self.assertEqual(df2.columns, ["a", "c", "g", "h"])

        starttime = datetime(2021, 4, 26)
        endtime = starttime + timedelta(minutes=1)
        pd = df2.to_pandas(starttime, endtime)
        self.assertEqual(len(pd), 1)
        self.assertEqual(list(pd.columns), df2.columns)

        ## attribute access
        self.assertEqual(id(df["a"]), id(df.a))

    def test_filter(self):
        df = sp2.DataFrame()
        df["a"] = sp2.count(sp2.timer(timedelta(seconds=1)))
        df["b"] = sp2.count(sp2.timer(timedelta(seconds=1))) * 2

        df2 = df[df["b"] <= 10]

        starttime = datetime(2021, 4, 26)
        endtime = starttime + timedelta(seconds=10)
        pd = df.to_pandas(starttime, endtime)
        pd2 = df2.to_pandas(starttime, endtime)
        self.assertEqual(len(pd), 10)
        self.assertEqual(len(pd2), 5)
        self.assertTrue(pd2.equals(pd[pd["b"] <= 10]))

    def test_perspective(self):
        """cant really test all but at least exercise the code"""
        # Test will only run if perspective is in the env
        try:
            import perspective
        except ImportError:
            return

        df = sp2.DataFrame()
        df["a"] = sp2.count(sp2.timer(timedelta(seconds=0.01)))
        df["b"] = sp2.count(sp2.timer(timedelta(seconds=0.01))) * 2

        starttime = datetime(2021, 4, 26)
        endtime = starttime + timedelta(seconds=10)

        _ = df.to_perspective(starttime, endtime)

        # realtime
        widget = df.to_perspective(datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True)
        import time

        time.sleep(1)
        widget.stop()


if __name__ == "__main__":
    unittest.main()
