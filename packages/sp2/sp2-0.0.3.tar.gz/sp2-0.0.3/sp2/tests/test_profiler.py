import numpy as np
import os
import pandas as pd
import pytz
import string
import tempfile
import time as Time
import unittest
from datetime import date, datetime, time, timedelta
from functools import reduce

import sp2
import sp2.stats as stats
from sp2 import profiler, ts
from sp2.tests.test_dynamic import DynData, gen_basket, random_keys

from .test_showgraph import _cant_find_graphviz


@sp2.graph
def stats_graph():
    # Larger graph, run for many cycles
    # Test: utilization, exec_counts, cycle_count
    # Also ensure: max and avg times are not equal for all nodes
    x = sp2.count(sp2.timer(timedelta(seconds=1)))
    y = sp2.count(sp2.timer(timedelta(seconds=2)))

    s = stats.sum(x, trigger=sp2.timer(timedelta(seconds=5)))
    k = stats.kurt(y, trigger=sp2.timer(timedelta(seconds=10)))

    sp2.add_graph_output("s", s)
    sp2.add_graph_output("k", k)


st = datetime(2020, 1, 1)


class TestProfiler(unittest.TestCase):
    def test_graph_info(self):
        @sp2.graph
        def graph1():
            x0 = sp2.timer(timedelta(seconds=1), 1)
            x1 = sp2.timer(timedelta(seconds=1), 2)
            x2 = sp2.timer(timedelta(seconds=1), 3)
            x3 = sp2.timer(timedelta(seconds=1), True)

            x4 = sp2.filter(x3, x0)
            x5 = sp2.filter(x3, x1)
            x6 = sp2.filter(x3, x2)

            x7 = sp2.merge(x4, x5)
            x8 = sp2.merge(x4, x6)

            sp2.add_graph_output("x7", x7)
            sp2.add_graph_output("x8", x8)

        graph_info = sp2.profiler.graph_info(graph1)
        self.assertEqual(graph_info.node_count, 11)
        self.assertEqual(graph_info.edge_count, 12)
        self.assertEqual(len(graph_info.longest_path), 4)
        self.assertEqual(graph_info.longest_path[0], "sp2.timer")
        self.assertEqual(graph_info.longest_path[-1], "add_graph_output")
        self.assertEqual(graph_info.most_common_node()[0], "sp2.timer")
        self.assertEqual(graph_info.nodetype_counts["sp2.timer"], 4)
        self.assertEqual(graph_info.nodetype_counts["filter"], 3)
        self.assertEqual(graph_info.nodetype_counts["merge"], 2)
        self.assertEqual(graph_info.nodetype_counts["add_graph_output"], 2)

        @sp2.graph
        def graph_fb():
            # has some feedback connections
            x0 = sp2.timer(timedelta(seconds=1), 5)

            reset_feedback = sp2.feedback(bool)
            s = stats.sum(x0, 25, reset=reset_feedback.out())
            reset_signal = sp2.gt(s, sp2.const(100))  # reset sum whenever its greater than 100
            reset_feedback.bind(reset_signal)
            sp2.add_graph_output("s", s)

        graph_info = sp2.profiler.graph_info(graph_fb)
        self.assertEqual(graph_info.node_count, 15)
        self.assertEqual(graph_info.edge_count, 21)
        self.assertEqual(len(graph_info.longest_path), 7)
        self.assertEqual(graph_info.longest_path[0], "sp2.timer")
        self.assertEqual(graph_info.longest_path[-1], "FeedbackOutputDef")
        self.assertEqual(graph_info.nodetype_counts["sp2.timer"], 1)
        self.assertEqual(graph_info.nodetype_counts["FeedbackInputDef"], 1)
        self.assertEqual(graph_info.nodetype_counts["FeedbackOutputDef"], 1)

    def test_profile(self):
        @sp2.node
        def sleep_for(t: ts[float]) -> ts[bool]:
            Time.sleep(t)
            return True

        # # # # # #
        # Test timing
        @sp2.graph
        def graph1():
            # sleep for 1 second, 2 times
            x = sp2.timer(timedelta(seconds=1), 1.0)
            sleep = sleep_for(x)
            sp2.add_graph_output("sleep", sleep)

        with profiler.Profiler() as p:
            results = sp2.run(graph1, starttime=st, endtime=st + timedelta(seconds=2))

        prof = p.results()

        self.assertGreater(prof.average_cycle_time, 1.0)
        self.assertGreater(prof.max_cycle_time, 1.0)
        self.assertGreater(prof.node_stats["sleep_for"]["total_time"], 2.0)
        self.assertGreater(prof.node_stats["sleep_for"]["max_time"], 1.0)
        self.assertEqual(prof.node_stats["sleep_for"]["executions"], 2)
        self.assertEqual(prof.cycle_count, 2)
        self.assertEqual(prof.utilization, 1.0)  # profile node not included

        # tested to ensure profile=False afterwards

        with profiler.Profiler() as p:
            results = sp2.run(stats_graph, starttime=st, endtime=st + timedelta(seconds=100))

        prof = p.results()

        # Cycles: 1 per seconds => 100
        # count, cast_int_to_float, time_window_updates: 1 per second + 1 per 2 seconds => 150
        # sum:  1 per 5 seconds + 1 at the first tick => 21
        # kurt: 1 per 10 seconds + 1 at the first tick => 11
        # total _compute execs: sum + kurt = 32
        # Util. = 482 / (9 * 100)

        self.assertEqual(prof.cycle_count, 100)
        self.assertEqual(prof.node_stats["count"]["executions"], 150)
        self.assertEqual(prof.node_stats["cast_int_to_float"]["executions"], 150)
        self.assertEqual(prof.node_stats["_time_window_updates"]["executions"], 150)
        self.assertEqual(prof.node_stats["_compute"]["executions"], 32)
        self.assertEqual(prof.utilization, 4.82 / 9)
        self.assertEqual(prof.graph_info, profiler.graph_info(stats_graph))

        # From test_dynamic.py
        @sp2.graph
        def dyn(key: str, val: [str], key_ts: ts[DynData], scalar: str):
            sp2.add_graph_output(f"{key}_key", sp2.const(key))
            sp2.add_graph_output(f"{key}_val", sp2.const(val))
            sp2.add_graph_output(f"{key}_ts", key_ts)
            sp2.add_graph_output(f"{key}_scalar", sp2.const(scalar))
            key_ts = sp2.merge(key_ts, sp2.sample(sp2.const(1), key_ts))
            sp2.add_graph_output(f"{key}_tsadj", key_ts.val * 2)

        def graph3():
            keys = random_keys(list(string.ascii_uppercase), timedelta(seconds=1), True)
            sp2.add_graph_output("keys", keys)
            basket = gen_basket(keys, sp2.null_ts([str]))
            sp2.dynamic(basket, dyn, sp2.snapkey(), sp2.snap(keys), sp2.attach(), "hello world!")

        with profiler.Profiler() as p:
            results = sp2.run(graph3, starttime=st, endtime=st + timedelta(seconds=100))
            if not _cant_find_graphviz():
                with tempfile.NamedTemporaryFile(prefix="foo", suffix=".png", mode="w") as temp_file:
                    temp_file.close()
                    sp2.show_graph(graph3, graph_filename=temp_file.name)

        prof = p.results()
        self.assertEqual(prof.cycle_count, 100)
        self.assertEqual(prof.node_stats["dynamic<dyn>"]["executions"], 100)
        self.assertEqual(prof.node_stats["gen_basket"]["executions"], 100)
        self.assertTrue("sample" in prof.node_stats)
        self.assertTrue("merge" in prof.node_stats)
        self.assertEqual("dynamic<dyn>", prof.max_time_node()[0])  # dynamic graph must take longest time as a "node"

        # test print stats
        prof.format_stats(sort_by="total_time", max_nodes=100)

        # test dump and load
        with tempfile.NamedTemporaryFile(prefix="foo", suffix=".p", mode="w") as temp_file:
            temp_file.close()

            prof.dump_stats(temp_file.name)
            p2 = prof.load_stats(temp_file.name)
        self.assertEqual(prof, p2)

    def test_node_names(self):
        # There was an issue where the baselib math ops were showing up with their generic names rather than overridden name
        with profiler.Profiler() as p:
            x = sp2.const(1) + 2
            sp2.run(x, starttime=datetime(2022, 8, 11), endtime=timedelta(seconds=1))

        self.assertTrue("add" in p.results().graph_info.nodetype_counts)
        # self.assertTrue('add' in p.results().node_stats )

        with profiler.Profiler() as p:
            x = sp2.const("1") + "2"
            sp2.run(x, starttime=datetime(2022, 8, 11), endtime=timedelta(seconds=1))

        self.assertTrue("add" in p.results().graph_info.nodetype_counts)
        self.assertTrue("add" in p.results().node_stats)

    def test_file_output(self):
        cycle_fn = f"cycle_data_{os.getpid()}.csv"
        node_fn = f"node_data_{os.getpid()}.csv"
        with profiler.Profiler(cycle_file=cycle_fn, node_file=node_fn) as p:
            results = sp2.run(stats_graph, starttime=st, endtime=st + timedelta(seconds=100))

        # Verify that the files are proper, then clear them
        prof_info = p.results()

        with open(cycle_fn, "r") as f:
            lines = f.readlines()
            self.assertEqual(prof_info.cycle_count, len(lines[1:]))  # need to subtract one for column names
            file_act = sum([float(x) for x in lines[1:]]) / len(lines[1:])

        with open(node_fn, "r") as f:
            self.assertEqual(
                reduce(lambda a, b: a + b["executions"], prof_info.node_stats.values(), 0), len(f.readlines()) - 1
            )

        # Assert average cycle time is correct
        np.testing.assert_almost_equal(prof_info.average_cycle_time, file_act, decimal=6)

        # Make sure both can be read as csv
        df_node = pd.read_csv(node_fn)
        df_cycle = pd.read_csv(cycle_fn)
        max_times = df_node.groupby("Node Type").max().reset_index()
        self.assertEqual(
            round(prof_info.node_stats["cast_int_to_float"]["max_time"], 4),
            round(float(max_times.loc[max_times["Node Type"] == "cast_int_to_float"]["Execution Time"]), 4),
        )

        # Cleanup files
        os.remove(cycle_fn)
        os.remove(node_fn)

        # Ensure invalid file paths throw an error (do not fail silently)
        with self.assertRaises(ValueError):
            with profiler.Profiler(cycle_file="not_a_path/a.csv", node_file="also_not_a_path/b.csv") as p:
                results = sp2.run(stats_graph, starttime=st, endtime=st + timedelta(seconds=100))


if __name__ == "__main__":
    unittest.main()
