import itertools
import numpy
import random
import string
import time
import unittest
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List

import sp2
from sp2 import ts


class DynData(sp2.Struct):
    key: str
    val: int


@sp2.node
def gen_basket(keys: ts[[str]], deletes: ts[[str]]) -> sp2.DynamicBasket[str, DynData]:
    with sp2.state():
        s_counts = defaultdict(int)
    if sp2.ticked(keys):
        for key in keys:
            s_counts[key] += 1
            sp2.output({key: DynData(key=key, val=s_counts[key])})

    if sp2.ticked(deletes):
        for key in deletes:
            sp2.remove_dynamic_key(key)


@sp2.node
def random_keys(keys: [str], interval: timedelta, repeat: bool) -> ts[[str]]:
    with sp2.alarms():
        x = sp2.alarm(int)
    with sp2.state():
        s_keys = list(keys)

    with sp2.start():
        sp2.schedule_alarm(x, interval, 0)

    if sp2.ticked(x):
        count = min(random.randint(1, 5), len(s_keys))
        res = list(numpy.random.choice(s_keys, count, replace=False))
        if not repeat:
            for k in res:
                s_keys.remove(k)

        if s_keys:
            sp2.schedule_alarm(x, interval, 0)

        return res


@sp2.node
def delayed_deletes(keys: ts[[str]], delay: timedelta) -> ts[[str]]:
    with sp2.alarms():
        delete = sp2.alarm([str])
    with sp2.state():
        s_pending = set()

    if sp2.ticked(keys):
        deletes = []
        for k in keys:
            if k not in s_pending:
                s_pending.add(k)
                deletes.append(k)
        if deletes:
            sp2.schedule_alarm(delete, delay, deletes)

    if sp2.ticked(delete):
        for key in delete:
            s_pending.remove(key)
        return delete


class TestDynamic(unittest.TestCase):
    def setUp(self):
        seed = int(time.time())
        print("SEEDING with", seed)
        numpy.random.seed(seed)
        random.seed(seed)

    def test_start_stop_dynamic(self):
        started = {}
        stopped = {}

        @sp2.node
        def start_stop(key: str, x: ts[object]):
            with sp2.start():
                started[key] = True

            with sp2.stop():
                stopped[key] = True

            if sp2.ticked(x):
                pass

        @sp2.graph
        def dyn_graph(key: str):
            start_stop(key, sp2.const(1))

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), True)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, sp2.snapkey())
            sp2.add_graph_output("keys", keys)

        res = sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        actual_keys = set(itertools.chain.from_iterable(v[1] for v in res["keys"]))
        self.assertEqual(set(started.keys()), actual_keys)
        self.assertEqual(set(stopped.keys()), actual_keys)

    def test_clean_shutdown(self):
        """ensure inputs are cleaned up on shutdown by triggering events past shutdown"""

        @sp2.graph
        def dyn_graph(key: str):
            # const delay
            sp2.add_graph_output(f"{key}_const", sp2.merge(sp2.const(1), sp2.const(2, delay=timedelta(seconds=10))))

            # timer
            sp2.add_graph_output(f"{key}_timer", sp2.timer(timedelta(seconds=1)))

            # pull adapter
            data = [(timedelta(seconds=n + 1), n) for n in range(100)]
            sp2.add_graph_output(f"{key}_pull", sp2.curve(int, data))

            # node with alarm
            sp2.add_graph_output(
                f"{key}_alarm",
                sp2.merge(sp2.delay(sp2.const(1), timedelta(seconds=1)), sp2.delay(sp2.const(2), timedelta(seconds=1))),
            )

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            deletes = sp2.delay(keys, timedelta(seconds=5.1))

            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, deletes)
            sp2.dynamic(basket, dyn_graph, sp2.snapkey())

        res = sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        actual_keys = set(itertools.chain.from_iterable(v[1] for v in res["keys"]))
        for key in actual_keys:
            self.assertEqual(len(res[f"{key}_const"]), 1)
            self.assertEqual(len(res[f"{key}_alarm"]), 1)
            self.assertEqual(len(res[f"{key}_timer"]), 5)
            self.assertEqual(len(res[f"{key}_pull"]), 5)

    def test_dynamic_args(self):
        """test various "special" arguments"""

        @sp2.graph
        def dyn_graph(key: str, val: [str], key_ts: ts[DynData], scalar: str):
            sp2.add_graph_output(f"{key}_key", sp2.const(key))
            sp2.add_graph_output(f"{key}_val", sp2.const(val))
            sp2.add_graph_output(f"{key}_ts", key_ts)
            sp2.add_graph_output(f"{key}_scalar", sp2.const(scalar))

            # Lets add some actual nodes to the graph!
            # Force an initial tick so it aligns with add_graph_output data
            key_ts = sp2.merge(key_ts, sp2.sample(sp2.const(1), key_ts))
            sp2.add_graph_output(f"{key}_tsadj", key_ts.val * 2)

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), True)
            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, sp2.snapkey(), sp2.snap(keys), sp2.attach(), "hello world!")

        res = sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        actual_keys = set(itertools.chain.from_iterable(v[1] for v in res["keys"]))
        for key in actual_keys:
            self.assertEqual(res[f"{key}_key"][0][1], key)
            # val is snap of list of keys when created, just assert key is in the list
            self.assertIn(key, res[f"{key}_val"][0][1])
            self.assertEqual(res[f"{key}_scalar"][0][1], "hello world!")
            ts_ticks = len(res[f"{key}_ts"])
            self.assertGreater(ts_ticks, 0)
            self.assertEqual(
                [v[1] for v in res[f"{key}_ts"]], [DynData(key=key, val=n) for n in range(1, ts_ticks + 1)]
            )
            self.assertEqual(len(res[f"{key}_tsadj"]), ts_ticks)
            self.assertTrue(all(x[1].val * 2 == y[1] for x, y in zip(res[f"{key}_ts"], res[f"{key}_tsadj"])))

    def test_shared_input(self):
        """ensure an externally wired input is shared / not recreated per sub-graph"""
        instances = []

        @sp2.node
        def source_node() -> ts[int]:
            with sp2.alarms():
                x = sp2.alarm(int)
            with sp2.start():
                print("There can be only one!")
                instances.append(1)
                sp2.schedule_alarm(x, timedelta(seconds=1), 1)

            if sp2.ticked(x):
                sp2.schedule_alarm(x, timedelta(seconds=1), x + 1)
                return x

        @sp2.graph
        def dyn_graph(key: str, x: ts[int]):
            sp2.add_graph_output(key, x * x)

        def g():
            s = source_node()
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), True)
            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, sp2.snapkey(), s)

        sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        self.assertEqual(len(instances), 1)

        ## There was a bug where nodes creates outside of run would register in the global memcache
        # and then get picked up in dynamic, which would then find it in memo.  Ensure it doesnt break
        # when passing potentially globally memoized edges directly into dynamic
        # Force memoizing sp2.timer(Timedelta(seconds=1)) in global cache
        _ = sp2.timer(timedelta(seconds=1))

        @sp2.graph
        def dyn_graph(key: str, x: ts[int]):
            sp2.add_graph_output(key, x * x)
            sp2.add_graph_output(key + "_timer", sp2.count(sp2.timer(timedelta(seconds=1))))

        def g():
            s = sp2.count(sp2.timer(timedelta(seconds=1)))
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            deletes = sp2.delay(keys, timedelta(seconds=2.1))
            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, deletes)
            sp2.dynamic(basket, dyn_graph, sp2.snapkey(), s)

        sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))

    def test_dynamic_outputs(self):
        @sp2.graph
        def dyn_graph_named(key: str) -> sp2.Outputs(k=ts[DynData], v=ts[int]):
            v = sp2.count(sp2.timer(timedelta(seconds=1)))
            k = DynData.fromts(key=sp2.const(key, delay=timedelta(seconds=1)), val=v * 2)
            return sp2.output(k=k, v=v)

        @sp2.graph
        def dyn_graph_unnamed(key: str) -> ts[DynData]:
            v = sp2.count(sp2.timer(timedelta(seconds=1)))
            return DynData.fromts(key=sp2.const(key, delay=timedelta(seconds=1)), val=v * 3)

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            deletes = sp2.delay(keys, timedelta(seconds=5.1))
            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, deletes)
            res = sp2.dynamic(basket, dyn_graph_named, sp2.snapkey())
            res2 = sp2.dynamic(basket, dyn_graph_unnamed, sp2.snapkey())

            sp2.add_graph_output("k", sp2.dynamic_collect(res.k))
            sp2.add_graph_output("v", sp2.dynamic_collect(res.v))
            sp2.add_graph_output("unnamed", sp2.dynamic_collect(res2))

        res = sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        self.assertEqual(len(res["k"]), len(res["v"]))
        self.assertEqual(len(res["k"]), len(res["unnamed"]))

        cache = defaultdict(lambda: 1)
        for r in res["k"]:
            for k, v in r[1].items():
                self.assertEqual(k, v.key)
                self.assertEqual(cache[k] * 2, v.val)
                cache[k] += 1

        cache = defaultdict(lambda: 1)
        for r in res["v"]:
            for k, v in r[1].items():
                self.assertEqual(cache[k], v)
                cache[k] += 1

        cache = defaultdict(lambda: 1)
        for r in res["unnamed"]:
            for k, v in r[1].items():
                self.assertEqual(k, v.key)
                self.assertEqual(cache[k] * 3, v.val)
                cache[k] += 1

    def test_add_remove_add(self):
        @sp2.graph
        def dyn_graph(key: str, version: int, x: ts[int]):
            key = f"{key}_{version}"
            sp2.add_graph_output(key, DynData.fromts(key=sp2.const(key), val=x * x))

        def g():
            c = sp2.count(sp2.timer(timedelta(seconds=1)))
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), True)
            # keys = sp2.const.using(T=[str])( ['A'], delay=timedelta(seconds=1) )
            deletes = delayed_deletes(keys, timedelta(seconds=3.1))
            basket = gen_basket(keys, deletes)
            sp2.dynamic(basket, dyn_graph, sp2.snapkey(), sp2.snap(sp2.count(keys)), c)

        res = sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        for k, v in res.items():
            for tick in v:
                self.assertEqual(tick[1].key, k)

    def test_nested_dynamics(self):
        @sp2.graph
        def dyn_graph_inner(parent_key: str, key: str, x: ts[int]) -> ts[DynData]:
            key = "_".join([parent_key, key])

            const_key = sp2.sample(sp2.firstN(x, 1), sp2.const(key))
            v = DynData.fromts(key=const_key, val=x * x)
            sp2.add_graph_output(key, v)
            sp2.add_graph_output(key + "_alarm", sp2.count(sp2.timer(timedelta(seconds=1))))
            return v

        @sp2.graph
        def dyn_graph(key: str, x: ts[int]) -> ts[{str: DynData}]:
            keys = random_keys(list("ABC"), timedelta(seconds=0.5), False)
            deletes = delayed_deletes(keys, timedelta(seconds=1.1))
            basket = gen_basket(keys, deletes)
            res = sp2.dynamic(basket, dyn_graph_inner, key, sp2.snapkey(), x)
            v = sp2.dynamic_collect(res)
            return v

        def g():
            c = sp2.count(sp2.timer(timedelta(seconds=1)))
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            deletes = delayed_deletes(keys, timedelta(seconds=3.1))

            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, deletes)
            res = sp2.dynamic(basket, dyn_graph, sp2.snapkey(), c)
            sp2.add_graph_output("all", sp2.dynamic_collect(res))

            # sp2.print('keys', keys)
            # sp2.print('deletes',deletes)

        res = sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=60))
        for t, v in res["all"]:
            for parent_key, child in v.items():
                for key, data in child.items():
                    self.assertEqual("_".join([parent_key, key]), data.key)

    def test_stop_engine_dynamic(self):
        @sp2.node
        def on_stop(key: str, x: ts[object]):
            if sp2.ticked(x):
                sp2.stop_engine(dynamic=True)

        @sp2.graph
        def dyn_graph(key: str) -> ts[int]:
            sp2.stop_engine(sp2.const(1, delay=timedelta(seconds=2)), True)
            return sp2.const(1)

        @sp2.node
        def assert_destruction_time(dyn_output: {ts[str]: ts[object]}):
            with sp2.state():
                s_added = {}

            if sp2.ticked(dyn_output.shape):
                for k in dyn_output.shape.added:
                    s_added[k] = sp2.now()
                for k in dyn_output.shape.removed:
                    # Assert we were shutdown after 3 2 seconds ( sp2.stop_engine call ) not after 5.1 ( key removal )
                    self.assertEqual(sp2.now() - s_added[k], timedelta(seconds=2))

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            deletes = sp2.delay(keys, timedelta(seconds=5.1))
            basket = gen_basket(keys, deletes)
            res = sp2.dynamic(basket, dyn_graph, sp2.snapkey())
            assert_destruction_time(res)

        sp2.run(g, starttime=datetime(2021, 6, 22), endtime=timedelta(seconds=30))

    def test_initial_ticks(self):
        @sp2.node
        def do_assert(tag: str, x: ts[object], expect_tick: bool):
            with sp2.alarms():
                start = sp2.alarm(int)
            with sp2.state():
                s_ticked = False

            with sp2.start():
                sp2.schedule_alarm(start, timedelta(), True)

            if sp2.ticked(start):
                self.assertEqual(sp2.ticked(x), expect_tick, tag)

        @sp2.node
        def assert_multiple_alarm():
            with sp2.alarms():
                a = sp2.alarm(bool)
            with sp2.state():
                s_alarm_count = 0

            with sp2.start():
                for _ in range(10):
                    sp2.schedule_alarm(a, timedelta(), True)

            with sp2.stop():
                self.assertEqual(s_alarm_count, 10)

            if sp2.ticked(a):
                s_alarm_count += 1

        @sp2.graph
        def dyn_graph(x: ts[object], y: ts[object], z: ts[object]):
            do_assert("x", x, True)  # sp2.attach edge
            do_assert("y", y, True)  # sp2.timer edge
            do_assert("z", z, False)  # timer not on start

            do_assert("const", sp2.const(1), True)
            do_assert("curve", sp2.curve(int, [(timedelta(), 1)]), True)

            assert_multiple_alarm()

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(
                basket, dyn_graph, sp2.attach(), sp2.timer(timedelta(seconds=1)), sp2.timer(timedelta(seconds=0.17))
            )
            sp2.add_graph_output("keys", keys)

        sp2.run(g, starttime=datetime(2021, 6, 28), endtime=timedelta(seconds=10))

        # This was a bug where initial tick processing was dropping externally scheduled events on now that were deferred
        @sp2.graph
        def dyn(s: str):
            sp2.add_graph_output(f"tick_{s}", sp2.const(s))

        @sp2.graph
        def main():
            sym_ts = sp2.flatten([sp2.const("A"), sp2.const("B")])
            demuxed_data = sp2.dynamic_demultiplex(sym_ts, sym_ts)
            sp2.dynamic(demuxed_data, dyn, sp2.snapkey())
            sp2.add_graph_output("sym_ts", sym_ts)

        res = sp2.run(main, starttime=datetime(2021, 6, 7), endtime=timedelta(seconds=20))["sym_ts"]
        self.assertEqual([v[1] for v in res], ["A", "B"])

    def test_exceptions(self):
        # snap / attach in container
        @sp2.graph
        def dyn_graph(k: [str]):
            pass

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, [sp2.snapkey()])

        with self.assertRaisesRegex(TypeError, "sp2.snap and sp2.attach are not supported as members of containers"):
            sp2.run(g, starttime=datetime(2021, 6, 28), endtime=timedelta(seconds=10))

        # dynamic basket outputs
        @sp2.graph
        def dyn_graph(k: str) -> [ts[int]]:
            return [sp2.const(1)]

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, sp2.snapkey())

        with self.assertRaisesRegex(TypeError, "sp2.dynamic does not support basket outputs of sub_graph"):
            sp2.run(g, starttime=datetime(2021, 6, 28), endtime=timedelta(seconds=10))

        # duplicate output keys
        @sp2.graph
        def dyn_graph(k: str):
            sp2.add_graph_output("duplicate", sp2.const(1))

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, sp2.snapkey())

        with self.assertRaisesRegex(ValueError, 'graph output key "duplicate" is already bound'):
            sp2.run(g, starttime=datetime(2021, 6, 28), endtime=timedelta(seconds=10))

        # sp2.snap on invalid input
        @sp2.graph
        def dyn_graph(snap: int):
            pass

        def g():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), False)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn_graph, sp2.snap(sp2.null_ts(int)))

        with self.assertRaisesRegex(RuntimeError, "sp2.snap input \\( sub_graph arg 0 \\) is not valid"):
            sp2.run(g, starttime=datetime(2021, 6, 28), endtime=timedelta(seconds=10))

    def test_dynamic_with_self_reference(self):
        # This test ensures that triggers and processes can be driven by functions attached
        # to an object instance, because dynamic's do special argument parsing to inject
        # snapkey, snap, attach, etc
        class Container:
            @sp2.node
            def trigger(self, x: ts[str]) -> sp2.DynamicBasket[str, str]:
                if sp2.ticked(x):
                    return {x: x}

            @sp2.graph
            def process(self, key: str) -> ts[bool]:
                return sp2.const(True)

            @sp2.graph
            def main_graph(self):
                data = sp2.curve(
                    str,
                    [
                        (timedelta(seconds=0), "a"),
                        (timedelta(seconds=1), "b"),
                        (timedelta(seconds=2), "a"),
                        (timedelta(seconds=3), "c"),
                        (timedelta(seconds=4), "a"),
                    ],
                )
                dyn_data = sp2.dynamic(self.trigger(data), self.process, sp2.snapkey())
                sp2.print("Results: ", data)

        c = Container()
        sp2.run(c.main_graph, starttime=datetime.utcnow().replace(microsecond=0), endtime=timedelta(seconds=10))


if __name__ == "__main__":
    unittest.main()
