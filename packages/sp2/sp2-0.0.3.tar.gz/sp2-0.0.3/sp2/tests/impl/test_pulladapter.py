import time
import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import PushMode, ts


class MyStruct(sp2.Struct):
    a: int
    b: str


class TestPullAdapter(unittest.TestCase):
    def test_basic(self):
        # We just use the existing curve adapter to test pull since its currently implemented as a python PullInputAdapter
        @sp2.node
        def check(burst: ts[["T"]], lv: ts["T"], nc: ts["T"]):
            if sp2.ticked(burst):
                self.assertEqual(len(burst), 2)
                self.assertEqual(burst[0], nc)

            if sp2.ticked(nc):
                if isinstance(nc, int):
                    self.assertEqual(nc, sp2.num_ticks(nc))
                else:
                    self.assertEqual(nc.a, sp2.num_ticks(nc))
                if not sp2.ticked(burst):
                    self.assertEqual(nc, burst[1])

            if sp2.ticked(lv):
                if isinstance(lv, int):
                    self.assertEqual(lv, sp2.num_ticks(lv) * 2)
                else:
                    self.assertEqual(lv.a, sp2.num_ticks(lv) * 2)

        def graph(typ: type):
            raw_data = []
            td = timedelta()
            for x in range(1, 100, 2):
                if typ is int:
                    raw_data.append((td, x))
                    raw_data.append((td, x + 1))
                else:
                    raw_data.append((td, MyStruct(a=x, b=str(x))))
                    raw_data.append((td, MyStruct(a=x + 1, b=str(x + 1))))

                td += timedelta(seconds=1)

            nc = sp2.curve(typ, raw_data, push_mode=sp2.PushMode.NON_COLLAPSING)
            lv = sp2.curve(typ, raw_data, push_mode=PushMode.LAST_VALUE)
            burst = sp2.curve(typ, raw_data, push_mode=PushMode.BURST)
            check(burst, lv, nc)

        sp2.run(graph, int, starttime=datetime(2023, 2, 21))
        # This was actually a bug specifically on Struct types: "PyPullAdapter crashes on burst of structs"
        sp2.run(graph, MyStruct, starttime=datetime(2023, 2, 21))


if __name__ == "__main__":
    unittest.main()
