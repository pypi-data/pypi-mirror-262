import typing
import unittest
from datetime import datetime

import sp2
from sp2 import ts


class TestNumbaTypeChecking(unittest.TestCase):
    @unittest.skip("numba not yet used, tests fail on newer numba we get in our 3.8 build")
    def test_graph_build_type_checking(self):
        @sp2.numba_node
        def typed_ts(x: ts[int]):
            if sp2.ticked(x):
                pass

        @sp2.numba_node
        def typed_scalar(x: ts[int], y: str):
            if sp2.ticked(x):
                pass

        @sp2.graph
        def graph():
            i = sp2.const(5)
            typed_ts(i)

            typed_scalar(i, "xyz")

            with self.assertRaisesRegex(TypeError, "Expected ts\\[int\\] for argument 'x', got ts\\[str\\]"):
                s = sp2.const("xyz")
                ## THIS SHOULD RAISE, passing ts[str] but typed takes ts[int]
                typed_ts(s)

            with self.assertRaisesRegex(TypeError, "Expected str for argument 'y', got 123 \\(int\\)"):
                ## THIS SHOULD RAISE, passing int instead of str
                typed_scalar(i, 123)

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    @unittest.skip("numba not yet used, tests fail on newer numba we get in our 3.8 build")
    def test_runtime_type_check(self):
        ## native output type
        @sp2.numba_node
        def typed_int(x: ts["T"]) -> ts[int]:
            if sp2.ticked(x):
                return x

        # TODO: Uncomment
        # @sp2.numba_node
        # def typed_alarm(v: '~T', alarm_type: 'V') -> outputs(ts['V']):
        #     with sp2.alarms():
        #         alarm = sp2.alarm( 'V' )
        #     with sp2.start():
        #         sp2.schedule_alarm(alarm, timedelta(), v)
        #
        #     if sp2.ticked(alarm):
        #         return alarm

        # Valid
        sp2.run(typed_int, sp2.const(5), starttime=datetime(2020, 2, 7))

        # Invalid
        with self.assertRaisesRegex(RuntimeError, "Unable to resolve getter function for type.*"):
            sp2.run(typed_int, sp2.const("5"), starttime=datetime(2020, 2, 7))

        # TODO: uncomment
        # # valid
        # sp2.run(typed_alarm, 5, int, starttime=datetime(2020, 2, 7))
        # sp2.run(typed_alarm, 5, object, starttime=datetime(2020, 2, 7))
        # sp2.run(typed_alarm, [1, 2, 3], [int], starttime=datetime(2020, 2, 7))
        #
        # # Invalid
        # with self.assertRaisesRegex(TypeError,
        #                             '"typed_alarm" node expected output type on output #0 to be of type "str" got type "int"'):
        #     sp2.run(typed_alarm, 5, str, starttime=datetime(2020, 2, 7))
        #
        # with self.assertRaisesRegex(TypeError,
        #                             '"typed_alarm" node expected output type on output #0 to be of type "bool" got type "int"'):
        #     sp2.run(typed_alarm, 5, bool, starttime=datetime(2020, 2, 7))
        #
        # with self.assertRaisesRegex(TypeError,
        #                             '"typed_alarm" node expected output type on output #0 to be of type "str" got type "list"'):
        #     sp2.run(typed_alarm, [1, 2, 3], str, starttime=datetime(2020, 2, 7))

    @unittest.skip("numba not yet used, tests fail on newer numba we get in our 3.8 build")
    def test_dict_type_resolutions(self):
        @sp2.numba_node
        def typed_dict_int_int(x: {int: int}):
            pass

        @sp2.numba_node
        def typed_dict_int_int2(x: typing.Dict[int, int]):
            pass

        @sp2.numba_node
        def typed_dict_int_float(x: {int: int}):
            pass

        @sp2.numba_node
        def typed_dict_float_float(x: {float: float}):
            pass

        @sp2.numba_node
        def typed_dict(x: {"T": "V"}):
            pass

        @sp2.numba_node
        def deep_nested_generic_resolution(x: "T1", y: "T2", z: {"T1": {"T2": [{"T1"}]}}):
            pass

        @sp2.graph
        def graph():
            d_i_i = sp2.const({1: 2, 3: 4})
            sp2.add_graph_output("o1", d_i_i)

            # Ok int dict expected
            typed_dict_int_int({1: 2, 3: 4})

            # Ok int dict expected
            typed_dict_int_int2({1: 2, 3: 4})

            typed_dict_float_float({1: 2})
            typed_dict_float_float({1.0: 2})
            typed_dict_float_float({})

            with self.assertRaisesRegex(TypeError, r"Expected typing.Dict\[int, int\] for argument 'x', got .*"):
                # Passing a float value instead of expected ints
                typed_dict_int_int2({1: 2, 3: 4.0})

            l_good = sp2.const.using(T={int: float})({})
            sp2.add_graph_output("o2", l_good)
            l_good = sp2.const.using(T={int: float})({2: 1})
            sp2.add_graph_output("o3", l_good)
            l_good = sp2.const.using(T={int: float})({2: 1.0})
            sp2.add_graph_output("o4", l_good)

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    @unittest.skip("numba not yet used, tests fail on newer numba we get in our 3.8 build")
    def test_list_type_resolutions(self):
        @sp2.numba_node
        def typed_list_int(x: [int]):
            pass

        @sp2.numba_node
        def typed_list_int2(x: typing.List[int]):
            pass

        @sp2.numba_node
        def typed_list_float(x: [float]):
            pass

        def graph():
            l_i = sp2.const([1, 2, 3, 4])

            typed_list_int([])
            typed_list_int([1, 2, 3])
            typed_list_int2([1, 2, 3])
            typed_list_float([1, 2, 3])
            typed_list_float([1, 2, 3.0])

            with self.assertRaisesRegex(TypeError, r"Expected typing.List\[int\] for argument 'x', got .*"):
                # Passing a float value instead of expected ints
                typed_list_int([1, 2, 3.0])

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))


if __name__ == "__main__":
    unittest.main()
