import functools
import itertools
import logging
import math
import numpy as np
import unittest
from datetime import date, datetime, timedelta, timezone
from enum import Enum, auto

import sp2
from sp2 import ts
from sp2.baselib import _convert_ts_object_for_print
from sp2.impl.struct import defineStruct


class TestBaselib(unittest.TestCase):
    def test_const(self):
        @sp2.graph
        def graph():
            sp2.add_graph_output("i", sp2.const(1))
            sp2.add_graph_output("s", sp2.const("hello world!"))
            sp2.add_graph_output("id", sp2.const(2, delay=timedelta(seconds=1)))

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st)
        self.assertEqual(results["i"], [(st, 1)])
        self.assertEqual(results["s"], [(st, "hello world!")])
        self.assertEqual(results["id"], [(st + timedelta(seconds=1), 2)])

    def test_timer(self):
        @sp2.graph
        def graph():
            sp2.add_graph_output("i", sp2.timer(timedelta(seconds=1), 1))
            sp2.add_graph_output("s", sp2.timer(timedelta(seconds=2), "hello world!"))

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st, endtime=st + timedelta(seconds=10))
        self.assertEqual(results["i"], [(st + timedelta(seconds=x), 1) for x in range(1, 11)])
        self.assertEqual(results["s"], [(st + timedelta(seconds=x * 2), "hello world!") for x in range(1, 6)])

    def test_sample(self):
        x = sp2.count(sp2.timer(timedelta(seconds=1), 1))
        trigger = sp2.timer(timedelta(seconds=0.6), True)

        st = datetime(2020, 1, 1)
        result = sp2.run(sp2.sample, trigger, x, starttime=st, endtime=st + timedelta(seconds=3))[0]
        self.assertEqual(
            result,
            [
                (st + timedelta(seconds=1.2), 1),
                (st + timedelta(seconds=1.8), 1),
                (st + timedelta(seconds=2.4), 2),
                (st + timedelta(seconds=3), 3),
            ],
        )

    def test_firstN(self):
        x = sp2.count(sp2.timer(timedelta(seconds=1), 1))
        firstN = sp2.firstN(x, 5)
        st = datetime(2020, 1, 1)
        result = sp2.run(firstN, starttime=st, endtime=st + timedelta(seconds=30))[0]
        self.assertEqual(result, [(st + timedelta(seconds=x), x) for x in range(1, 6)])

    def test_count(self):
        x = sp2.count(sp2.timer(timedelta(seconds=1), True))
        st = datetime(2020, 1, 1)
        result = sp2.run(x, starttime=st, endtime=st + timedelta(seconds=10))[0]
        self.assertEqual(result, [(st + timedelta(seconds=x), x) for x in range(1, 11)])

    def test_delay(self):
        @sp2.graph
        def graph():
            # data slower than delay
            x = sp2.count(sp2.timer(timedelta(seconds=2), True))
            # data rate faster than delay
            y = sp2.count(sp2.timer(timedelta(seconds=0.5), True))

            sp2.add_graph_output("x", sp2.delay(x, timedelta(seconds=1)))
            sp2.add_graph_output("y", sp2.delay(y, timedelta(seconds=1)))
            sp2.add_graph_output("z", sp2.delay(y, 3))

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st, endtime=st + timedelta(seconds=10))
        self.assertEqual(results["x"], [(st + timedelta(seconds=3 + 2 * x), x + 1) for x in range(0, 4)])
        self.assertEqual(results["y"], [(st + timedelta(seconds=1.5 + 0.5 * x), x + 1) for x in range(0, 18)])
        self.assertEqual(results["z"], [(st + timedelta(seconds=2 + 0.5 * x), x + 1) for x in range(0, 17)])

    def test_delay_irregular_spacing(self):
        st = datetime(2020, 1, 3)

        @sp2.graph
        def graph():
            x = sp2.curve(float, [(st + timedelta(seconds=x), y) for x, y in {0: 1, 7: 2, 12: 3, 15: 4}.items()])

            dtime = sp2.delay(x, timedelta(seconds=2))  # [2:1, 9:2, 14:3, 17:4]
            dtick = sp2.delay(x, 2)  # [12:1, 15:2]

            sp2.add_graph_output("dtime", dtime)
            sp2.add_graph_output("dtick", dtick)

        results = sp2.run(graph, starttime=st, endtime=st + timedelta(seconds=20))
        self.assertEqual(
            results["dtime"], [(st + timedelta(seconds=x), y) for x, y in {2: 1, 9: 2, 14: 3, 17: 4}.items()]
        )
        self.assertEqual(results["dtick"], [(st + timedelta(seconds=x), y) for x, y in {12: 1, 15: 2}.items()])

    def test_lag(self):
        @sp2.graph
        def graph():
            x = sp2.curve(
                typ=int,
                data=[
                    # spacing so in one case with timedelta lag, the lag skips over a tick (doesn't always give prior tick)
                    (datetime(2000, 1, 1), 2),
                    (datetime(2000, 1, 4), 5),
                    (datetime(2000, 1, 5), 12),
                    (datetime(2000, 1, 9), 23),
                ],
            )
            lagged_dt = sp2.baselib._lag(x, timedelta(days=2))
            lagged_n = sp2.baselib._lag(x, 2)
            sp2.add_graph_output("lagged_dt", lagged_dt)
            sp2.add_graph_output("lagged_n", lagged_n)

        results = sp2.run(graph, starttime=datetime(2000, 1, 1), endtime=datetime(2000, 1, 15))
        self.assertEqual(
            results["lagged_dt"], [(datetime(2000, 1, 4), 2), (datetime(2000, 1, 5), 2), (datetime(2000, 1, 9), 12)]
        )
        self.assertEqual(results["lagged_n"], [(datetime(2000, 1, 5), 2), (datetime(2000, 1, 9), 5)])

    def test_diff(self):
        @sp2.graph
        def graph():
            x = sp2.curve(
                typ=int,
                data=[
                    # spacing so in one case with timedelta lag, the lag skips over a tick (doesn't always give prior tick)
                    (datetime(2000, 1, 1), 2),
                    (datetime(2000, 1, 4), 5),
                    (datetime(2000, 1, 5), 12),
                    (datetime(2000, 1, 9), 23),
                ],
            )
            diff_dt = sp2.diff(x, timedelta(days=2))
            diff_n = sp2.diff(x, 2)
            sp2.add_graph_output("diff_dt", diff_dt)
            sp2.add_graph_output("diff_n", diff_n)

        results = sp2.run(graph, starttime=datetime(2000, 1, 1), endtime=datetime(2000, 1, 15))
        self.assertEqual(
            results["diff_dt"], [(datetime(2000, 1, 4), 3), (datetime(2000, 1, 5), 10), (datetime(2000, 1, 9), 11)]
        )
        self.assertEqual(results["diff_n"], [(datetime(2000, 1, 5), 10), (datetime(2000, 1, 9), 18)])

    def test_merge(self):
        x = sp2.curve(int, [(timedelta(seconds=v * 2), v * 100) for v in range(1, 6)])
        y = sp2.curve(int, [(timedelta(seconds=v), v) for v in range(1, 6)])
        st = datetime(2020, 1, 1)
        td = timedelta(seconds=1)
        results = sp2.run(sp2.merge, x, y, starttime=st)[0]
        self.assertEqual(
            results,
            [
                (st + td, 1),
                (st + td * 2, 100),
                (st + td * 3, 3),
                (st + td * 4, 200),
                (st + td * 5, 5),
                (st + td * 6, 300),
                (st + td * 8, 400),
                (st + td * 10, 500),
            ],
        )

        results = sp2.run(sp2.merge, y, x, starttime=st)[0]
        self.assertEqual(
            results,
            [
                (st + td, 1),
                (st + td * 2, 2),
                (st + td * 3, 3),
                (st + td * 4, 4),
                (st + td * 5, 5),
                (st + td * 6, 300),
                (st + td * 8, 400),
                (st + td * 10, 500),
            ],
        )

    def test_split(self):
        x = sp2.timer(timedelta(seconds=1), 1)
        flag = sp2.curve(bool, [(timedelta(), True), (timedelta(seconds=4.5), False)])

        st = datetime(2020, 1, 1)
        td = timedelta(seconds=1)
        results = sp2.run(sp2.split, flag, x, starttime=st, endtime=st + timedelta(seconds=10))
        self.assertEqual(results["true"], [(st + td * x, 1) for x in range(1, 5)])
        self.assertEqual(results["false"], [(st + td * x, 1) for x in range(5, 11)])

    def test_filter(self):
        x = sp2.timer(timedelta(seconds=1), 1)
        flag = sp2.curve(bool, [(timedelta(), True), (timedelta(seconds=4.5), False)])

        st = datetime(2020, 1, 1)
        td = timedelta(seconds=1)
        results = sp2.run(sp2.filter, flag, x, starttime=st, endtime=st + timedelta(seconds=10))[0]
        self.assertEqual(results, [(st + td * x, 1) for x in range(1, 5)])

    def test_unroll(self):
        st = datetime(2020, 1, 1)
        td = timedelta(seconds=1)
        x = sp2.curve(
            [int],
            [
                (st, [1]),
                (st + td * 1, [2, 3, 4]),
                (st + td * 2, [5]),
                (st + td * 3, []),
                (st + td * 4, [6, 7, 8, 9, 10]),
            ],
        )
        x2 = sp2.curve(
            [[int]],
            [
                (st, [[1]]),
                (st + td * 1, [[2, 3, 4]]),
                (st + td * 2, [[5]]),
                (st + td * 3, [[]]),
                (st + td * 4, [[6, 7, 8, 9, 10]]),
            ],
        )
        results = sp2.run(sp2.unroll, x, starttime=st)[0]
        self.assertEqual([x[1] for x in results], list(range(1, 11)))
        results2 = sp2.run(sp2.unroll, x2, starttime=st)
        lists2 = list(zip(*results2[0]))[1]
        self.assertEqual(len(lists2), 5)
        self.assertEqual(list(itertools.chain(*lists2)), list(range(1, 11)))

    def test_collect(self):
        x0 = sp2.timer(timedelta(seconds=1), 0)
        x1 = sp2.timer(timedelta(seconds=1.5), 1)
        x2 = sp2.timer(timedelta(seconds=2), 2)

        st = datetime(2020, 1, 1)
        results = sp2.run(sp2.collect, [x0, x1, x2], starttime=st, endtime=st + timedelta(seconds=6))[0]
        self.assertEqual(
            results,
            [
                (st + timedelta(seconds=1), [0]),
                (st + timedelta(seconds=1.5), [1]),
                (st + timedelta(seconds=2), [2, 0]),
                (st + timedelta(seconds=3), [1, 0]),
                (st + timedelta(seconds=4), [2, 0]),
                (st + timedelta(seconds=4.5), [1]),
                (st + timedelta(seconds=5), [0]),
                (st + timedelta(seconds=6), [2, 1, 0]),
            ],
        )

    def test_flatten(self):
        x0 = sp2.timer(timedelta(seconds=1), 0)
        x1 = sp2.timer(timedelta(seconds=1.5), 1)
        x2 = sp2.timer(timedelta(seconds=2), 2)

        st = datetime(2020, 1, 1)
        results = sp2.run(sp2.flatten, [x0, x1, x2], starttime=st, endtime=st + timedelta(seconds=6.1))[0]
        self.assertEqual([x[1] for x in results], [0, 1, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1, 0])

    def test_flatten_single_optimization(self):
        x0 = sp2.timer(timedelta(seconds=1), 0)
        st = datetime(2020, 1, 1)
        g = sp2.flatten([x0])

        # assert that the flatten did not wrap the timer in a collect/unroll
        assert isinstance(g.nodedef, sp2.baselib._timer)

    def test_default(self):
        @sp2.graph
        def g():
            # 123 should win
            sp2.add_graph_output("c1", sp2.default(sp2.const(123), 456))
            # 456 should win
            sp2.add_graph_output("c2", sp2.default(sp2.const(123, delay=timedelta(seconds=1)), 456))
            # 456 should win
            sp2.add_graph_output(
                "c3", sp2.default(sp2.const(123, delay=timedelta(seconds=1)), 456, delay=timedelta(seconds=0.5))
            )
            # 123 should win, 456 should not tick
            sp2.add_graph_output(
                "c4", sp2.default(sp2.const(123, delay=timedelta(seconds=1)), 456, delay=timedelta(seconds=2))
            )

        results = sp2.run(g, starttime=datetime(2020, 8, 11))
        self.assertEqual([v[1] for v in results["c1"]], [123])
        self.assertEqual([v[1] for v in results["c2"]], [456, 123])
        self.assertEqual([v[1] for v in results["c3"]], [456, 123])
        self.assertEqual([v[1] for v in results["c4"]], [123])
        pass

    def test_stop_engine(self):
        def graph():
            x = sp2.timer(timedelta(seconds=1))
            stop = sp2.const(True, delay=timedelta(seconds=5))

            sp2.stop_engine(stop)
            return x

        results = sp2.run(graph, starttime=datetime(2020, 5, 19))[0]
        self.assertEqual(len(results), 5)

    def test_accum(self):
        x = sp2.count(sp2.timer(timedelta(seconds=1), True))

        st = datetime(2020, 1, 1)
        result = sp2.run(sp2.accum, x, starttime=st, endtime=st + timedelta(seconds=10))[0]

        self.assertEqual([x[1] for x in result], [sum(range(1, 2 + n)) for n in range(10)])

    def test_exprtk(self):
        start_time = datetime(2020, 1, 3)
        end_time = start_time + timedelta(seconds=6)
        x = sp2.curve(float, [(start_time + timedelta(seconds=i), i) for i in range(5)])  # 0 1 2  3 4
        y = sp2.curve(float, [(start_time + timedelta(seconds=i), 10 * i) for i in range(0, 5, 2)])  # 0 . 20 . 40
        s = sp2.curve(str, [(start_time, "+"), (start_time + timedelta(seconds=2), "*")])  # + . *  . .
        n = sp2.curve(
            np.ndarray,
            data=[(start_time + timedelta(seconds=i), np.array([1, i, 7 + i], dtype=float)) for i in range(5)],
        )
        n2 = sp2.curve(
            np.ndarray,
            data=[(start_time + timedelta(seconds=i), np.array([-2, i, i * i], dtype=float)) for i in [1, 3, 6]],
        )

        # basic
        results = sp2.run(sp2.exprtk("x+y", {"x": x, "y": y}), starttime=start_time, endtime=end_time)
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in range(5)], [0, 1, 22, 23, 44]))
        )

        # string input
        results = sp2.run(
            sp2.exprtk("if (s == '+') x + y; else if (s == '*') x * y;", {"x": x, "y": y, "s": s}),
            starttime=start_time,
            endtime=end_time,
        )
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in range(5)], [0, 1, 40, 60, 160]))
        )

        # state
        results = sp2.run(sp2.exprtk("FOO := FOO + x", {"x": x}, {"FOO": 100}), starttime=start_time, endtime=end_time)
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in range(5)], [100, 101, 103, 106, 110]))
        )

        # sp2.now()
        results = sp2.run(sp2.exprtk("y + sp2.now()", {"y": y}), starttime=start_time, endtime=end_time)
        self.assertEqual(
            results[0],
            list(
                zip([start_time + timedelta(seconds=i) for i in range(0, 5, 2)], [1578009600, 1578009622, 1578009644])
            ),
        )

        # trigger
        results = sp2.run(sp2.exprtk("x", {"x": x}, trigger=y), starttime=start_time, endtime=end_time)
        self.assertEqual(results[0], list(zip([start_time + timedelta(seconds=i) for i in range(0, 5, 2)], [0, 2, 4])))

        # numpy array
        results = sp2.run(sp2.exprtk("sum(2 * n)", {"n": n}), starttime=start_time, endtime=end_time)
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in range(5)], [16, 20, 24, 28, 32]))
        )

        # numpy array mixed with scalar float
        results = sp2.run(sp2.exprtk("y * max(n) + sum(n)", {"y": y, "n": n2}), starttime=start_time, endtime=end_time)
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in [1, 2, 3, 4, 6]], [0, 20, 190, 370, 1480]))
        )

        # function
        results = sp2.run(
            sp2.exprtk(
                "2 * foo(x) + bar(x,y)",
                {"x": x, "y": y},
                functions={"foo": (("x",), "x*x"), "bar": (("x", "y"), "x*y")},
            ),
            starttime=start_time,
            endtime=end_time,
        )
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in range(5)], [0, 2, 48, 78, 192]))
        )

        # ndarray output
        results = sp2.run(
            sp2.exprtk("return [x, x*x, 10*x]", {"x": x}, output_ndarray=True), starttime=start_time, endtime=end_time
        )
        expected = list(
            zip(
                [start_time + timedelta(seconds=i) for i in range(5)],
                [
                    np.array([0.0, 0.0, 0.0]),
                    np.array([1.0, 1.0, 10.0]),
                    np.array([2.0, 4.0, 20.0]),
                    np.array([3.0, 9.0, 30.0]),
                    np.array([4.0, 16.0, 40.0]),
                ],
            )
        )
        np.testing.assert_equal(results[0], expected)

        # constants
        results = sp2.run(sp2.exprtk("x * c", {"x": x}, constants={"c": 77}), starttime=start_time, endtime=end_time)
        self.assertEqual(
            results[0], list(zip([start_time + timedelta(seconds=i) for i in range(5)], [0, 77, 154, 231, 308]))
        )

    def test_multiplex_decode(self):
        class Trade(sp2.Struct):
            price: float
            size: int
            account: str
            symbol: str

        class IntTrade(sp2.Struct):
            price: float
            size: int
            account: int
            symbol: str

        accounts = ["TEST1", "TEST2", "TEST3"]
        invalid_accounts = ["INVALID1", "INVALID2", "INVALID3"]
        int_accounts = [0, 1, 2]

        st = datetime(2020, 1, 1)

        trade_list_1 = [
            (st + timedelta(seconds=1), Trade(price=100.0, size=50, account="TEST1", symbol="AAPL")),
            (st + timedelta(seconds=6), Trade(price=101.4, size=500, account="TEST1", symbol="IBM")),
        ]

        trade_list_2 = [
            (st + timedelta(seconds=2), Trade(price=101.5, size=500, account="TEST2", symbol="AAPL")),
            (st + timedelta(seconds=5), Trade(price=101.3, size=500, account="TEST2", symbol="IBM")),
        ]

        trade_list_3 = [
            (st + timedelta(seconds=3), Trade(price=100.50, size=100, account="TEST3", symbol="AAPL")),
            (st + timedelta(seconds=4), Trade(price=101.2, size=500, account="TEST3", symbol="IBM")),
        ]

        int_trade_list_1 = [
            (st + timedelta(seconds=1), IntTrade(price=100.0, size=50, account=0, symbol="AAPL")),
            (st + timedelta(seconds=6), IntTrade(price=101.4, size=500, account=0, symbol="IBM")),
        ]

        int_trade_list_2 = [
            (st + timedelta(seconds=2), IntTrade(price=101.5, size=500, account=1, symbol="AAPL")),
            (st + timedelta(seconds=5), IntTrade(price=101.3, size=500, account=1, symbol="IBM")),
        ]

        int_trade_list_3 = [
            (st + timedelta(seconds=3), IntTrade(price=100.50, size=100, account=2, symbol="AAPL")),
            (st + timedelta(seconds=4), IntTrade(price=101.2, size=500, account=2, symbol="IBM")),
        ]

        account_list = [
            (st + timedelta(seconds=1), "TEST1"),
            (st + timedelta(seconds=2), "TEST2"),
            (st + timedelta(seconds=3), "TEST3"),
            (st + timedelta(seconds=4), "TEST3"),
            (st + timedelta(seconds=5), "TEST2"),
            (st + timedelta(seconds=6), "TEST1"),
        ]

        account_list_tick_early = [
            (st + timedelta(seconds=0.9), "TEST1"),
            (st + timedelta(seconds=1.9), "TEST2"),
            (st + timedelta(seconds=2.9), "TEST3"),
            (st + timedelta(seconds=3.9), "TEST3"),
            (st + timedelta(seconds=4.9), "TEST2"),
            (st + timedelta(seconds=5.9), "TEST1"),
        ]

        invalid_account_list = [
            (st + timedelta(seconds=1), "INVALID1"),
            (st + timedelta(seconds=2), "INVALID2"),
            (st + timedelta(seconds=3), "INVALID3"),
            (st + timedelta(seconds=4), "INVALID3"),
            (st + timedelta(seconds=5), "INVALID2"),
            (st + timedelta(seconds=6), "INVALID1"),
        ]

        int_account_list = [
            (st + timedelta(seconds=1), 0),
            (st + timedelta(seconds=2), 1),
            (st + timedelta(seconds=3), 2),
            (st + timedelta(seconds=4), 2),
            (st + timedelta(seconds=5), 1),
            (st + timedelta(seconds=6), 0),
        ]

        invalid_int_account_list = [
            (st + timedelta(seconds=1), 4),
            (st + timedelta(seconds=2), 5),
            (st + timedelta(seconds=3), 6),
            (st + timedelta(seconds=4), 6),
            (st + timedelta(seconds=5), 5),
            (st + timedelta(seconds=6), 4),
        ]

        trade_list = [
            (st + timedelta(seconds=1), Trade(price=100.0, size=50, account="TEST1", symbol="AAPL")),
            (st + timedelta(seconds=2), Trade(price=101.5, size=500, account="TEST2", symbol="AAPL")),
            (st + timedelta(seconds=3), Trade(price=100.50, size=100, account="TEST3", symbol="AAPL")),
            (st + timedelta(seconds=4), Trade(price=101.2, size=500, account="TEST3", symbol="IBM")),
            (st + timedelta(seconds=5), Trade(price=101.3, size=500, account="TEST2", symbol="IBM")),
            (st + timedelta(seconds=6), Trade(price=101.4, size=500, account="TEST1", symbol="IBM")),
        ]

        trade_list_tick_early = [
            (st + timedelta(seconds=1), Trade(price=100.0, size=50, account="TEST1", symbol="AAPL")),
            (st + timedelta(seconds=2), Trade(price=101.5, size=500, account="TEST2", symbol="AAPL")),
            (st + timedelta(seconds=3), Trade(price=100.50, size=100, account="TEST3", symbol="AAPL")),
            (
                st + timedelta(seconds=3.9),
                Trade(price=100.50, size=100, account="TEST3", symbol="AAPL"),
            ),  # last tick on test3
            (st + timedelta(seconds=4), Trade(price=101.2, size=500, account="TEST3", symbol="IBM")),
            (
                st + timedelta(seconds=4.9),
                Trade(price=101.5, size=500, account="TEST2", symbol="AAPL"),
            ),  # last tick on test2
            (st + timedelta(seconds=5), Trade(price=101.3, size=500, account="TEST2", symbol="IBM")),
            (
                st + timedelta(seconds=5.9),
                Trade(price=100, size=50, account="TEST1", symbol="AAPL"),
            ),  # last tick on test2
            (st + timedelta(seconds=6), Trade(price=101.4, size=500, account="TEST1", symbol="IBM")),
        ]

        int_trade_list = [
            (st + timedelta(seconds=1), IntTrade(price=100.0, size=50, account=0, symbol="AAPL")),
            (st + timedelta(seconds=2), IntTrade(price=101.5, size=500, account=1, symbol="AAPL")),
            (st + timedelta(seconds=3), IntTrade(price=100.50, size=100, account=2, symbol="AAPL")),
            (st + timedelta(seconds=4), IntTrade(price=101.2, size=500, account=2, symbol="IBM")),
            (st + timedelta(seconds=5), IntTrade(price=101.3, size=500, account=1, symbol="IBM")),
            (st + timedelta(seconds=6), IntTrade(price=101.4, size=500, account=0, symbol="IBM")),
        ]

        class TestType(Enum):
            Standard = auto()
            TickOnIndex = auto()
            InvalidKeys = auto()
            LateKeyTick = auto()

        def multiplex_graph(test_type=TestType.Standard):
            trades1 = sp2.curve(Trade, trade_list_1)
            trades2 = sp2.curve(Trade, trade_list_2)
            trades3 = sp2.curve(Trade, trade_list_3)
            str_basket = {"TEST1": trades1, "TEST2": trades2, "TEST3": trades3}

            if test_type == TestType.InvalidKeys:
                invalid_accounts = sp2.curve(str, invalid_account_list)
                str_multiplexed = sp2.multiplex(str_basket, invalid_accounts, raise_on_bad_key=True)
            elif test_type == TestType.LateKeyTick:
                accounts = sp2.curve(str, account_list[1:])
                str_multiplexed = sp2.multiplex(str_basket, accounts, raise_on_bad_key=True)
            elif test_type == TestType.TickOnIndex:
                accounts = sp2.curve(str, account_list_tick_early)
                str_multiplexed = sp2.multiplex(str_basket, accounts, tick_on_index=True, raise_on_bad_key=True)
            else:
                accounts = sp2.curve(str, account_list_tick_early)
                str_multiplexed = sp2.multiplex(str_basket, accounts, raise_on_bad_key=True)

            sp2.add_graph_output("multiplexed", str_multiplexed)

            int_trades1 = sp2.curve(IntTrade, int_trade_list_1)
            int_trades2 = sp2.curve(IntTrade, int_trade_list_2)
            int_trades3 = sp2.curve(IntTrade, int_trade_list_3)
            int_accounts = sp2.curve(int, int_account_list)

            int_basket = {0: int_trades1, 1: int_trades2, 2: int_trades3}
            int_multiplexed = sp2.multiplex(int_basket, int_accounts)

            sp2.add_graph_output("int_multiplexed", int_multiplexed)

        results = sp2.run(multiplex_graph, TestType.Standard, starttime=st)
        self.assertEqual(results["multiplexed"], trade_list)
        self.assertEqual(results["int_multiplexed"], int_trade_list)

        try:
            sp2.run(multiplex_graph, TestType.InvalidKeys, starttime=st)
            self.assertFalse(True)
        except Exception as e:
            self.assertIsInstance(e, ValueError)

        results = sp2.run(multiplex_graph, TestType.LateKeyTick, starttime=st)
        self.assertEqual(results["multiplexed"], trade_list[1:])
        self.assertEqual(results["int_multiplexed"], int_trade_list)

        results = sp2.run(multiplex_graph, TestType.TickOnIndex, starttime=st)
        self.assertEqual(results["multiplexed"], trade_list_tick_early)
        self.assertEqual(results["int_multiplexed"], int_trade_list)

        def decode_graph(test_type=TestType.Standard):
            trades = sp2.curve(Trade, trade_list)
            if test_type == TestType.InvalidKeys:
                account = sp2.curve(str, invalid_account_list)  # test invalid keys
            elif test_type == TestType.LateKeyTick:
                account = sp2.curve(
                    str, account_list[1:]
                )  # test correct keys, but first trade ticks before first key ticks
            else:
                self.assertEqual(test_type, TestType.Standard)
                account = trades.account

            decoded = sp2.demultiplex(trades, account, accounts, raise_on_bad_key=True)
            for account in accounts:
                sp2.add_graph_output(account, decoded[account])

            int_trades = sp2.curve(IntTrade, int_trade_list)
            if test_type == TestType.InvalidKeys:
                account = sp2.curve(int, invalid_int_account_list)
            elif test_type == TestType.LateKeyTick:
                account = sp2.curve(int, int_account_list[1:])
            else:
                account = int_trades.account

            int_decoded = sp2.demultiplex(int_trades, account, int_accounts)
            for account in int_accounts:
                sp2.add_graph_output(account, int_decoded[account])

        results = sp2.run(decode_graph, TestType.Standard, starttime=st)
        self.assertEqual(results["TEST1"], trade_list_1)
        self.assertEqual(results["TEST2"], trade_list_2)
        self.assertEqual(results["TEST3"], trade_list_3)
        self.assertEqual(results[0], int_trade_list_1)
        self.assertEqual(results[1], int_trade_list_2)
        self.assertEqual(results[2], int_trade_list_3)

        try:
            sp2.run(decode_graph, TestType.InvalidKeys, starttime=st)
            self.assertFalse(True)
        except Exception as e:
            self.assertIsInstance(e, ValueError)

        results = sp2.run(decode_graph, TestType.LateKeyTick, starttime=st)
        self.assertEqual(results["TEST1"], trade_list_1[1:])
        self.assertEqual(results["TEST2"], trade_list_2)
        self.assertEqual(results["TEST3"], trade_list_3)
        self.assertEqual(results[0], int_trade_list_1[1:])
        self.assertEqual(results[1], int_trade_list_2)
        self.assertEqual(results[2], int_trade_list_3)

    def test_delayed_demultiplex(self):
        class MyStruct(sp2.Struct):
            key: str
            value: int

        @sp2.graph
        def my_graph():
            ticks = [MyStruct(key=chr(ord("A") + i % 5), value=i) for i in range(1000)]
            ticks = sp2.unroll(sp2.const.using(T=[MyStruct])(ticks))
            demux = sp2.DelayedDemultiplex(ticks, ticks.key, raise_on_bad_key=False)

            sp2.add_graph_output("A", demux.demultiplex("A"))
            sp2.add_graph_output("C", demux.demultiplex("C"))
            sp2.add_graph_output("D", demux.demultiplex("D"))

        rv = sp2.run(my_graph, starttime=datetime(2020, 11, 3))
        for k in "ACD":
            self.assertGreater(len(rv[k]), 1)
            self.assertTrue(all(v[1].key == k for v in rv[k]))

        # Test type checking
        def my_graph2():
            demux = sp2.DelayedDemultiplex(sp2.const(MyStruct()), sp2.const("test"))
            demux.demultiplex(123)

        with self.assertRaisesRegex(TypeError, "Conflicting type resolution for K when calling to _demultiplex"):
            sp2.run(my_graph2, starttime=datetime.utcnow())

    def test_delayed_collect(self):
        def g():
            collect = sp2.DelayedCollect(int)
            for i in range(20):
                collect.add_input(sp2.const(i, delay=timedelta(seconds=i)))

            return collect.output()

        res = sp2.run(g, starttime=datetime(2022, 1, 21))[0]
        self.assertEqual(len(res), 20)
        self.assertTrue(all(res[i][1][0] == i for i in range(20)))

    def test_convert_ts_object_for_print(self):
        @sp2.graph
        def aux() -> sp2.Outputs(a=sp2.ts[int], b=sp2.ts[int]):
            return sp2.output(a=sp2.const(1), b=sp2.const(2))

        @sp2.graph
        def g() -> sp2.ts[str]:
            return _convert_ts_object_for_print(aux())

        res = sp2.run(g, starttime=datetime(2022, 1, 21))
        self.assertEqual(res[0], [(datetime(2022, 1, 21, 0, 0), "{'a': 1, 'b': 2}")])

    def test_print_node(self):
        @sp2.graph
        def g() -> sp2.ts[int]:
            ret = sp2.print("x", sp2.const(5))

        sp2.run(g, starttime=datetime(2022, 1, 21))

    def test_times(self):
        times_list = [
            datetime(2020, 1, 1),
            datetime(2020, 1, 1) + timedelta(microseconds=1),
            datetime(2020, 1, 1) + timedelta(seconds=2),
        ]

        @sp2.graph
        def g() -> sp2.Outputs(times=sp2.ts[datetime], times_f=sp2.ts[int]):
            x = sp2.curve(typ=bool, data=[(times_list[i], True) for i in range(3)])

            t = sp2.times(x)
            t_f = sp2.times_ns(x)
            return sp2.output(times=t, times_f=t_f)

        res = sp2.run(g, starttime=datetime(2020, 1, 1))

        timestamps = []
        for i in range(3):
            timestamps.append(list(res["times_f"][i]))
            timestamps[-1][1] /= 1e9
            timestamps[i] = tuple(timestamps[i])

        self.assertEqual(res["times"], [(times_list[i], times_list[i]) for i in range(3)])
        self.assertEqual(
            timestamps, [(times_list[i], times_list[i].replace(tzinfo=timezone.utc).timestamp()) for i in range(3)]
        )

    def test_gate(self):
        @sp2.node
        def validate(x: ts[object], gate: ts[bool]):
            if sp2.ticked(x):
                self.assertTrue(gate)

        @sp2.graph
        def g():
            x = sp2.count(sp2.timer(timedelta(seconds=1)))
            gate = sp2.flatten(
                [
                    sp2.const(True, delay=timedelta(seconds=2)),
                    sp2.delay(sp2.timer(timedelta(seconds=4), True), delay=timedelta(seconds=2)),
                    sp2.timer(timedelta(seconds=4), False),
                ]
            )
            gated_x = sp2.gate(x, gate)
            validate(gated_x, gate)
            sp2.add_graph_output("gate", gated_x)

        res = sp2.run(g, starttime=datetime(2022, 5, 13), endtime=timedelta(seconds=20))["gate"]
        all_values = functools.reduce(lambda x, y: x + y, [v[1] for v in res])

        p = 0
        for x in all_values:
            self.assertEqual(x, p + 1)
            p = x

    def test_drop_dups(self):
        @sp2.graph
        def g(d1: list, d2: list, d3: list, d4: list, d5: list):
            d1 = sp2.unroll(sp2.const.using(T=[int])(d1))
            d2 = sp2.unroll(sp2.const.using(T=[tuple])(d2))
            d3 = sp2.unroll(sp2.const.using(T=[float])(d3))
            d4 = sp2.unroll(sp2.const.using(T=[float])(d4))
            d5 = sp2.unroll(sp2.const.using(T=[float])(d5))

            sp2.add_graph_output("d1", sp2.drop_dups(d1))
            sp2.add_graph_output("d2", sp2.drop_dups(d2))
            sp2.add_graph_output("d3", sp2.drop_dups(d3))
            sp2.add_graph_output("d4", sp2.drop_dups(d4, eps=1e-1))
            sp2.add_graph_output("d5", sp2.drop_dups(d5, eps=1e-7))

        eps = {"d4": 1e-1, "d5": 1e-7}
        nan = float("nan")
        d1 = [1, 2, 3, 3, 4, 3, 5, 5]
        d2 = [(1, 2), (1, 2), (3, 4)]
        d3 = [1.0, 2.0, 3.0, 3.0, nan, 4.0, nan, nan, nan, 5, 0.3 - 0.2, 0.1]
        d4 = [0.1, 0.19, 0.5, nan]
        d5 = [0.3 - 0.2, 0.1, 0.09999999999999, nan, 0.2]
        res = sp2.run(g, d1, d2, d3, d4, d5, starttime=datetime(2022, 5, 13))

        for k, tseries in res.items():
            prev = None
            for v in tseries:
                if prev and isinstance(v[1], float) and isinstance(prev[1], float):
                    self.assertTrue(math.isnan(v[1]) != math.isnan(prev[1]) or abs(v[1] - prev[1]) > eps.get(k, 1e-12))
                else:
                    self.assertNotEqual(v, prev)
                prev = v

    def test_struct_fromts(self):
        class S(sp2.Struct):
            a: bool
            b: float
            c: str

        def g():
            a = sp2.curve(bool, [(timedelta(), False), (timedelta(seconds=1), True)])
            b = sp2.curve(float, [(timedelta(seconds=0.2), 123.0), (timedelta(seconds=1), 456.0)])
            c = sp2.curve(str, [(timedelta(seconds=0.4), "hey"), (timedelta(seconds=1.1), "yo")])

            trigger = sp2.timer(timedelta(seconds=1), True)
            sp2.add_graph_output("fromts", S.fromts(a=a, b=b, c=c))
            sp2.add_graph_output("fromts_trigger", S.fromts(trigger, a=a, b=b, c=c))

        res = sp2.run(g, starttime=datetime(2022, 8, 1), endtime=timedelta(seconds=2))
        fromts = res["fromts"]
        fromts_trigger = res["fromts_trigger"]
        self.assertEqual(len(fromts), 5)
        self.assertEqual(
            [x[1] for x in fromts],
            [
                S(a=False),
                S(a=False, b=123.0),
                S(a=False, b=123.0, c="hey"),
                S(a=True, b=456.0, c="hey"),
                S(a=True, b=456.0, c="yo"),
            ],
        )
        self.assertEqual(len(fromts_trigger), 2)
        self.assertEqual([x[1] for x in fromts_trigger], [S(a=True, b=456.0, c="hey"), S(a=True, b=456.0, c="yo")])

    def test_struct_collectts(self):
        class S(sp2.Struct):
            a: bool
            b: float
            c: str

        def g():
            a = sp2.curve(bool, [(timedelta(), False), (timedelta(seconds=1), True)])
            b = sp2.curve(float, [(timedelta(seconds=0.2), 123.0), (timedelta(seconds=1), 456.0)])
            c = sp2.curve(str, [(timedelta(seconds=0.4), "hey"), (timedelta(seconds=1.1), "yo")])

            trigger = sp2.timer(timedelta(seconds=1), True)
            sp2.add_graph_output("collectts", S.collectts(a=a, b=b, c=c))

        res = sp2.run(g, starttime=datetime(2022, 8, 1), endtime=timedelta(seconds=2))
        collectts = res["collectts"]
        self.assertEqual(len(collectts), 5)
        self.assertEqual([x[1] for x in collectts], [S(a=False), S(b=123.0), S(c="hey"), S(a=True, b=456.0), S(c="yo")])

    def test_cppimpls(self):
        import random
        import time

        class MyEnum(sp2.Enum):
            A = 0
            B = 1
            C = 2
            D = 3
            E = 4

        class MyStruct(sp2.Struct):
            value: float

        class MyObject:
            def __init__(self):
                self.value = None

            def __eq__(self, rhs):
                return self.value == rhs.value

        # multiple field types to test struct_field
        class MyStruct2(sp2.Struct):
            b: bool
            i: int
            f: float
            s: str
            d: datetime
            t: timedelta
            dt: date
            e: MyEnum
            st: MyStruct
            o: MyObject
            l: [int]

        @sp2.node
        def random_gen(trigger: ts[object], typ: "T") -> ts["T"]:
            if sp2.ticked(trigger):
                v = 1000 * random.random()
                if typ is MyStruct:
                    return MyStruct(value=v)
                if typ is MyObject:
                    obj = MyObject()
                    obj.value = v
                    return obj
                if typ is bool:
                    return v < 500
                if typ is datetime:
                    return datetime.fromtimestamp(v * 1e6)
                if typ is timedelta:
                    return timedelta(seconds=v)
                if typ is date:
                    return date.today() + timedelta(days=v)
                if typ is MyEnum:
                    return MyEnum(int(v) % 5)
                if isinstance(typ, list):
                    return [int(v), int(v * 2)]
                return typ(v)

        @sp2.node
        def random_gen_nan(trigger: ts[object]) -> ts[float]:
            if sp2.ticked(trigger):
                if random.random() < 0.2:
                    return float("nan")
                return 1000 * random.random()

        @sp2.node
        def random_delay(x: ts["T"]) -> ts["T"]:
            with sp2.alarms():
                tick = sp2.alarm("T")

            if sp2.ticked(x):
                delay = timedelta(seconds=round(random.random(), 1))
                sp2.schedule_alarm(tick, delay, x)

            if sp2.ticked(tick):
                return tick

        @sp2.node
        def accum_list(x: ts["T"]) -> ts[["T"]]:
            with sp2.state():
                s_nextcount = 1
                s_accum = []

            if sp2.ticked(x):
                s_accum.append(x)
                if len(s_accum) >= s_nextcount:
                    s_nextcount = random.randint(1, 3)
                    sp2.output(s_accum)
                    s_accum = []

        @sp2.node
        def random_basket_key(trigger: ts[object], keys: list) -> ts[str]:
            if sp2.ticked(trigger):
                index = random.randrange(0, len(keys))
                return keys[index]

        @sp2.node
        def assertEqual(node: str, type: str, python: ts["T"], cpp: ts["T"]):
            if sp2.ticked(python, cpp):
                self.assertEqual(python, cpp, f"node: {node} type: {type}")

        def graph():
            types = [bool, int, float, str, datetime, timedelta, date, MyEnum, MyStruct, MyObject, [int]]
            basket_keys = list("ABCDEFGHIJK")

            trigger1 = sp2.timer(timedelta(seconds=1))
            trigger2 = sp2.timer(timedelta(seconds=1.4))
            nodes = {
                sp2.sample: lambda node, typ: node(random_gen(trigger2, typ), random_gen(trigger1, typ)),
                sp2.firstN: lambda node, typ: node(random_gen(trigger1, typ), 5),
                sp2.count: lambda node, typ: node(random_gen(trigger1, typ)),
                sp2.merge: lambda node, typ: node(random_gen(trigger1, typ), random_gen(trigger2, typ)),
                sp2.filter: lambda node, typ: node(random_gen(trigger1, bool), random_gen(trigger2, typ)),
                sp2.unroll: lambda node, typ: node(accum_list(random_gen(trigger1, typ))),
                sp2.demultiplex: lambda node, typ: node(
                    random_gen(trigger1, typ), random_basket_key(trigger2, basket_keys), basket_keys
                ),
                sp2.baselib._delay_by_timedelta: lambda node, typ: node(
                    random_gen(trigger1, typ), timedelta(seconds=0.333)
                ),
                sp2.baselib._delay_by_ticks: lambda node, typ: node(random_gen(trigger1, typ), 2),
            }

            other_nodes = {
                sp2.drop_nans: lambda node: node(random_gen_nan(trigger1)),
                sp2.cast_int_to_float: lambda node: node(random_gen(trigger1, int)),
                sp2.bitwise_not: lambda node: node(random_gen(trigger1, int)),
            }

            def handle_split(node, typ):
                ret = node(random_gen(trigger1, bool), random_gen(trigger2, typ))
                return sp2.merge.python(ret.false, ret.true)

            def handle_multiplex(node, typ):
                basket = {k: random_delay(random_gen(trigger1, typ)) for k in basket_keys}
                return node(basket, random_delay(random_basket_key(trigger1, basket_keys)))

            def handle_collect(node, typ):
                basket = [random_delay(random_gen(trigger1, typ)) for _ in range(20)]
                return node(basket)

            nodes[sp2.split] = handle_split
            nodes[sp2.multiplex] = handle_multiplex
            nodes[sp2.collect] = handle_collect

            for typ in types:
                for node, apply in nodes.items():
                    python = apply(node.python, typ)
                    cpp = apply(node, typ)
                    # for demux basket output
                    if isinstance(python, dict):
                        for k, v in python.items():
                            assertEqual(node.__name__ + f" key{k}", str(typ), v, cpp[k])
                    else:
                        assertEqual(node.__name__, str(typ), python, cpp)

            for node, apply in other_nodes.items():
                python = apply(node.python)
                cpp = apply(node)
                assertEqual(node.__name__, "", python, cpp)

            # Special tests for struct_nodes
            fields_ts = {k: random_delay(random_gen(trigger1, typ)) for k, typ in MyStruct2.metadata().items()}
            struct_ts = MyStruct2.collectts(**fields_ts)
            for field, type in MyStruct2.metadata().items():
                python = sp2.struct_field.python(struct_ts, field, type)
                cpp = sp2.struct_field(struct_ts, field, type)
                assertEqual("sp2.struct_field", str(type), python, cpp)

            # Struct_fromts
            struct_fromts = (
                sp2.baselib._struct_fromts,
                lambda node: node(MyStruct2, fields_ts, sp2.null_ts(bool), False),
            )
            struct_fromts_trigger = (
                sp2.baselib._struct_fromts,
                lambda node: node(MyStruct2, fields_ts, trigger1, True),
            )
            struct_collectts = (sp2.baselib.struct_collectts, lambda node: node(MyStruct2, fields_ts))

            for node, apply in [struct_fromts, struct_fromts_trigger, struct_collectts]:
                python = apply(node.python)
                cpp = apply(node)
                assertEqual(node.__name__, "MyStruct2", python, cpp)

        seed = int(time.time())

        print("test_cppimpls seeding with ", seed)
        random.seed(seed)
        sp2.run(graph, starttime=datetime(2020, 12, 23), endtime=timedelta(seconds=30))

    def test_log(self):
        @sp2.graph
        def graph():
            sp2.log(logging.CRITICAL, "rt", sp2.const(9), logging.getLogger("myVeryOwnLogger"))
            sp2.log(logging.CRITICAL, "won't throw error", sp2.const(1))
            sp2.add_graph_output("i", sp2.const(1))

        st = datetime(2020, 1, 1)
        with self.assertLogs("myVeryOwnLogger", level="CRITICAL") as cm:
            sp2.run(graph, starttime=st)
        self.assertEqual(cm.output, ["CRITICAL:myVeryOwnLogger:2020-01-01 00:00:00 rt:9"])

        # test log dominated graph (proper thread waiting/joining)
        fields = 1000
        LargeStruct = defineStruct("LargeStruct", {f"{i}": int for i in range(fields)})  # struct with 1000 int fields
        structs = []
        for i in range(60):
            struct = LargeStruct()
            for j in range(fields):
                setattr(struct, f"{j}", j + i)
            structs.append(struct)

        @sp2.graph
        def graph():
            x = sp2.curve(LargeStruct, [(st + timedelta(seconds=i + 1), structs[i]) for i in range(60)])
            sp2.log(logging.CRITICAL, "x", x, use_thread=True)  # use default sp2 logger
            sp2.add_graph_output("x", x)

        with self.assertLogs("sp2", level="CRITICAL") as cm:
            sp2.run(graph, starttime=st, endtime=timedelta(seconds=60))

        exp_out = [
            f'CRITICAL:sp2:{(st+timedelta(seconds=(i+1))).strftime("%Y-%m-%d %H:%M:%S")} x:{(structs[i])}'
            for i in range(60)
        ]
        self.assertEqual(cm.output, exp_out)

        # test multiple logs to the same logger
        @sp2.graph
        def graph():
            x = sp2.timer(timedelta(seconds=1), 1.0)
            y = sp2.timer(timedelta(seconds=1), 2.0)
            sp2.log(logging.CRITICAL, "x", x, logging.getLogger("myVeryOwnLogger"), use_thread=True)
            sp2.log(logging.CRITICAL, "y", y, logging.getLogger("myVeryOwnLogger"), use_thread=True)
            sp2.add_graph_output("x", x)

        with self.assertLogs("myVeryOwnLogger", level="CRITICAL") as cm:
            sp2.run(graph, starttime=st, endtime=timedelta(seconds=60))

        l = lambda x: "y:2.0" if x % 2 else "x:1.0"
        exp_out = [
            f'CRITICAL:myVeryOwnLogger:{(st+timedelta(seconds=((i+2)//2))).strftime("%Y-%m-%d %H:%M:%S")} {l(i)}'
            for i in range(120)
        ]
        self.assertEqual(cm.output, exp_out)

        # test multiple different loggers
        @sp2.graph
        def graph():
            x = sp2.curve(float, [(st + timedelta(seconds=i + 1), float(i + 1)) for i in range(60)])
            y = sp2.curve(float, [(st + timedelta(seconds=i + 1), float(i + 2)) for i in range(60)])
            z = sp2.curve(float, [(st + timedelta(seconds=i + 1), float(i + 3)) for i in range(60)])
            sp2.log(logging.CRITICAL, "x", x, logging.getLogger("logger1"), use_thread=True)
            sp2.log(logging.CRITICAL, "y", y, logging.getLogger("logger2"), use_thread=True)
            sp2.log(logging.CRITICAL, "z", z, logging.getLogger("logger3"))
            sp2.add_graph_output("x", x)

        with self.assertLogs("logger1", level="CRITICAL") as cm1, self.assertLogs(
            "logger2", level="CRITICAL"
        ) as cm2, self.assertLogs("logger3", level="CRITICAL") as cm3:
            sp2.run(graph, starttime=st, endtime=timedelta(seconds=60))

        exp_out_log1 = [
            f'CRITICAL:logger1:{(st+timedelta(seconds=(i+1))).strftime("%Y-%m-%d %H:%M:%S")} x:{float(i+1)}'
            for i in range(60)
        ]
        exp_out_log2 = [
            f'CRITICAL:logger2:{(st+timedelta(seconds=(i+1))).strftime("%Y-%m-%d %H:%M:%S")} y:{float(i+2)}'
            for i in range(60)
        ]
        exp_out_log3 = [
            f'CRITICAL:logger3:{(st+timedelta(seconds=(i+1))).strftime("%Y-%m-%d %H:%M:%S")} z:{float(i+3)}'
            for i in range(60)
        ]
        self.assertEqual(cm1.output, exp_out_log1)
        self.assertEqual(cm2.output, exp_out_log2)
        self.assertEqual(cm3.output, exp_out_log3)

    def test_log_output_basket(self):
        @sp2.graph
        def aux() -> sp2.Outputs(a=sp2.ts[int], b=sp2.ts[int]):
            return sp2.output(a=sp2.const(1), b=sp2.const(2))

        @sp2.graph
        def g():
            sp2.log(logging.CRITICAL, "output_basket", aux(), logging.getLogger("myVeryOwnLogger"))

        st = datetime(2020, 1, 1)
        with self.assertLogs("myVeryOwnLogger", level="CRITICAL") as cm:
            sp2.run(g, starttime=st)
        self.assertEqual(cm.output, ["CRITICAL:myVeryOwnLogger:2020-01-01 00:00:00 output_basket:{'a': 1, 'b': 2}"])

    def test_node_renaming(self):
        x = sp2.timer(timedelta(seconds=1), int(2))
        x_f = sp2.cast_int_to_float.using(name="my_cast")(x)  # node implemented in cpp
        sq = sp2.apply.using(name="sq")(x_f, lambda x: x**2, float)
        cube = sp2.apply.using(name="cube")(x_f, lambda x: x**3, float)
        unnamed = sp2.apply(x_f, lambda x: x**4, float)
        my_const = sp2.const.using(name="my_const")(2.0)

        @sp2.graph
        def graph():
            sp2.add_graph_output.using(name="out1")("sq", sq)
            sp2.add_graph_output.using(name="out2")("cube", cube)
            sp2.add_graph_output.using(name="out3")("unnamed", unnamed)
            sp2.add_graph_output.using(name="out4")("my_const", my_const)

        results = sp2.run(graph, starttime=datetime(2020, 12, 23), endtime=timedelta(seconds=10))

        # Verify node names
        self.assertEqual(x_f.nodedef.__name__, "my_cast")
        self.assertEqual(my_const.nodedef.__name__, "my_const")
        self.assertEqual(sq.nodedef.__name__, "sq")
        self.assertEqual(cube.nodedef.__name__, "cube")
        self.assertEqual(unnamed.nodedef.__name__, "apply")

        # Verify nodes function properly
        self.assertEqual(results["sq"], [(datetime(2020, 12, 23) + timedelta(seconds=i + 1), 4.0) for i in range(10)])
        self.assertEqual(results["cube"], [(datetime(2020, 12, 23) + timedelta(seconds=i + 1), 8.0) for i in range(10)])

        # sp2.showgraph.show_graph(graph, graph_filename="graph.png")

    def test_casts(self):
        class Base(sp2.Struct):
            a: int

        class D(Base):
            b: float

        x_int = sp2.const(1)
        x_bool = sp2.const(True)
        x_float = sp2.const(123.456)

        x_b = sp2.const.using(T=Base)(D(a=1, b=2.1))

        def g():
            return {
                "static_b_d": sp2.static_cast(x_b, D),
                "dynamic_bool_int": sp2.dynamic_cast(x_bool, int),
                "dynamic_b_d": sp2.dynamic_cast(x_b, D),
            }

        res = sp2.run(g, starttime=datetime.utcnow(), endtime=timedelta())
        self.assertEqual(res["static_b_d"][0][1], D(a=1, b=2.1))
        self.assertEqual(res["dynamic_bool_int"][0][1], 1)
        self.assertEqual(res["dynamic_b_d"][0][1], D(a=1, b=2.1))

        with self.assertRaisesRegex(TypeError, "Unable to sp2.static_cast edge of type int to str"):
            sp2.run(sp2.static_cast(x_int, str), starttime=datetime.utcnow(), endtime=timedelta())

        with self.assertRaisesRegex(TypeError, "Unable to sp2.static_cast edge of type int to bool"):
            sp2.run(sp2.static_cast(x_int, bool), starttime=datetime.utcnow(), endtime=timedelta())

        # Runtime type check
        with self.assertRaisesRegex(TypeError, 'expected output type on .* to be of type "int" got type "float"'):
            sp2.run(sp2.dynamic_cast(x_float, int), starttime=datetime.utcnow(), endtime=timedelta())


if __name__ == "__main__":
    unittest.main()
