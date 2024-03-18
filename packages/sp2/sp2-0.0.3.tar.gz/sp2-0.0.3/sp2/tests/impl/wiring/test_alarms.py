import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import ts


class TestState(unittest.TestCase):
    def test_alarms_defined_in_with_block_scheduled_in_start_block(self):
        @sp2.node
        def test_node() -> ts[int]:
            with sp2.alarms():
                z = sp2.alarm(bool)
            with sp2.state():
                x = 5
            with sp2.start():
                sp2.schedule_alarm(z, timedelta(seconds=0), True)

            if sp2.ticked(z):
                assert x == 5
                return x

        @sp2.graph
        def test_graph() -> ts[int]:
            return test_node()

        starttime = datetime(2021, 1, 1)

        ret = sp2.run(test_graph, starttime=starttime, endtime=timedelta(seconds=15))

        self.assertEqual(ret[0][0][1], 5)


if __name__ == "__main__":
    unittest.main()
