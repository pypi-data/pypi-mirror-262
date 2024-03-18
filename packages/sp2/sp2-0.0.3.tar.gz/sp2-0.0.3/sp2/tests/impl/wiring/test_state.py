import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import ts


class TestState(unittest.TestCase):
    def test_state_defined_in_with_block(self):
        @sp2.node
        def test_node(in_: ts[bool]) -> ts[int]:
            with sp2.state():
                x = 5

            if sp2.ticked(in_):
                assert x == 5
                return x

        @sp2.graph
        def test_graph() -> ts[int]:
            return test_node(sp2.const(True))

        starttime = datetime(2021, 1, 1)

        ret = sp2.run(test_graph, starttime=starttime, endtime=timedelta(seconds=15))

        self.assertEqual(ret[0][0][1], 5)


if __name__ == "__main__":
    unittest.main()
