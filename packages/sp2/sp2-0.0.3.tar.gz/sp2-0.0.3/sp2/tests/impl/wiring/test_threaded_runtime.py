import time
import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import ts


@sp2.node
def graph_stop(xs: ts["T"], output: dict) -> ts["T"]:
    with sp2.stop():
        output["stop"] = sp2.now()

    if sp2.ticked(xs):
        return xs


@sp2.node
def node_exception(xs: ts["T"]) -> ts["T"]:
    if sp2.ticked(xs):
        raise ValueError("Test Node")
        return xs


@sp2.graph
def graph_exception():
    raise ValueError("Test Graph")


class TestThreadedRuntime(unittest.TestCase):
    def test_run_on_thread(self):
        output = {}
        starttime = datetime.utcnow()
        endtime = starttime + timedelta(minutes=1)
        runner = sp2.run_on_thread(
            graph_stop, sp2.const(True), output, starttime=starttime, endtime=endtime, realtime=True
        )
        self.assertTrue(runner.is_alive())
        runner.stop_engine()
        runner.join()
        self.assertFalse(runner.is_alive())
        self.assertTrue(output.get("stop"))
        self.assertLess(output["stop"], endtime)

    def test_node_exception(self):
        runner = sp2.run_on_thread(
            node_exception, sp2.const(True), starttime=datetime.utcnow(), endtime=timedelta(seconds=1), realtime=True
        )
        self.assertRaises(RuntimeError, runner.join)
        self.assertFalse(runner.is_alive())
        self.assertEqual(runner.join(True), None)

    def test_graph_exception(self):
        runner = sp2.run_on_thread(
            graph_exception, sp2.const(True), starttime=datetime.utcnow(), endtime=timedelta(seconds=1), realtime=True
        )
        self.assertRaises(RuntimeError, runner.join)
        self.assertFalse(runner.is_alive())
        self.assertEqual(runner.join(True), None)

    def test_auto_shutdown(self):
        output = {}
        starttime = datetime.utcnow()
        endtime = starttime + timedelta(minutes=1)
        runner = sp2.run_on_thread(
            graph_stop, sp2.const(True), output, auto_shutdown=True, starttime=starttime, endtime=endtime, realtime=True
        )
        self.assertTrue(runner.is_alive())
        del runner
        self.assertTrue(output.get("stop"))
        self.assertLess(output["stop"], endtime)

    def test_auto_shutdown_exception(self):
        runner = sp2.run_on_thread(
            node_exception,
            sp2.const(True),
            auto_shutdown=True,
            starttime=datetime.utcnow(),
            endtime=timedelta(seconds=1),
            realtime=True,
        )
        time.sleep(1.0)  # Avoid race condition with graph raising exception
        del runner  # This should not throw an exception, even though one has been raised on the thread

    def test_sp2_run_symmetric_api(self):
        # make sure args and kwargs passed the same

        @sp2.graph
        def graph(arg: int):
            values = sp2.const(arg)
            sp2.print("values: ", values)

        # kwargs
        sp2.run(graph, arg=1, starttime=datetime.utcnow(), endtime=timedelta(seconds=0.1), realtime=True)
        res = sp2.run_on_thread(
            graph, arg=1, starttime=datetime.utcnow(), endtime=timedelta(seconds=0.1), realtime=True
        )
        res.join()

        # args
        sp2.run(graph, 1, starttime=datetime.utcnow(), endtime=timedelta(seconds=0.1), realtime=True)
        res = sp2.run_on_thread(graph, 1, starttime=datetime.utcnow(), endtime=timedelta(seconds=0.1), realtime=True)
        res.join()


if __name__ == "__main__":
    unittest.main()
