import collections
import gc
import numpy as np
import os
import pickle
import platform
import psutil
import random
import re
import sys
import time
import traceback
import typing
import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import PushMode, ts
from sp2.impl.types.instantiation_type_resolver import ArgTypeMismatchError, TSArgTypeMismatchError
from sp2.impl.wiring.delayed_node import DelayedNodeWrapperDef
from sp2.impl.wiring.runtime import build_graph


@sp2.graph
def _dummy_graph():
    raise NotImplementedError()


@sp2.node
def _dummy_node():
    raise NotImplementedError()


@sp2.graph(cache=True)
def _dummy_graph_cached() -> sp2.ts[float]:
    raise NotImplementedError()
    return sp2.const(1)


@sp2.node(cache=True)
def _dummy_node_cached() -> sp2.ts[float]:
    raise NotImplementedError()
    return 1


class TestEngine(unittest.TestCase):
    def test_simple(self):
        @sp2.node
        def simple(x: ts[int]) -> ts[float]:
            if sp2.ticked(x):
                return x / 2.0

        def graph():
            x = sp2.const(5)
            y = simple(x)
            return y

        result = sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))[0][0]
        self.assertEqual(result[0], datetime(2020, 2, 7, 9))
        self.assertEqual(result[1], 5 / 2.0)

    def test_multiple_inputs(self):
        def graph():
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            y = sp2.curve(int, [(timedelta(seconds=(v + 1) * 2), v + 1) for v in range(2)])

            return sp2.add(x, y)

        result = sp2.run(graph, starttime=datetime(2020, 2, 7, 9))[0]
        self.assertEqual(
            result,
            [
                (datetime(2020, 2, 7, 9, 0, 2), 3),  # First tick only once x and y are valid
                (datetime(2020, 2, 7, 9, 0, 3), 4),
                (datetime(2020, 2, 7, 9, 0, 4), 6),
            ],
        )

    def test_state_noblock(self):
        def graph():
            @sp2.node
            def state_no_block(x: ts[int]) -> ts[int]:
                with sp2.state():
                    s_c = 0

                if sp2.ticked(x):
                    s_c += x
                    return s_c

            return state_no_block(sp2.curve(int, [(timedelta(seconds=v), v) for v in range(10)]))

            result = sp2.run(graph, starttime=datetime(2020, 2, 7, 9))[0][-1]
            self.assertEqual(result, sum(range(10)))

    def test_state_withblock(self):
        def graph():
            @sp2.node
            def state_with_block(x: ts[int], start: int) -> ts[int]:
                with sp2.state():
                    s_c = start

                if sp2.ticked(x):
                    s_c += x
                    return s_c

            x = sp2.curve(int, [(timedelta(seconds=v), v) for v in range(10)])
            return state_with_block(x, 5)

            result = sp2.run(graph, starttime=datetime(2020, 2, 7, 9))[0][-1]
            self.assertEqual(result, 5 + sum(range(10)))

    def test_stop_block(self):
        @sp2.node
        def mutate_on_stop(x: ts[int], out: list):
            with sp2.state():
                s_sum = 0
            with sp2.stop():
                out.append(s_sum)

            if sp2.ticked(x):
                s_sum += x

        out = []
        x = sp2.timer(timedelta(seconds=1), 1)
        sp2.run(mutate_on_stop, x, out, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))
        self.assertEqual(out[0], 10)

    def test_alarm(self):
        @sp2.node
        def alarm_node(repetition: int, cancel: bool = False) -> ts[int]:
            with sp2.alarms():
                alarm = sp2.alarm(int)
            with sp2.start():
                for x in range(repetition):
                    handle = sp2.schedule_alarm(alarm, timedelta(seconds=1), x)
                    if cancel:
                        sp2.cancel_alarm(alarm, handle)

            if sp2.ticked(alarm):
                sp2.schedule_alarm(alarm, timedelta(seconds=1), alarm + repetition)
                return alarm

        result = sp2.run(alarm_node(1), starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual(len(result), 10)
        self.assertEqual([v[1] for v in result], list(range(10)))

        result = sp2.run(alarm_node(2), starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual(len(result), 20)
        self.assertEqual([v[1] for v in result], list(range(20)))

        result = sp2.run(alarm_node(1, True), starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual(len(result), 0)

        result = sp2.run(alarm_node(2, True), starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual(len(result), 0)

        @sp2.node
        def reschedule_node() -> ts[int]:
            with sp2.alarms():
                main = sp2.alarm(bool)
                rescheduled = sp2.alarm(int)
            with sp2.state():
                s_handle = None
                s_expected_time = None

            # TEst will reschedule the alarm twice before allowing it to trigger
            with sp2.start():
                sp2.schedule_alarm(main, timedelta(seconds=1), True)
                s_handle = sp2.schedule_alarm(rescheduled, timedelta(seconds=10), 123)
                s_expected_time = sp2.now() + timedelta(seconds=5)

            if sp2.ticked(main):
                if sp2.num_ticks(main) == 1:
                    sp2.schedule_alarm(main, timedelta(seconds=1), True)
                    # closer execution, start + 10 -> start + (1+2)
                    s_handle = sp2.reschedule_alarm(rescheduled, s_handle, timedelta(seconds=2))
                else:
                    # further execeution, start + (1+2) -> start + ( 2 + 3)
                    s_handle = sp2.reschedule_alarm(rescheduled, s_handle, timedelta(seconds=3))

            if sp2.ticked(rescheduled):
                self.assertEqual(sp2.now(), s_expected_time)
                sp2.stop_engine()

                # verify exception
                with self.assertRaisesRegex(ValueError, "attempting to reschedule expired handle"):
                    sp2.reschedule_alarm(rescheduled, s_handle, timedelta(seconds=1))

                return rescheduled

        result = sp2.run(reschedule_node, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=120))[0]
        self.assertEqual(result[0][1], 123)

        # Test for bug "Cant cancel/reschedule non-collapsed alarms"
        @sp2.node
        def node() -> ts[int]:
            with sp2.alarms():
                main = sp2.alarm(int)
            with sp2.state():
                s_handle = None

            with sp2.start():
                for i in range(10):
                    h = sp2.schedule_alarm(main, timedelta(), i)
                    if i == 5:
                        s_handle = h

            if sp2.ticked(main):
                self.assertNotEqual(main, 5)
                # By 3, 5 should be deferred
                if main == 3:
                    sp2.cancel_alarm(main, s_handle)

                return 1

        sp2.run(node, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=1))

    def test_active_passive(self):
        @sp2.node
        def active_passive(x: ts[int], y: ts[int]) -> ts[int]:
            if sp2.ticked(y):
                if sp2.num_ticks(y) % 2 == 1:
                    # intentionally testing multiple calls
                    sp2.make_passive(x)
                    sp2.make_passive(x)
                    sp2.make_passive(x)
                else:
                    sp2.make_active(x)
                    sp2.make_active(x)

            if sp2.ticked(x):
                return x

        x = sp2.count(sp2.timer(timedelta(seconds=1), True))
        y = sp2.count(sp2.timer(timedelta(seconds=1.01), True))
        result = sp2.run(active_passive(x, y), starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual(
            result,
            [
                (datetime(2020, 2, 7, 9, 0, 1), 1),
                (datetime(2020, 2, 7, 9, 0, 3), 3),
                (datetime(2020, 2, 7, 9, 0, 5), 5),
                (datetime(2020, 2, 7, 9, 0, 7), 7),
                (datetime(2020, 2, 7, 9, 0, 9), 9),
            ],
        )

        @sp2.node
        def active_passive(x: ts[int]) -> sp2.Outputs(x=ts[int], active=ts[bool]):
            with sp2.alarms():
                alarm = sp2.alarm(bool)
            with sp2.start():
                sp2.schedule_alarm(alarm, timedelta(seconds=1), True)

            if sp2.ticked(alarm):
                # Skew to get to 0
                if random.random() > 0.7:
                    sp2.make_active(x)
                    sp2.output(active=True)
                else:
                    sp2.make_passive(x)
                    sp2.output(active=False)

                sp2.schedule_alarm(alarm, timedelta(seconds=1), True)

            if sp2.ticked(x):
                sp2.output(x=x)

        @sp2.node
        def checkActiveTick(x_orig: ts[int], x: ts[int], active: ts[bool]):
            if sp2.ticked(x_orig) and sp2.valid(active):
                self.assertEqual(active, sp2.ticked(x), (sp2.now(), x_orig))

        def g():
            # intentionally misalign the input tick, we dont want it to tick at the same time as the alarm switch for this test
            x = sp2.count(sp2.timer(timedelta(seconds=1.0 / 3.0)))

            with sp2.memoize(False):
                # Create a duplicate input so that we dont keep x active in checkActiveTick
                # we want to force consumers to go to and from 0
                x_dup = sp2.count(sp2.timer(timedelta(seconds=1.0 / 3.0)))
                # We want to exercise the consumer vector empty/single/vector logic
                # Ensure we create multiple consumers by turning off memoization
                for i in range(5):
                    res = active_passive(x)
                    checkActiveTick(x_dup, res.x, res.active)

        seed = int(time.time())
        print("USING SEED", seed)
        random.seed(seed)
        sp2.run(g, starttime=datetime(2022, 7, 26), endtime=timedelta(minutes=30))

    def test_node_sp2_count(self):
        @sp2.node
        def count(x: ts[int]) -> ts[int]:
            if sp2.ticked(x):
                return sp2.num_ticks(x)

        x = sp2.count(sp2.timer(timedelta(seconds=1), True))
        result = sp2.run(x, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual([v[1] for v in result], list(range(1, 11)))

    def test_named_outputs(self):
        @sp2.node
        def split(x: ts[int]) -> sp2.Outputs(even=ts[int], odd=ts[int]):
            if sp2.ticked(x):
                if x % 2 == 0:
                    sp2.output(even=x)
                else:
                    sp2.output(odd=x)

        x = sp2.count(sp2.timer(timedelta(seconds=1), True))
        result = sp2.run(split, x, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))
        self.assertEqual([v[1] for v in result["even"]], list(range(2, 11, 2)))
        self.assertEqual([v[1] for v in result["odd"]], list(range(1, 10, 2)))

    def test_named_return(self):
        @sp2.node
        def split(x: ts[int]) -> sp2.Outputs(even=ts[int], odd=ts[int]):
            if sp2.ticked(x):
                if x % 2 == 0:
                    return sp2.output(even=x)
                return sp2.output(odd=x)

        x = sp2.count(sp2.timer(timedelta(seconds=1), True))
        result = sp2.run(split, x, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))
        self.assertEqual([v[1] for v in result["even"]], list(range(2, 11, 2)))
        self.assertEqual([v[1] for v in result["odd"]], list(range(1, 10, 2)))

    def test_single_sp2_output(self):
        @sp2.node
        def count(x: ts[int]) -> ts[int]:
            if sp2.ticked(x):
                sp2.output(sp2.num_ticks(x) * 2)

        x = sp2.timer(timedelta(seconds=1), True)
        result = sp2.run(count, x, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual([v[1] for v in result], list(x * 2 for x in range(1, 11)))

    def test_single_sp2_numpy_output(self):
        @sp2.node
        def count(x: ts[int]) -> ts[int]:
            if sp2.ticked(x):
                sp2.output(sp2.num_ticks(x) * 2)

        x = sp2.timer(timedelta(seconds=1), True)
        result = sp2.run(count, x, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10), output_numpy=True)[
            0
        ]
        expected_times = np.array(
            list(np.datetime64(datetime(2020, 2, 7, 9) + timedelta(seconds=x)) for x in range(1, 11))
        )
        self.assertTrue(np.array_equal(result[0], expected_times))
        self.assertEqual(result[1].tolist(), list(x * 2 for x in range(1, 11)))

    def test_multi_sp2_numpy_output(self):
        @sp2.graph
        def my_graph():
            sp2.add_graph_output("a", sp2.const("foo"))
            sp2.add_graph_output("b", sp2.merge(sp2.const(1), sp2.const(2, timedelta(seconds=1))))

        result = sp2.run(my_graph, starttime=datetime(2021, 6, 21), output_numpy=True)

        res1 = result["a"]
        expected_times_1 = np.array([np.datetime64(datetime(2021, 6, 21))])
        self.assertTrue(np.array_equal(res1[0], expected_times_1))
        self.assertEqual(res1[1].tolist(), ["foo"])

        res2 = result["b"]
        expected_times_2 = np.array([np.datetime64(datetime(2021, 6, 21) + timedelta(seconds=x)) for x in (0, 1)])
        self.assertTrue(np.array_equal(res2[0], expected_times_2))
        self.assertEqual(res2[1].tolist(), [1, 2])

    def test_single_valued_sp2_numpy_output(self):
        # these are a special case where, due to optimization, there is no buffer so we only need the last value
        class Foo:
            pass

        foo = Foo()

        @sp2.graph
        def g():
            sp2.add_graph_output("a", sp2.const("a"), tick_count=1)
            sp2.add_graph_output("b", sp2.count(sp2.timer(timedelta(seconds=1), 1)), tick_count=1)
            sp2.add_graph_output("c", sp2.const(foo), tick_count=1)
            sp2.add_graph_output("d", sp2.const(datetime(2020, 1, 1)), tick_count=1)
            sp2.add_graph_output("e", sp2.const(timedelta(seconds=1)), tick_count=1)

        res = sp2.run(g, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=2), output_numpy=True)

        # times
        exp_time_1 = np.array([np.datetime64(datetime(2020, 1, 1))])
        for out in ["a", "c", "d", "e"]:
            self.assertTrue(np.array_equal(res[out][0], exp_time_1))
        exp_time_2 = np.array([np.datetime64(datetime(2020, 1, 1) + timedelta(seconds=2))])
        self.assertTrue(np.array_equal(res["b"][0], exp_time_2))

        # values
        self.assertEqual(res["a"][1].tolist(), ["a"])
        self.assertEqual(res["b"][1].tolist(), [2])
        self.assertEqual(res["c"][1].tolist(), [foo])
        self.assertTrue(np.array_equal(res["d"][1], exp_time_1))
        self.assertTrue(np.array_equal(res["e"][1], np.array([np.timedelta64(timedelta(seconds=1))])))

    def test_single_sp2_return(self):
        @sp2.node
        def count(x: ts[int]) -> ts[int]:
            if sp2.ticked(x):
                return sp2.output(sp2.num_ticks(x) * 2)

        x = sp2.timer(timedelta(seconds=1), True)
        result = sp2.run(count, x, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual([v[1] for v in result], list(x * 2 for x in range(1, 11)))

    def test_sp2_now(self):
        @sp2.node
        def times(x: ts[bool]) -> ts[datetime]:
            if sp2.ticked(x):
                return sp2.now()

        x = sp2.timer(timedelta(seconds=1), True)
        result = sp2.run(times(x), starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))[0]
        self.assertEqual([v[0] for v in result], [v[1] for v in result])

    def test_stop_engine(self):
        @sp2.node
        def stop(x: ts[bool]) -> ts[bool]:
            if sp2.ticked(x):
                if sp2.num_ticks(x) == 5:
                    sp2.stop_engine()
                return x

        result = sp2.run(stop, sp2.timer(timedelta(seconds=1)), starttime=datetime(2020, 5, 19))[0]
        self.assertEqual(len(result), 5)

    def test_class_member_node(self):
        class ClassWithNodes:
            def __init__(self):
                self._data = []

            @sp2.node
            def member_node(self: object, x: ts[int]):
                """it is NOT recommended to mutate state in a node!!"""
                if sp2.ticked(x):
                    self._data.append(x)

        c = ClassWithNodes()

        def graph():
            x = c.member_node(sp2.count(sp2.timer(timedelta(seconds=1), True)))

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=timedelta(seconds=10))
        self.assertEqual(c._data, list(range(1, 11)))

    def test_duplicate_outputs(self):
        def graph():
            sp2.add_graph_output(0, sp2.const(1))
            return sp2.const(2)

        with self.assertRaisesRegex(ValueError, 'graph output key "0" is already bound'):
            sp2.run(graph, starttime=datetime.now())

    def test_with_support(self):
        # This test case tests a parsing bug that we had, where "with" statement at the main function block was causing parse error
        class ValueSetter(object):
            def __init__(self, l: typing.List[int]):
                self._l = l

            def __enter__(self):
                self._l.append(1)

            def __exit__(self, exc_type, exc_val, exc_tb):
                self._l.append(2)

        @sp2.node
        def my_node(inp: ts[bool]) -> ts[[int]]:
            with sp2.state():
                l = []
            with ValueSetter(l):
                return l

        def graph():
            sp2.add_graph_output("my_node", my_node(sp2.timer(timedelta(seconds=1))))

        res = sp2.run(graph, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=3))
        self.assertEqual(res["my_node"][-1][1], [1, 2, 1, 2, 1])
        self.assertEqual(res["my_node"][-2][1], [1, 2, 1])
        self.assertEqual(res["my_node"][-3][1], [1])

    def test_bugreport_sp228(self):
        """bug where non-basket inputs after basket inputs were not being assigne dproperly in c++"""

        @sp2.node
        def buggy(basket: [ts[int]], x: ts[bool]) -> ts[bool]:
            if sp2.ticked(x) and sp2.valid(x):
                return x

        result = sp2.run(buggy, [sp2.const(1, delay=timedelta(seconds=1))], sp2.const(True), starttime=datetime.now())[
            0
        ]
        self.assertEqual(len(result), 1)

    def test_output_validation(self):
        from sp2.impl.wiring import Sp2ParseError

        with self.assertRaisesRegex(Sp2ParseError, "returning from node without any outputs defined"):

            @sp2.node
            def n(x: ts[bool]):
                return 1

        with self.assertRaisesRegex(Sp2ParseError, "returning from node without any outputs defined"):

            @sp2.node
            def n(x: ts[bool]):
                sp2.output(1)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def n(x: ts[bool]) -> ts[bool]:
                sp2.output(x=1)

        with self.assertRaisesRegex(
            Sp2ParseError, "node has __outputs__ defined but no return or sp2.output statements"
        ):

            @sp2.node
            def n(x: ts[bool]) -> ts[bool]:
                pass

        with self.assertRaisesRegex(Sp2ParseError, "output 'y' is never returned"):

            @sp2.node
            def n(x: ts[bool]) -> sp2.Outputs(x=ts[bool], y=ts[bool]):
                sp2.output(x=5)

        with self.assertRaisesRegex(Sp2ParseError, "output 'y' is never returned"):

            @sp2.node
            def n(x: ts[bool]) -> sp2.Outputs(x=ts[bool], y=ts[bool]):
                return sp2.output(x=5)

        with self.assertRaisesRegex(KeyError, "Output y is not returned from the graph"):

            @sp2.graph
            def g() -> sp2.Outputs(x=ts[int], y=ts[int]):
                return sp2.output(x=sp2.const(1), z=sp2.const(3))

            sp2.run(g, starttime=datetime.now(), endtime=timedelta(seconds=1))

    def test_access_before_valid(self):
        @sp2.node
        def foo(x: ts[int], y: ts[int]):
            print(x + y)

        major, minor, *rest = sys.version_info
        if major >= 3 and minor >= 11:
            expected_str = "cannot access local variable"
        else:
            expected_str = "referenced before assignment"
        with self.assertRaisesRegex(UnboundLocalError, expected_str):
            sp2.run(foo, sp2.const(1), sp2.const(1, delay=timedelta(1)), starttime=datetime.utcnow())

    def test_cell_access(self):
        '''was a bug "PyNode crashes on startup when cellvars are generated"'''

        # All types of ts inputs as cellvars, no args
        @sp2.node
        def node(x: ts[int], y: [ts[int]], x2: ts[int], y2: [ts[int]], s: int) -> sp2.Outputs(o1=ts[int], o2=ts[int]):
            with sp2.state():
                s_1 = 1
                s_2 = 2

            ## Force as many combinations of locals vs cellvars as we can
            xl = lambda: x2
            yl = lambda: y2[0]
            ol = lambda v: sp2.output(o2, v)
            sl = lambda: s_2
            # Node ref
            nl = lambda: sp2.now()

            val = nl()
            out = xl() + yl() + sl()
            ol(out)

            sp2.output(o1, 1)

        res = sp2.run(
            node, sp2.const(1), [sp2.const(1)], sp2.const(100), [sp2.const(200)], 5, starttime=datetime.utcnow()
        )["o2"][0]
        self.assertEqual(res[1], 100 + 200 + 2)

        # Test arguments in cellvars werent being processed correctly

        # scalar only in cellvar
        @sp2.node
        def node2(x: ts[int], s: int) -> ts[int]:
            f = lambda: s
            return x * f()

        res = sp2.run(node2, sp2.const(1), 5, starttime=datetime.utcnow())[0][0]
        self.assertEqual(res[1], 5)

        # scalar and ts in cellvar
        @sp2.node
        def node3(x: ts[int], s: int) -> ts[int]:
            with sp2.state():
                s_1 = 1
                s_2 = 2

            f = lambda: x * s
            return f()

        res = sp2.run(node3, sp2.const(1), 5, starttime=datetime.utcnow())[0][0]
        self.assertEqual(res[1], 5)

    def test_stop_time(self):
        '''was a bug "__stop__ sp2.now() returns wrong time"'''

        @sp2.node
        def t(x: ts[int], endtime: datetime):
            with sp2.stop():
                self.assertEqual(sp2.now(), endtime)

            if sp2.ticked(x):
                pass

        st = datetime(2020, 6, 11)
        et = st + timedelta(seconds=10)
        sp2.run(t, sp2.timer(timedelta(seconds=1)), et, starttime=st, endtime=et)

        ## This checks that endtime aligns with time at time of a stop_engine call
        @sp2.node
        def t(x: ts[int], endtime: datetime):
            with sp2.alarms():
                stop = sp2.alarm(bool)
            with sp2.start():
                sp2.schedule_alarm(stop, endtime, True)

            with sp2.stop():
                self.assertEqual(sp2.now(), endtime)

            if sp2.ticked(stop):
                sp2.stop_engine()

        st = datetime(2020, 6, 11)
        sp2.run(t, sp2.timer(timedelta(seconds=1)), st + timedelta(seconds=5), starttime=st, endtime=et)

    def test_duplicate_time(self):
        data = [
            (timedelta(seconds=0), 1),
            (timedelta(seconds=1), 2),
            (timedelta(seconds=1), 3),
            (timedelta(seconds=2), 4),
            (timedelta(seconds=2), 5),
            (timedelta(seconds=3), 6),
            (timedelta(seconds=4), 7),
        ]

        c = sp2.curve(int, data, push_mode=sp2.PushMode.NON_COLLAPSING)

        # Forcing through a node
        c = sp2.filter(sp2.const(True), c)
        st = datetime(2020, 1, 1)
        r = sp2.run(c, starttime=st)[0]
        expected = [(st + d[0], d[1]) for d in data]
        self.assertEqual(r, expected)

        ## Test duplicate time on alarms
        @sp2.node
        def alarms(data: list) -> ts[int]:
            with sp2.alarms():
                tick = sp2.alarm(int)
            with sp2.state():
                s_index = 0
                s_start = sp2.now()
            with sp2.start():
                sp2.schedule_alarm(tick, s_start + data[s_index][0], data[s_index][1])
                s_index += 1

            if sp2.ticked(tick):
                sp2.output(tick)
                if s_index < len(data):
                    sp2.schedule_alarm(tick, s_start + data[s_index][0], data[s_index][1])
                    s_index += 1

        r = sp2.run(alarms, data, starttime=st)[0]
        self.assertEqual(r, expected)

    def test_sim_push_mode(self):
        data = [
            (timedelta(seconds=0), 1),
            (timedelta(seconds=1), 2),
            (timedelta(seconds=1), 3),
            (timedelta(seconds=2), 4),
            (timedelta(seconds=2), 5),
            (timedelta(seconds=2), 6),
            (timedelta(seconds=3), 7),
            (timedelta(seconds=4), 8),
        ]

        def graph():
            lv = sp2.curve(int, data, push_mode=sp2.PushMode.LAST_VALUE)
            nc = sp2.curve(int, data, push_mode=sp2.PushMode.NON_COLLAPSING)
            b = sp2.curve(int, data, push_mode=sp2.PushMode.BURST)

            sp2.add_graph_output("lv", lv)
            sp2.add_graph_output("nc", nc)
            sp2.add_graph_output("b", b)

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st)

        self.assertEqual(results["nc"], [(st + td, v) for td, v in data])
        self.assertEqual(results["lv"], [(st + td, v) for td, v in data if v not in (2, 4, 5)])
        b = collections.defaultdict(list)
        for t, v in data:
            b[st + t].append(v)
        self.assertEqual(results["b"], list(b.items()))

    def test_managed_sim_input_pushmode(self):
        from sp2.impl.adaptermanager import AdapterManagerImpl, ManagedSimInputAdapter
        from sp2.impl.wiring import py_managed_adapter_def

        class TestAdapterManager:
            def __init__(self, data):
                self._data = data

            def subscribe(self, id, push_mode):
                return TestAdapter(self, int, id, push_mode=push_mode)

            def _create(self, engine, memo):
                return TestAdapterManagerImpl(engine, self)

        class TestAdapterManagerImpl(AdapterManagerImpl):
            def __init__(self, engine, adapterRep):
                super().__init__(engine)
                self._data = adapterRep._data
                self._inputs = {}
                self._idx = 0

            def start(self, starttime, endtime):
                pass

            def register_input_adapter(self, id, adapter):
                self._inputs[id] = adapter

            def process_next_sim_timeslice(self, now):
                if self._idx >= len(self._data):
                    return None

                while self._idx < len(self._data):
                    time, id, value = self._data[self._idx]
                    if time > now:
                        return time
                    self._inputs[id].push_tick(value)
                    self._idx += 1

                return None

        class TestAdapterImpl(ManagedSimInputAdapter):
            def __init__(self, managerImpl, typ, id):
                managerImpl.register_input_adapter(id, self)

        TestAdapter = py_managed_adapter_def(
            "test_adapter", TestAdapterImpl, ts["T"], TestAdapterManager, typ="T", id=str
        )

        st = datetime(2020, 6, 17)
        data = [
            (st + timedelta(seconds=1), "lv", 1),
            (st + timedelta(seconds=1), "lv", 2),
            (st + timedelta(seconds=1), "nc", 1),
            (st + timedelta(seconds=1), "nc", 2),
            (st + timedelta(seconds=1), "b", 1),
            (st + timedelta(seconds=1), "b", 2),
            (st + timedelta(seconds=2), "nc", 3),
            (st + timedelta(seconds=3), "lv", 3),
            (st + timedelta(seconds=4), "lv", 4),
            (st + timedelta(seconds=4), "lv", 5),
            (st + timedelta(seconds=4), "b", 3),
            (st + timedelta(seconds=4), "b", 4),
            (st + timedelta(seconds=4), "b", 5),
            (st + timedelta(seconds=4), "b", 6),
            (st + timedelta(seconds=5), "nc", 4),
            (st + timedelta(seconds=5), "nc", 5),
            (st + timedelta(seconds=5), "nc", 6),
            (st + timedelta(seconds=5), "b", 7),
            (st + timedelta(seconds=5), "b", 8),
            (st + timedelta(seconds=5), "b", 9),
        ]

        def graph():
            adapter = TestAdapterManager(data)

            nc = adapter.subscribe("nc", push_mode=sp2.PushMode.NON_COLLAPSING)
            lv = adapter.subscribe("lv", push_mode=sp2.PushMode.LAST_VALUE)
            b = adapter.subscribe("b", push_mode=sp2.PushMode.BURST)

            sp2.add_graph_output("nc", nc)
            sp2.add_graph_output("lv", lv)
            sp2.add_graph_output("b", b)

        results = sp2.run(graph, starttime=st)
        self.assertEqual(results["lv"], [(v[0], v[2]) for v in data if v[1] == "lv" and v[2] not in (1, 4)])
        self.assertEqual(results["nc"], [(v[0], v[2]) for v in data if v[1] == "nc"])
        b = collections.defaultdict(list)
        for t, n, v in data:
            if n == "b":
                b[t].append(v)
        self.assertEqual(results["b"], list(b.items()))

    def test_feedback(self):
        # Dummy example
        class Request(sp2.Struct):
            command: str

        class Reply(sp2.Struct):
            response: str

        @sp2.node
        def process_req(request: ts[Request]) -> ts[Reply]:
            with sp2.alarms():
                reply = sp2.alarm(Reply)
            if sp2.ticked(request):
                sp2.schedule_alarm(reply, timedelta(seconds=1), Reply(response="ack" + request.command))

            if sp2.ticked(reply):
                return reply

        responses = []

        @sp2.node
        def req_reply(command: ts[str], reply: ts[Reply]) -> ts[Request]:
            if sp2.ticked(command):
                return Request(command=command)

            if sp2.ticked(reply):
                responses.append((sp2.now(), reply))

        @sp2.graph
        def graph():
            commands = sp2.curve(str, [(timedelta(seconds=x), str(x)) for x in range(10)])

            reply_fb = sp2.feedback(Reply)
            requests = req_reply(commands, reply_fb.out())
            reply = process_req(requests)
            reply_fb.bind(reply)

            sp2.add_graph_output("reply_fb", reply_fb.out())
            sp2.add_graph_output("reply", reply)

        st = datetime(2020, 7, 7)
        results = sp2.run(graph, starttime=st)
        self.assertEqual(responses, [(st + timedelta(seconds=x + 1), Reply(response="ack%s" % x)) for x in range(10)])
        self.assertEqual(responses, results["reply_fb"])
        self.assertEqual(responses, results["reply"])

        ## Test exceptions
        def graph():
            fb = sp2.feedback(int)
            with self.assertRaisesRegex(
                TypeError,
                re.escape(r"""In function _bind: Expected sp2.impl.types.tstype.TsType[""")
                + ".*"
                + re.escape(r"""('T')] for argument 'x', got 1 (int)"""),
            ):
                fb.bind(1)

            with self.assertRaisesRegex(
                TypeError, re.escape(r"""In function _bind: Expected ts[T] for argument 'x', got ts[str](T=int)""")
            ):
                fb.bind(sp2.const("123"))

            fb.bind(sp2.const(1))
            with self.assertRaisesRegex(RuntimeError, "sp2.feedback is already bound"):
                fb.bind(sp2.const(1))

        build_graph(graph)

        def unbound_graph():
            fb = sp2.feedback(int)
            sp2.print("test", fb.out())

        with self.assertRaisesRegex(RuntimeError, "unbound sp2.feedback used in graph"):
            sp2.run(unbound_graph, starttime=datetime.utcnow())

    def test_list_feedback_typecheck(self):
        @sp2.graph
        def g() -> sp2.ts[[int]]:
            fb = sp2.feedback([int])
            with self.assertRaisesRegex(
                TypeError, re.escape(r"""Expected ts[T] for argument 'x', got ts[int](T=typing.List[int])""")
            ):
                fb.bind(sp2.const(42))

            fb.bind(sp2.const([42]))
            return fb.out()

        res = sp2.run(g, starttime=datetime.utcnow())
        self.assertEqual(res[0][0][1], [42])

        # Test Typing.List which was a bug "crash on feedback tick"
        @sp2.graph
        def g() -> sp2.ts[typing.List[int]]:
            fb = sp2.feedback(typing.List[int])
            with self.assertRaisesRegex(
                TypeError, re.escape(r"""Expected ts[T] for argument 'x', got ts[int](T=typing.List[int])""")
            ):
                fb.bind(sp2.const(42))

            fb.bind(sp2.const([42]))
            return fb.out()

        res = sp2.run(g, starttime=datetime.utcnow())
        self.assertEqual(res[0][0][1], [42])

    def test_list_inside_callable(self):
        '''was a bug "Empty list inside callable annotation raises exception"'''

        @sp2.graph
        def graph(v: typing.Dict[str, typing.Callable[[], str]]):
            pass

        sp2.run(graph, {"x": (lambda v: v)}, starttime=datetime(2020, 6, 17))

    def test_tuples_as_list(self):
        '''was a bug "Support tuples as list baskets"'''

        @sp2.node
        def sum_vals(inputs: [ts["T"]]) -> ts["T"]:
            if sp2.ticked(inputs) and sp2.valid(inputs):
                return sum((inp for inp in inputs))

        @sp2.graph
        def my_graph():
            my_ts = sp2.timer(timedelta(hours=1), 1)
            tuple_basket = (my_ts, my_ts)

            sp2.add_graph_output("sampled", sum_vals(tuple_basket))

        g = sp2.run(my_graph, starttime=datetime(2020, 3, 1, 9, 30), endtime=timedelta(hours=0, minutes=390))

    def test_node_parse_stack(self):
        '''was a bug "Node parsing exception stacks are truncated, but type errors when invoking are not."'''

        @sp2.node
        def aux(tag: str, my_arg: ts["T"]):
            pass

        @sp2.node
        def f(x: ts[int]):
            __out__()
            pass

        def graph():
            x = f(sp2.const(1))
            aux("x", x)

        try:
            build_graph(graph)
            # Should never get here
            self.assertFalse(True)
        except Exception as e:
            self.assertIsInstance(e, TSArgTypeMismatchError)
            traceback_list = list(
                filter(lambda v: v.startswith("File"), (map(str.strip, traceback.format_exc().split("\n"))))
            )
            self.assertTrue(__file__ in traceback_list[-1])
            self.assertLessEqual(len(traceback_list), 10)
            self.assertEqual(str(e), "In function aux: Expected ts[T] for argument 'my_arg', got None")

    def test_union_type_check(self):
        '''was a bug "Add support for typing.Union in type checking layer"'''

        @sp2.graph
        def graph(x: typing.Union[int, float, str]):
            pass

        build_graph(graph, 1)
        build_graph(graph, 1.1)
        build_graph(graph, "s")
        with self.assertRaisesRegex(
            TypeError,
            "In function graph: Expected typing.Union\\[int, float, str\\] for argument 'x', got \\[1.1\\] \\(list\\)",
        ):
            build_graph(graph, [1.1])

        @sp2.graph
        def graph(x: ts[typing.Union[int, float, str]]):
            pass

        build_graph(graph, sp2.const(1))
        build_graph(graph, sp2.const(1.1))
        build_graph(graph, sp2.const("s"))
        with self.assertRaisesRegex(
            TypeError,
            "In function graph: Expected ts\\[typing.Union\\[int, float, str\\]\\] for argument 'x', got ts\\[typing.List\\[float\\]\\]",
        ):
            build_graph(graph, sp2.const([1.1]))

    def test_realtime_timers(self):
        """was a bug"""
        rv = sp2.run(
            sp2.timer,
            timedelta(seconds=1),
            starttime=datetime.utcnow(),
            endtime=timedelta(seconds=3),
            realtime=True,
            queue_wait_time=timedelta(seconds=0.001),
        )[0]
        self.assertLess(len(rv), 3)

    def test_graph_arguments_propagation(self):
        @sp2.graph
        def my_graph(s: str, i: int):
            sp2.add_graph_output("s", sp2.const(s))
            sp2.add_graph_output("i", sp2.const(i))

        rv = sp2.run(my_graph, s="sss", i=42, starttime=datetime.utcnow(), endtime=timedelta(seconds=1))
        self.assertEqual(1, len(rv["s"]))
        self.assertEqual(rv["s"][0][1], "sss")
        self.assertEqual(1, len(rv["i"]))
        self.assertEqual(rv["i"][0][1], 42)

        rv = sp2.run(my_graph, "sss", 42, starttime=datetime.utcnow(), endtime=timedelta(seconds=1))
        self.assertEqual(1, len(rv["s"]))
        self.assertEqual(rv["s"][0][1], "sss")
        self.assertEqual(1, len(rv["i"]))
        self.assertEqual(rv["i"][0][1], 42)

    def test_caching_non_cachable_object(self):
        class Dummy:
            def __hash__(self):
                hash({})

        @sp2.graph
        def sub_graph(x: Dummy) -> sp2.Outputs(i=ts[int]):
            return sp2.const(1)

        @sp2.graph
        def my_graph():
            sp2.add_graph_output("i", sub_graph(Dummy()))

        sp2.run(my_graph, starttime=datetime.now())

        @sp2.graph(force_memoize=True)
        def sub_graph(x: Dummy) -> sp2.Outputs(i=ts[int]):
            return sp2.const(1)

        @sp2.graph
        def my_graph():
            sp2.add_graph_output("i", sub_graph(Dummy()))

        with self.assertRaisesRegex(TypeError, "unhashable type.*"):
            sp2.run(my_graph, starttime=datetime.now())

    def test_realtime_timer_lag(self):
        '''bugfix exception when timers would reschedule on a lagged engine
        "timers in realtime raise exception if they get behind"'''
        delay = timedelta(seconds=0.25)
        timer_interval = timedelta(seconds=0.1)

        @sp2.node
        def lag(x: ts[int]) -> ts[datetime]:
            if sp2.ticked(x):
                import time

                time.sleep(delay.total_seconds())
                return datetime.utcnow()

        @sp2.graph
        def graph(count: int, allow_deviation: bool) -> ts[datetime]:
            x = lag(sp2.count(sp2.timer(timer_interval, allow_deviation=allow_deviation)))
            stop_cond = sp2.count(x) == count
            sp2.stop_engine(sp2.filter(stop_cond, stop_cond))
            return x

        results = sp2.run(graph, 4, False, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True)[0]
        self.assertEqual(len(results), 4)
        self.assertTrue(all((results[i][0] - results[i - 1][0]) == timer_interval for i in range(1, len(results))))
        # Assert lag from engine -> wallclock on last tick is greater than minimum expected amount
        self.assertGreater(results[-1][1] - results[-1][0], (delay - timer_interval) * len(results))

        results = sp2.run(graph, 5, True, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True)[0]
        self.assertEqual(len(results), 5)
        self.assertTrue(all((results[i][0] - results[i - 1][0]) > delay for i in range(2, len(results))))

    def test_timer_exception(self):
        with self.assertRaisesRegex(ValueError, "sp2.timer interval must be > 0"):
            _ = sp2.timer(timedelta(0))

    def test_list_comprehension_bug(self):
        @sp2.node
        def list_comprehension_bug_node(n_seconds: int, input: sp2.ts["T"]) -> sp2.ts[["T"]]:
            with sp2.start():
                sp2.set_buffering_policy(input, tick_history=timedelta(seconds=30))

            if sp2.ticked(input):
                return [sp2.value_at(input, timedelta(seconds=-n_seconds + i), default=0) for i in range(1)]

        @sp2.graph
        def list_comprehension_bug_graph():
            curve_int = sp2.curve(int, [(timedelta(seconds=i), i) for i in range(30)])
            sp2.add_graph_output("Bucket", list_comprehension_bug_node(10, curve_int))

        rv = sp2.run(list_comprehension_bug_graph, starttime=datetime(2020, 1, 1))["Bucket"]
        self.assertEqual([v[1][0] for v in rv[10:]], list(range(20)))

    def test_alarm_leak(self):
        """this was a leak in Scheduler.cpp"""

        @sp2.node
        def generate(x: ts[object]):
            with sp2.alarms():
                alarm = sp2.alarm(str)

            if sp2.ticked(x):
                for x in range(100):
                    sp2.schedule_alarm(alarm, timedelta(seconds=1), "test")

        def graph():
            generate(sp2.timer(timedelta(seconds=1)))

        proc_info = psutil.Process(os.getpid())
        start_mem = proc_info.memory_info().rss
        for _ in range(5):
            sp2.run(graph, starttime=datetime(2020, 9, 24), endtime=timedelta(hours=1))
            gc.collect()
        end_mem = proc_info.memory_info().rss

        # 5MB leeway, the leak resulted in 50MB+ leak
        self.assertLess(end_mem - start_mem, 5000000)

    def test_multiple_alarms_bug(self):
        @sp2.node
        def n() -> sp2.ts[int]:
            with sp2.alarms():
                a1 = sp2.alarm(int)
                a2 = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a1, timedelta(seconds=5), 1)
                sp2.schedule_alarm(a2, timedelta(seconds=10), 2)
            if sp2.ticked(a1):
                self.assertEqual(a1, 1)
                return a1
            if sp2.ticked(a2):
                self.assertEqual(a2, 2)
                return a2

        @sp2.graph
        def g():
            sp2.add_graph_output("o", n())

        res = sp2.run(g, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=10))
        self.assertEqual(res, {"o": [(datetime(2020, 1, 1, 0, 0, 5), 1), (datetime(2020, 1, 1, 0, 0, 10), 2)]})

    def test_memoize_non_comparable(self):
        class A:
            pass

        @sp2.node
        def my_sink(x: ts["T"]):
            pass

        @sp2.graph
        def g(o: object):
            my_sink(sp2.const(1))

        sp2.run(
            g,
            {A(): "f1", A(): "f2"},
            starttime=datetime(
                2020,
                1,
                1,
            ),
            endtime=timedelta(seconds=1),
        )
        sp2.run(
            g,
            {A(), A()},
            starttime=datetime(
                2020,
                1,
                1,
            ),
            endtime=timedelta(seconds=1),
        )

    def test_nested_using(self):
        @sp2.graph
        def g(x: "~X", y: "~Y"):
            pass

        sp2.run(g.using(X=int).using(Y=float), 1, 2, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=10))
        with self.assertRaises(ArgTypeMismatchError):
            sp2.run(g.using(X=int).using(Y=str), 1, 2, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=10))

    def test_null_nodes(self):
        @sp2.node
        def assert_never_ticks(i: ts["T"]):
            if sp2.ticked(i):
                raise RuntimeError("Unexpected ticked value")

        @sp2.graph
        def g():
            assert_never_ticks.using(T=str)(sp2.null_ts(str))
            assert_never_ticks(sp2.null_ts(str))
            with self.assertRaises(TSArgTypeMismatchError):
                assert_never_ticks.using(T=int)(sp2.null_ts(str))

        sp2.run(g, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=10))

    def test_start_end_times(self):
        start_time = datetime(2020, 1, 1, 9, 31, 5, 1)
        end_time = start_time + timedelta(seconds=20)

        @sp2.node
        def n():
            with sp2.start():
                self.assertEqual(sp2.engine_start_time(), start_time)
                self.assertEqual(sp2.engine_end_time(), end_time)

        @sp2.graph
        def g():
            self.assertEqual(sp2.engine_start_time(), start_time)
            self.assertEqual(sp2.engine_end_time(), end_time)
            n()

        sp2.run(g, starttime=start_time, endtime=end_time)

        with self.assertRaisesRegex(RuntimeError, "sp2 graph information is not available"):
            sp2.engine_start_time()

    def test_ctrl_c(self):
        pid = os.fork()
        if pid == 0:
            all_good = False
            try:
                x = sp2.timer(timedelta(seconds=1), True)
                sp2.run(x, starttime=datetime.utcnow(), endtime=timedelta(seconds=60), realtime=True)
            except KeyboardInterrupt:
                all_good = True

            os._exit(all_good)
        else:
            import signal
            import time

            time.sleep(1)
            os.kill(pid, signal.SIGINT)
            all_good = os.waitpid(pid, 0)

            self.assertTrue(all_good)

    def test_curve_multiple_values_same_time(self):
        '''addresses "Add support for multiple values on same timestamp for sp2.curve"'''

        @sp2.graph
        def g() -> sp2.Outputs(o1=sp2.ts[int], o2=sp2.ts[int], o3=sp2.ts[int]):
            values = [
                (timedelta(seconds=0), 0),
                (timedelta(seconds=0), 1),
                (timedelta(seconds=1), 2),
                (timedelta(seconds=2), 3),
                (timedelta(seconds=3), 4),
                (timedelta(seconds=3), 5),
                (timedelta(seconds=4), 6),
                (timedelta(seconds=5), 7),
                (timedelta(seconds=5), 8),
            ]
            return sp2.output(
                o1=sp2.curve(int, values),
                o2=sp2.curve(int, values, push_mode=PushMode.NON_COLLAPSING),
                o3=sp2.curve(int, values, push_mode=PushMode.LAST_VALUE),
            )

        res = sp2.run(g, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=5))
        for k in ("o1", "o2"):
            times, values = zip(*res[k])
            self.assertEqual(
                times, tuple(datetime(2020, 1, 1) + timedelta(seconds=s) for s in [0, 0, 1, 2, 3, 3, 4, 5, 5])
            )
            self.assertEqual(values, tuple(range(9)))
        times, values = zip(*res["o3"])
        self.assertEqual(times, tuple(datetime(2020, 1, 1) + timedelta(seconds=s) for s in [0, 1, 2, 3, 4, 5]))
        self.assertEqual(values, (1, 2, 3, 5, 6, 8))

    def test_engine_scheduling_order(self):
        @sp2.node
        def my_node(val: int) -> ts[int]:
            with sp2.alarms():
                a = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=0), val)
            if sp2.ticked(a):
                sp2.schedule_alarm(a, timedelta(seconds=1), val)
                return a

        @sp2.node
        def dummy(v: ts[int]) -> ts[int]:
            return v

        @sp2.graph(cache=True)
        def my_ranked_node(val: int, rank: int = 0) -> sp2.Outputs(val=ts[int]):
            res = my_node(val)
            for i in range(rank):
                res = dummy(res)
            return sp2.output(val=res)

        @sp2.graph
        def my_graph():
            n1 = sp2.curve(int, [(timedelta(seconds=i), 1) for i in range(6)])
            n2 = my_ranked_node(3).val
            n3 = my_ranked_node(6, 4).val
            n4 = my_ranked_node(5, 3).val
            n5 = sp2.curve(int, [(timedelta(seconds=i), 2) for i in range(6)])
            n6 = my_ranked_node(4).val
            sp2.add_graph_output("o", sp2.collect([n1, n2, n3, n4, n5, n6]))

        def verify_res(res):
            for t, l in res:
                self.assertEqual(l, [1, 2, 3, 4, 5, 6])

        verify_res(sp2.run(my_graph, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=5))["o"])

    def test_datetime_timedelta_ranges(self):
        """range check when converting datetime"""
        for d in [
            datetime(2020, 12, 24, 1, 2, 3, 123456),
            datetime(1970, 1, 1),
            datetime(1969, 5, 6, 2, 3, 4),
            datetime(1969, 5, 6, 2, 3, 4, 123456),
            # Edge cases, DateTime MIN / MAX
            datetime(1969, 12, 31, 23, 59, 59) if platform.system() == "Darwin" else datetime(1968, 1, 1),
            datetime(2261, 12, 31, 23, 59, 59, 999999),
            timedelta(days=1, seconds=3600, microseconds=123456),
            timedelta(days=-1, seconds=3600, microseconds=123456),
        ]:
            res = sp2.run(sp2.const(d), starttime=datetime(2020, 12, 24))[0][0][1]
            self.assertEqual(res, d, f"date: {d}")

        # Out of bounds
        with self.assertRaisesRegex(OverflowError, "datetime 1677-09-20 00:00:00 is out of range for sp2 datetime"):
            d1 = datetime(1677, 9, 20)
            sp2.run(sp2.const(d1), starttime=datetime(2020, 12, 24))

        with self.assertRaisesRegex(OverflowError, "datetime 2262-04-12 00:00:00 is out of range for sp2 datetime"):
            d2 = datetime(2262, 4, 12)
            sp2.run(sp2.const(d2), starttime=datetime(2020, 12, 24))

        with self.assertRaisesRegex(OverflowError, "timedelta 106752 days, 0:00:00 out of range for sp2 timedelta"):
            td = timedelta(days=106752)
            sp2.run(sp2.const(td), starttime=datetime(2020, 12, 24))

        with self.assertRaisesRegex(OverflowError, "timedelta -106752 days, 0:00:00 out of range for sp2 timedelta"):
            td = timedelta(days=-106752)
            sp2.run(sp2.const(td), starttime=datetime(2020, 12, 24))

    def test_realtime_endtime(self):
        from sp2.impl.pushadapter import PushInputAdapter
        from sp2.impl.wiring import py_push_adapter_def

        # Ensure engine exits at end time even if no events are coming in ( ensure its not exiting due to the queue wait time setting )
        adapter = py_push_adapter_def("adapter", PushInputAdapter, ts[int])
        sp2.run(
            adapter(),
            starttime=datetime.utcnow(),
            endtime=timedelta(seconds=0.5),
            realtime=True,
            queue_wait_time=timedelta(days=1),
        )

    def test_threaded_run(self):
        # simple test
        runner = sp2.run_on_thread(
            sp2.count, sp2.timer(timedelta(seconds=1)), starttime=datetime(2021, 4, 23), endtime=timedelta(seconds=60)
        )
        res = runner.join()[0]
        self.assertEqual(len(res), 60)
        # ensure stopping doesnt try to access dead push input adapter
        runner.stop_engine()

        # realtime
        @sp2.graph
        def g(count: int) -> sp2.ts[int]:
            x = sp2.count(sp2.timer(timedelta(seconds=0.1)))
            stop = x == count
            stop = sp2.filter(stop, stop)

            sp2.stop_engine(stop)
            return x

        runner = sp2.run_on_thread(g, 5, starttime=datetime.utcnow(), endtime=timedelta(seconds=60), realtime=True)
        res = runner.join()[0]
        self.assertEqual(len(res), 5)

        # midway stop
        runner = sp2.run_on_thread(g, 50000, starttime=datetime.utcnow(), endtime=timedelta(minutes=30), realtime=True)
        import time

        time.sleep(1)
        runner.stop_engine()
        res = runner.join()[0]
        self.assertLess(len(res), 1000)

        # exception handling
        @sp2.node
        def err(x: ts[object]):
            if sp2.ticked(x) and sp2.num_ticks(x) > 5:
                a = b

        runner = sp2.run_on_thread(err, sp2.timer(timedelta(seconds=0.01)), realtime=True)
        with self.assertRaisesRegex(RuntimeError, ""):
            runner.join()

    def test_int_to_float_ts_conversion(self):
        @sp2.node
        def eq(i: sp2.ts["T1"], f: sp2.ts["T2"]):
            self.assertEqual(float(i), float(f))

        @sp2.node
        def basket_wrapper(l: [sp2.ts[float]], d: {str: sp2.ts[float]}) -> sp2.Outputs(
            l=sp2.OutputBasket(typing.List[sp2.ts[float]], shape_of="l"),
            d=sp2.OutputBasket(typing.Dict[str, sp2.ts[float]], shape_of="d"),
        ):
            if sp2.ticked(l):
                ticked_value_types = set(map(type, l.tickedvalues()))
                self.assertEqual(len(ticked_value_types), 1)
                self.assertIs(next(iter(ticked_value_types)), float)
                sp2.output(l=dict(l.tickeditems()))
            if sp2.ticked(d):
                ticked_value_types = set(map(type, d.tickedvalues()))
                self.assertEqual(len(ticked_value_types), 1)
                self.assertIs(next(iter(ticked_value_types)), float)
                sp2.output(d=dict(d.tickeditems()))

        def g():
            c_int = sp2.count(sp2.timer(timedelta(seconds=1)))
            c_float = sp2.sample.using(T=float)(c_int, c_int)
            eq(c_int, c_float)
            basket_outputs = basket_wrapper([c_int], {"0": c_int, "1": c_int})
            eq(basket_outputs.l[0], c_float)
            eq(basket_outputs.d["0"], c_float)
            eq(basket_outputs.d["1"], c_float)

        sp2.run(
            g,
            starttime=datetime(
                2021,
                1,
                1,
            ),
            endtime=timedelta(seconds=10),
        )

    def test_outputs_with_dict_naming(self):
        # This was a bug where outputs named with dict properties, ie "values", would fail to be accessed on the Outputs object
        @sp2.node
        def foo(x: ts[int]) -> sp2.Outputs(values=ts[int]):
            sp2.output(values=x)

        def g():
            rv = foo(sp2.const(5))
            return rv.values

        rv = sp2.run(
            g,
            starttime=datetime(
                2021,
                1,
                1,
            ),
            endtime=timedelta(seconds=10),
        )
        self.assertEqual(rv[0][0][1], 5)

    def test_pass_none_as_ts(self):
        @sp2.node
        def n(a: sp2.ts[int], d: {int: sp2.ts[int]}, l: [sp2.ts[int]]) -> sp2.ts[int]:
            if sp2.ticked(a):
                return a + d[0] + l[0]

        @sp2.graph
        def g(a: sp2.ts[int], d: {int: sp2.ts[int]}, l: [sp2.ts[int]]) -> sp2.ts[int]:
            if a is not None:
                return a + d[0] + l[0]
            else:
                assert d is None
                assert l is None
                return sp2.const.using(T=int)(-1)

        @sp2.graph
        def main(use_graph: bool, pass_null: bool) -> sp2.Outputs(o=sp2.ts[int]):
            inst = g if use_graph else n

            if pass_null:
                return sp2.output(o=inst(None, None, None))
            else:
                return sp2.output(o=inst(sp2.const(1), {0: sp2.const(2)}, [sp2.const(3)]))

        res1 = sp2.run(
            main,
            True,
            False,
            starttime=datetime(
                2021,
                1,
                1,
            ),
            endtime=timedelta(seconds=10),
        )
        self.assertEqual(res1["o"][0][1], 6)
        res2 = sp2.run(
            main,
            True,
            True,
            starttime=datetime(
                2021,
                1,
                1,
            ),
            endtime=timedelta(seconds=10),
        )
        self.assertEqual(res2["o"][0][1], -1)
        res3 = sp2.run(
            main,
            False,
            False,
            starttime=datetime(
                2021,
                1,
                1,
            ),
            endtime=timedelta(seconds=10),
        )
        self.assertEqual(res3["o"][0][1], 6)
        with self.assertRaises(TSArgTypeMismatchError):
            sp2.run(
                main,
                False,
                True,
                starttime=datetime(
                    2021,
                    1,
                    1,
                ),
                endtime=timedelta(seconds=10),
            )

    def test_return_arg_mismatch(self):
        @sp2.graph
        def my_graph(x: sp2.ts[int]) -> sp2.ts[str]:
            return x

        with self.assertRaises(TSArgTypeMismatchError) as ctxt:
            sp2.run(my_graph, sp2.const(1), starttime=datetime.utcnow())
        self.assertEqual(str(ctxt.exception), "In function my_graph: Expected ts[str] for return value, got ts[int]")

        @sp2.graph
        def dictbasket_graph(x: sp2.ts[int]) -> {str: sp2.ts[str]}:
            return sp2.output({"a": x})

        with self.assertRaises(ArgTypeMismatchError) as ctxt:
            sp2.run(dictbasket_graph, sp2.const(1), starttime=datetime.utcnow())
        self.assertRegex(
            str(ctxt.exception),
            "In function dictbasket_graph: Expected typing\.Dict\[str, .* for return value, got \{'a': .* \(dict\)",
        )

        @sp2.graph
        def listbasket_graph(x: sp2.ts[int]) -> [sp2.ts[str]]:
            return sp2.output([x])

        with self.assertRaises(ArgTypeMismatchError) as ctxt:
            sp2.run(listbasket_graph, sp2.const(1), starttime=datetime.utcnow())
        self.assertRegex(
            str(ctxt.exception),
            "In function listbasket_graph: Expected typing\.List\[.* for return value, got \[.* \(list\)",
        )

    def test_global_context(self):
        try:

            @sp2.graph
            def g() -> sp2.ts[int]:
                return sp2.const(1)

            res1 = sp2.run(
                g,
                starttime=datetime(
                    2021,
                    1,
                    1,
                ),
                endtime=timedelta(seconds=10),
            )
            c = g()
            res2 = sp2.run(
                c,
                starttime=datetime(
                    2021,
                    1,
                    1,
                ),
                endtime=timedelta(seconds=10),
            )

            self.assertEqual(res1, res2)

            replace_b_with_c = False

            @sp2.graph
            def g() -> sp2.Outputs(a=sp2.ts[int], b=sp2.ts[int]):
                key = sp2.curve(
                    str, [(timedelta(seconds=i), v) for i, v in enumerate(["A", "B", "A", "A", "A", "B", "C", "B"])]
                )
                value = sp2.curve(int, [(timedelta(seconds=i), i) for i in range(8)])

                demux = sp2.DelayedDemultiplex(value, key)
                a = demux.demultiplex("A")
                if replace_b_with_c:
                    b = demux.demultiplex("C")
                else:
                    b = demux.demultiplex("B")
                return sp2.output(a=a, b=b)

            res1 = sp2.run(
                g,
                starttime=datetime(
                    2021,
                    1,
                    1,
                ),
                endtime=timedelta(seconds=10),
            )
            with self.assertRaisesRegex(RuntimeError, ".*Delayed node must be created under a wiring context.*"):
                outputs = g()
            sp2.new_global_context()
            outputs = g()
            res2a = sp2.run(
                outputs.a,
                starttime=datetime(
                    2021,
                    1,
                    1,
                ),
                endtime=timedelta(seconds=10),
            )
            self.assertEqual(res2a[0], res1["a"])
            res2b = sp2.run(
                outputs.b,
                starttime=datetime(
                    2021,
                    1,
                    1,
                ),
                endtime=timedelta(seconds=10),
            )
            self.assertEqual(res2b[0], res1["b"])
            sp2.clear_global_context()
            with self.assertRaisesRegex(RuntimeError, ".*Delayed node must be created under a wiring context.*"):
                outputs = g()
            c = sp2.new_global_context(False)
            with self.assertRaisesRegex(RuntimeError, ".*Delayed node must be created under a wiring context.*"):
                outputs = g()
            with c:
                outputs = g()
                res2a = sp2.run(
                    outputs.a,
                    starttime=datetime(
                        2021,
                        1,
                        1,
                    ),
                    endtime=timedelta(seconds=10),
                )
                self.assertEqual(res2a[0], res1["a"])
            with self.assertRaisesRegex(RuntimeError, ".*Delayed node must be created under a wiring context.*"):
                outputs = g()
        finally:
            sp2.clear_global_context()

    def test_unnamed_basket_return(self):
        @sp2.node
        def n(x: {str: sp2.ts["T"]}) -> sp2.OutputBasket(typing.Dict[str, sp2.ts["T"]], shape_of="x"):
            if sp2.ticked(x):
                return sp2.output({k: v for k, v in x.tickeditems()})

        @sp2.node
        def n2(x: [sp2.ts["T"]]) -> sp2.OutputBasket(typing.List[sp2.ts["T"]], shape_of="x"):
            if sp2.ticked(x):
                return sp2.output({k: v for k, v in x.tickeditems()})

        def g():
            res = n({"a": sp2.const("v1"), "b": sp2.const("v2")})
            res2 = n2(list(res.values()))
            sp2.add_graph_output("a", res["a"])
            sp2.add_graph_output("b", res["b"])
            sp2.add_graph_output("c", res2[0])
            sp2.add_graph_output("d", res2[1])

        res = sp2.run(g, starttime=datetime(2021, 1, 1), endtime=timedelta(seconds=1))
        self.assertEqual(
            res,
            {
                "a": [(datetime(2021, 1, 1, 0, 0), "v1")],
                "b": [(datetime(2021, 1, 1, 0, 0), "v2")],
                "c": [(datetime(2021, 1, 1, 0, 0), "v1")],
                "d": [(datetime(2021, 1, 1, 0, 0), "v2")],
            },
        )

    def test_delayed_edge(self):
        x = sp2.DelayedEdge(ts[int])
        with self.assertRaisesRegex(RuntimeError, "Encountered unbound DelayedEdge"):
            sp2.run(x, starttime=datetime.utcnow(), endtime=timedelta())

        self.assertFalse(x.is_bound())
        x.bind(sp2.const(123))
        self.assertTrue(x.is_bound())

        res = sp2.run(x, starttime=datetime.utcnow(), endtime=timedelta())[0][0][1]
        self.assertEqual(res, 123)

        with self.assertRaisesRegex(
            RuntimeError,
            r"Attempted to bind DelayedEdge multiple times, previously bound to output from node \"sp2.const\"",
        ):
            x.bind(sp2.const(456))

        # Type check
        with self.assertRaisesRegex(
            TypeError, re.escape(r"""Expected ts[T] for argument 'edge', got ts[int](T=str)""")
        ):
            y = sp2.DelayedEdge(ts[str])
            y.bind(sp2.const(123))

        # Null default
        z = sp2.DelayedEdge(ts[int], default_to_null=True)
        self.assertFalse(z.is_bound())
        res = sp2.run(z, starttime=datetime.utcnow(), endtime=timedelta())[0]
        self.assertEqual(len(res), 0)
        z.bind(sp2.const(123))
        res = sp2.run(z, starttime=datetime.utcnow(), endtime=timedelta())[0][0][1]
        self.assertEqual(res, 123)

        # Should raise at this point
        with self.assertRaisesRegex(
            RuntimeError,
            r"Attempted to bind DelayedEdge multiple times, previously bound to output from node \"sp2.const\"",
        ):
            x.bind(sp2.const(456))

    def test_cyclical_graph_error(self):
        """Ensure cyclical graphs generate clear errors, can occur with delayed bindings"""

        def g():
            a = sp2.DelayedCollect(int)
            b = sp2.DelayedCollect(int)

            a.add_input(sp2.unroll(b.output()))
            b.add_input(sp2.unroll(a.output()))

            sp2.add_graph_output("a", sp2.unroll(a.output()) - 5)

        with self.assertRaisesRegex(
            RuntimeError,
            r"Illegal cycle found in graph, path:\n\t\*\* unroll -> collect -> unroll -> collect -> unroll \*\*  -> _binary_op -> GraphOutputAdapter",
        ):
            sp2.run(g, starttime=datetime.utcnow(), endtime=timedelta())

    def test_delayed_edge_derived_type(self):
        class Base(sp2.Struct):
            a: int

        class Derived(Base):
            b: float

        test_self = self

        class MyDelayedNode(DelayedNodeWrapperDef):
            def __init__(self):
                super().__init__()
                self.output = sp2.DelayedEdge(sp2.ts[Base])

            def copy(self):
                raise NotImplementedError()

            def _instantiate(self):
                with test_self.assertRaises(TypeError):
                    self.output.bind(sp2.const(1))

                self.output.bind(sp2.const(Derived(a=1, b=2)))

        @sp2.graph
        def g() -> sp2.ts[Base]:
            return MyDelayedNode().output

        res = sp2.run(g, starttime=datetime.utcnow(), endtime=timedelta())[0][0][1]
        self.assertEqual(res, Derived(a=1, b=2))

    def test_realtime_flag(self):
        def g(expected_realtime: bool):
            self.assertEqual(expected_realtime, sp2.is_configured_realtime())

        sp2.run(g, False, starttime=datetime.utcnow(), endtime=timedelta())
        sp2.run(g, True, starttime=datetime.utcnow(), endtime=timedelta(), realtime=True)

    def test_graph_shape_bug(self):
        """Address an assertion error bug that we had on returning list baskets with specified shape"""

        @sp2.graph
        def aux(x: [ts[float]], y: {str: ts[float]}) -> sp2.Outputs(
            o1=sp2.OutputBasket(typing.List[ts[float]], shape_of="x"),
            o2=sp2.OutputBasket(typing.Dict[str, ts[float]], shape_of="y"),
        ):
            return sp2.output(o1=x, o2=y)

        @sp2.graph
        def g() -> (
            sp2.Outputs(o1=sp2.OutputBasket(typing.List[ts[float]]), o2=sp2.OutputBasket(typing.Dict[str, ts[float]]))
        ):
            res = aux([sp2.const(1.0), sp2.const(2.0)], {"3": sp2.const(3.0), "4": sp2.const(4.0)})
            return sp2.output(o1=res.o1, o2=res.o2)

        res = sp2.run(g, starttime=datetime.now(), endtime=timedelta(seconds=10))
        self.assertEqual([v[0][1] for v in res.values()], [1.0, 2.0, 3.0, 4.0])

    def test_graph_node_pickling(self):
        """Checks for a bug that we had when transitioning to python 3.8 - the graphs and nodes became unpicklable
        :return:
        """
        from sp2.tests.test_engine import _dummy_graph, _dummy_graph_cached, _dummy_node, _dummy_node_cached

        self.assertEqual(_dummy_graph, pickle.loads(pickle.dumps(_dummy_graph)))
        self.assertEqual(_dummy_node, pickle.loads(pickle.dumps(_dummy_node)))
        self.assertEqual(_dummy_graph_cached, pickle.loads(pickle.dumps(_dummy_graph_cached)))
        self.assertEqual(_dummy_node_cached, pickle.loads(pickle.dumps(_dummy_node_cached)))

    def test_memoized_object(self):
        @sp2.sp2_memoized
        def my_data():
            return object()

        @sp2.node
        def my_node() -> sp2.ts[object]:
            with sp2.alarms():
                a = sp2.alarm(bool)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(), True)
            if sp2.ticked(a):
                return my_data()

        @sp2.graph
        def g() -> sp2.Outputs(o1=sp2.ts[object], o2=sp2.ts[object]):
            return sp2.output(o1=sp2.const(my_data()), o2=my_node())

        res = sp2.run(g, starttime=datetime.now(), endtime=timedelta(seconds=10))
        self.assertEqual(id(res["o1"][0][1]), id(res["o2"][0][1]))

    def test_separate_graph_build_and_run(self):
        @sp2.graph
        def g() -> sp2.ts[int]:
            return sp2.const(1)

        s = datetime.now()
        e = timedelta(seconds=10)

        g_built1 = build_graph(g)
        # Should be fine to run graph that was built without start or end time
        sp2.run(g_built1, starttime=s, endtime=e)

        with self.assertRaisesRegex(
            AssertionError,
            "Start time and end time should either both be specified or none of them should be specified when building a graph",
        ):
            g_built1 = build_graph(g, starttime=s)
        with self.assertRaisesRegex(
            AssertionError,
            "Start time and end time should either both be specified or none of them should be specified when building a graph",
        ):
            g_built1 = build_graph(g, endtime=e)

        g_built2 = build_graph(g, starttime=s, endtime=e)
        # Both of those should be fine
        sp2.run(g_built2, starttime=s, endtime=e)
        sp2.run(g_built2, starttime=s, endtime=s + e)

        with self.assertRaisesRegex(AssertionError, "Trying to run graph on period.*while it was built for.*"):
            sp2.run(g_built2, starttime=s, endtime=e + timedelta(seconds=1))

    def test_graph_kwargs_return(self):
        @sp2.node
        def f(x: ts[int]) -> sp2.Outputs(a=ts[int], b=ts[int]):
            if sp2.ticked(x):
                return sp2.output(a=x, b=x + 2)

        @sp2.graph
        def g(x: ts[int]) -> sp2.Outputs(a=ts[int], b=ts[int]):
            return sp2.output(**f(x))

        res = sp2.run(g, sp2.const(1), starttime=datetime.utcnow(), endtime=timedelta())
        self.assertEqual(res["a"][0][1], 1)
        self.assertEqual(res["b"][0][1], 3)

        # Error testing
        with self.assertRaisesRegex(
            sp2.Sp2ParseError, "only unpacking of other sp2.node or sp2.graph calls are allowed"
        ):

            @sp2.graph
            def g2() -> sp2.Outputs(x=ts[int]):
                return sp2.output(**{})

        with self.assertRaisesRegex(sp2.Sp2ParseError, "f outputs dont align with graph outputs"):

            @sp2.graph
            def g3() -> sp2.Outputs(x=ts[int]):
                return sp2.output(**f(sp2.const(1)))

        def some_func():
            return {}

        with self.assertRaisesRegex(
            sp2.Sp2ParseError, "only unpacking of other sp2.node or sp2.graph calls are allowed"
        ):

            @sp2.graph
            def g4() -> sp2.Outputs(x=ts[int]):
                return sp2.output(**some_func())

        pass

    def test_scheduler_exception(self):
        '''was a bug "scheduler accounting is off when callbacks throw"'''

        from sp2.impl.pulladapter import PullInputAdapter
        from sp2.impl.wiring import py_pull_adapter_def

        class MyPullAdapterImpl(PullInputAdapter):
            def __init__(self):
                self._next_time = None
                self._c = 0
                super().__init__()

            def start(self, start_time, end_time):
                super().start(start_time, end_time)
                self._next_time = start_time

            def next(self):
                self._c += 1
                time = self._next_time
                self._next_time += timedelta(seconds=1)
                if self._c > 10:
                    raise RuntimeError("all good")
                return time, self._c

        MyPullAdapter = py_pull_adapter_def("MyPullAdapter", MyPullAdapterImpl, ts[int])

        @sp2.node
        def my_node(x: ts[object]):
            with sp2.alarms():
                a = sp2.alarm(object)

            if sp2.ticked(x):
                sp2.schedule_alarm(a, timedelta(seconds=1), [1, 2, 3, "a"])

        def g():
            with sp2.memoize(False):
                for i in range(3):
                    c = sp2.count(sp2.timer(timedelta(seconds=1), True))
                    my_node(c)
                    data = MyPullAdapter()
                    sp2.add_graph_output(str(i), data)

        with self.assertRaisesRegex(RuntimeError, "all good"):
            sp2.run(g, starttime=datetime(2023, 1, 1), endtime=timedelta(1))


if __name__ == "__main__":
    unittest.main()
