import numpy as np
import pickle
import typing
import unittest
from datetime import datetime, time, timedelta

import sp2
import sp2.impl.types.instantiation_type_resolver as type_resolver
from sp2 import ts
from sp2.impl.wiring.runtime import build_graph


class TestTypeChecking(unittest.TestCase):
    class Dummy:
        pass

    class Dummy2(Dummy):
        pass

    class Dummy3:
        pass

    def test_graph_build_type_checking(self):
        @sp2.node
        def typed_ts(x: ts[int]):
            if sp2.ticked(x):
                pass

        @sp2.node
        def typed_scalar(x: ts[int], y: str):
            if sp2.ticked(x):
                pass

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

    def test_runtime_type_check(self):
        ## native output type
        @sp2.node
        def typed_int(x: ts["T"]) -> ts[int]:
            if sp2.ticked(x):
                return x

        # python object output type
        @sp2.node
        def typed_list(x: ts["T"]) -> ts[list]:
            if sp2.ticked(x):
                return x

        @sp2.node
        def typed_alarm(v: "~T", alarm_type: "V") -> ts["V"]:
            with sp2.alarms():
                alarm = sp2.alarm("V")
            with sp2.start():
                sp2.schedule_alarm(alarm, timedelta(), v)

            if sp2.ticked(alarm):
                return alarm

        # Valid
        sp2.run(typed_int, sp2.const(5), starttime=datetime(2020, 2, 7))

        # Invalid
        with self.assertRaisesRegex(
            TypeError, '"typed_int" node expected output type on output #0 to be of type "int" got type "str"'
        ):
            sp2.run(typed_int, sp2.const("5"), starttime=datetime(2020, 2, 7))

        # valid
        sp2.run(typed_list, sp2.const([1, 2, 3]), starttime=datetime(2020, 2, 7))

        # Invalid
        with self.assertRaisesRegex(
            TypeError, '"typed_list" node expected output type on output #0 to be of type "list" got type "str"'
        ):
            sp2.run(typed_list, sp2.const("5"), starttime=datetime(2020, 2, 7))

        # valid
        sp2.run(typed_alarm, 5, int, starttime=datetime(2020, 2, 7))
        sp2.run(typed_alarm, 5, object, starttime=datetime(2020, 2, 7))
        sp2.run(typed_alarm, [1, 2, 3], [int], starttime=datetime(2020, 2, 7))

        # Invalid
        with self.assertRaisesRegex(
            TypeError, '"typed_alarm" node expected output type on output #0 to be of type "str" got type "int"'
        ):
            sp2.run(typed_alarm, 5, str, starttime=datetime(2020, 2, 7))

        with self.assertRaisesRegex(
            TypeError, '"typed_alarm" node expected output type on output #0 to be of type "bool" got type "int"'
        ):
            sp2.run(typed_alarm, 5, bool, starttime=datetime(2020, 2, 7))

        with self.assertRaisesRegex(
            TypeError, '"typed_alarm" node expected output type on output #0 to be of type "str" got type "list"'
        ):
            sp2.run(typed_alarm, [1, 2, 3], str, starttime=datetime(2020, 2, 7))

    def test_primitive_to_obj_casting(self):
        @sp2.node
        def typed_ts_int(x: ts[int]):
            pass

        @sp2.node
        def typed_ts_float(x: ts[float]):
            pass

        @sp2.node
        def typed_ts_object(x: ts[object]):
            pass

        @sp2.node
        def typed_ts_dummy(x: ts[TestTypeChecking.Dummy]):
            pass

        @sp2.node
        def typed_scalar(t: "V", x: ts["V"], y: "~V"):
            pass

        @sp2.node
        def typed_scalar_two_args(t: "T", x: ts["T"]):
            pass

        @sp2.node
        def str_typed_scalar(x: ts["T"], y: str):
            pass

        @sp2.node
        def float_typed_scalar(x: ts["T"], y: float):
            pass

        def graph():
            i = sp2.const(5)
            f = sp2.const(5.0)
            o = sp2.const(object())
            d = sp2.const(TestTypeChecking.Dummy())
            typed_ts_int(i)
            typed_ts_object(i)
            typed_ts_object(f)
            typed_ts_object(o)
            typed_ts_float(i)
            typed_ts_float(f)
            typed_ts_dummy(d)

            typed_scalar(int, i, 1)
            typed_scalar(float, f, 1.0)
            typed_scalar(object, o, object())
            typed_scalar(float, i, 1)
            typed_scalar(object, i, 1)

            # T resolved to float - OK
            typed_scalar(int, i, 1.0)

            # T resolved to  object - OK
            typed_scalar(int, i, object())

            # T resolved to  object - OK
            typed_scalar(TestTypeChecking.Dummy, o, object())

            # Weirdly ok, T is resolved to object, and all are objects
            typed_scalar(TestTypeChecking.Dummy, o, 1)

            # # Weirdly ok, T is resolved to object, and all are objects
            typed_scalar(TestTypeChecking.Dummy, i, object())

            # # Weirdly ok, T is resolved to object, and all are objects
            typed_scalar(TestTypeChecking.Dummy, i, object())
            # # Weirdly ok, T is resolved to object, and all are objects
            typed_scalar.using(V=object)(TestTypeChecking.Dummy, i, object())

            typed_scalar_two_args(TestTypeChecking.Dummy, o)
            typed_scalar_two_args(int, o)

            # OK, resolved to Dummy
            typed_scalar_two_args(TestTypeChecking.Dummy2, d)

            with self.assertRaisesRegex(
                TypeError,
                "Conflicting type resolution for V when calling to typed_scalar : "
                + r".*<class 'int'>, <class '.*test_type_checking.TestTypeChecking.Dummy'>.*",
            ):
                typed_scalar(int, i, TestTypeChecking.Dummy())

            with self.assertRaisesRegex(
                TypeError,
                "Conflicting type resolution for T when calling to typed_scalar_two_args : "
                + r"\(<class '.*test_type_checking.TestTypeChecking.Dummy'>, <class 'int'>\)",
            ):
                typed_scalar_two_args(TestTypeChecking.Dummy, i)

            with self.assertRaisesRegex(TypeError, "Expected ts\\[int\\] for argument 'x', got ts\\[str\\]"):
                s = sp2.const("xyz")
                typed_ts_int(s)

            with self.assertRaisesRegex(TypeError, "Expected str for argument 'y', got 123 \\(int\\)"):
                ## THIS SHOULD RAISE, passing int instead of str
                str_typed_scalar(i, 123)
            with self.assertRaisesRegex(TypeError, r"Expected ~V for argument 't', got .*Dummy.*\(V=int\)"):
                typed_scalar.using(V=int)(TestTypeChecking.Dummy, i, object())

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    def test_dict_type_resolutions(self):
        @sp2.node
        def typed_dict_int_int(x: {int: int}):
            pass

        @sp2.node
        def typed_dict_int_int2(x: typing.Dict[int, int]):
            pass

        @sp2.node
        def typed_dict_int_float(x: {int: int}):
            pass

        @sp2.node
        def typed_dict_float_float(x: {float: float}):
            pass

        @sp2.node
        def typed_dict(x: {"T": "V"}):
            pass

        @sp2.node
        def typed_ts_and_scalar(x: ts[{int: int}], y: {int: int}):
            pass

        @sp2.node
        def typed_ts_and_scalar_generic(x: ts[{"T": "T"}], y: {"T": "T"}, z: "~T"):
            pass

        @sp2.node
        def deep_nested_generic_resolution(x: "T1", y: "T2", z: {"T1": {"T2": [{"T1"}]}}):
            pass

        @sp2.node
        def deep_nested_generic_resolution2(
            x: "T1", y: "T2", z: typing.Dict["T1", typing.Dict["T2", typing.List[typing.Set["T1"]]]]
        ):
            pass

        def graph():
            d_i_i = sp2.const({1: 2, 3: 4})

            # Ok int dict expected
            typed_dict_int_int({1: 2, 3: 4})

            # Ok int dict expected
            typed_dict_int_int2({1: 2, 3: 4})

            typed_dict_float_float({1: 2})
            typed_dict_float_float({1.0: 2})
            typed_dict_float_float({})

            typed_ts_and_scalar(d_i_i, {1: 2})
            typed_ts_and_scalar_generic(d_i_i, {1: 2.0}, 1)

            for f in (deep_nested_generic_resolution, deep_nested_generic_resolution2):
                f(
                    TestTypeChecking.Dummy,
                    TestTypeChecking.Dummy2,
                    {TestTypeChecking.Dummy(): {TestTypeChecking.Dummy2(): [{TestTypeChecking.Dummy()}, set()]}},
                )
                # Internal sets are Dummy and Dummy2, since Dummy2 inherits from Dummy, it's ok, it's in fact Dummy, so we are good
                f(
                    TestTypeChecking.Dummy,
                    TestTypeChecking.Dummy2,
                    {
                        TestTypeChecking.Dummy(): {
                            TestTypeChecking.Dummy2(): [{TestTypeChecking.Dummy()}, {TestTypeChecking.Dummy2()}]
                        }
                    },
                )

            with self.assertRaisesRegex(TypeError, r"Expected typing.Dict\[int, int\] for argument 'x', got .*"):
                # Passing a float value instead of expected ints
                typed_dict_int_int2({1: 2, 3: 4.0})

            with self.assertRaisesRegex(TypeError, r"Expected typing.Dict\[float, float\] for argument 'x', got .*"):
                # Passing a Dummy value instead of expected float
                typed_dict_float_float({1.0: TestTypeChecking.Dummy()})

            with self.assertRaisesRegex(
                TypeError, "Conflicting type resolution for T when calling to typed_ts_and_scalar_generic .*"
            ):
                # Passing a Dummy value instead of expected float
                typed_ts_and_scalar_generic(d_i_i, {1: 2.0}, TestTypeChecking.Dummy())

            with self.assertRaisesRegex(
                TypeError, "Conflicting type resolution for T1 when calling to deep_nested_generic_resolution : " ".*"
            ):
                # Here for inernal sets we pass Dummy and Dummy3 - they result in conflicting type resolution for T1
                deep_nested_generic_resolution(
                    TestTypeChecking.Dummy,
                    TestTypeChecking.Dummy2,
                    {
                        TestTypeChecking.Dummy(): {
                            TestTypeChecking.Dummy2(): [{TestTypeChecking.Dummy()}, {TestTypeChecking.Dummy3()}]
                        }
                    },
                )
            l_good = sp2.const.using(T={int: float})({})
            with self.assertRaisesRegex(
                TypeError,
                "Unable to resolve container type for type variable T explicit value must have"
                + " uniform values and be non empty.*",
            ):
                # Passing a Dummy value instead of expected float
                l_bad = sp2.const({})

            l_good = sp2.const.using(T={int: float})({2: 1})
            l_good = sp2.const.using(T={int: float})({2: 1.0})
            with self.assertRaises(TypeError):
                # passing float to int
                l_bad = sp2.const.using(T={int: float})({2.0: 1})

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    def test_list_type_resolutions(self):
        @sp2.node
        def typed_list_int(x: [int]):
            pass

        @sp2.node
        def typed_list_int2(x: typing.List[int]):
            pass

        @sp2.node
        def typed_list_float(x: [float]):
            pass

        @sp2.node
        def typed_ts_and_scalar(x: ts[[int]], y: [int]):
            pass

        @sp2.node
        def typed_ts_and_scalar_generic(x: ts[["T"]], y: ["T"], z: "~T"):
            pass

        def graph():
            l_i = sp2.const([1, 2, 3, 4])

            typed_list_int([])
            typed_list_int([1, 2, 3])
            typed_list_int2([1, 2, 3])
            typed_list_float([1, 2, 3])
            typed_list_float([1, 2, 3.0])

            typed_ts_and_scalar(l_i, [1, 2, 3])
            typed_ts_and_scalar_generic(l_i, [1, 2, 3], 1)

            with self.assertRaisesRegex(TypeError, r"Expected typing.List\[int\] for argument 'x', got .*"):
                # Passing a float value instead of expected ints
                typed_list_int([1, 2, 3.0])

            with self.assertRaisesRegex(TypeError, r"Expected typing.List\[float\] for argument 'x', got .*"):
                # Passing a Dummy value instead of expected float
                typed_list_float([TestTypeChecking.Dummy()])
            with self.assertRaisesRegex(
                TypeError, "Conflicting type resolution for T when calling to typed_ts_and_scalar_generic .*"
            ):
                # Passing a Dummy value instead of expected float
                typed_ts_and_scalar_generic(l_i, [1, 2], TestTypeChecking.Dummy())

            l_good = sp2.const.using(T=[int])([])
            with self.assertRaisesRegex(
                TypeError,
                "Unable to resolve container type for type variable T explicit value must have"
                + " uniform values and be non empty.*",
            ):
                # Passing a Dummy value instead of expected float
                l_bad = sp2.const([])

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    def test_set_type_resolutions(self):
        @sp2.node
        def typed_set_int(x: {int}):
            pass

        @sp2.node
        def typed_set_int2(x: typing.Set[int]):
            pass

        @sp2.node
        def typed_set_float(x: {float}):
            pass

        @sp2.node
        def typed_ts_and_scalar(x: ts[{int}], y: {int}):
            pass

        @sp2.node
        def typed_ts_and_scalar_generic(x: ts[{"T"}], y: {"T"}, z: "~T"):
            pass

        def graph():
            l_i = sp2.const({1, 2, 3, 4})

            typed_set_int(set())
            typed_set_int({1, 2, 3})
            typed_set_int2({1, 2, 3})
            typed_set_float({1, 2, 3})
            typed_set_float({1, 2, 3.0})

            typed_ts_and_scalar(l_i, {1, 2, 3})
            typed_ts_and_scalar_generic(l_i, {1, 2, 3}, 1)

            with self.assertRaisesRegex(TypeError, r"Expected typing.Set\[int\] for argument 'x', got .*"):
                # Passing a float value instead of expected ints
                typed_set_int({1, 2, 3.0})

            with self.assertRaisesRegex(TypeError, r"Expected typing.Set\[float\] for argument 'x', got .*"):
                # Passing a Dummy value instead of expected float
                typed_set_float({TestTypeChecking.Dummy()})
            with self.assertRaisesRegex(
                TypeError, "Conflicting type resolution for T when calling to typed_ts_and_scalar_generic .*"
            ):
                # Passing a Dummy value instead of expected float
                typed_ts_and_scalar_generic(l_i, {1, 2}, TestTypeChecking.Dummy())

            l_good = sp2.const.using(T={int})(set())
            with self.assertRaisesRegex(
                TypeError,
                "Unable to resolve container type for type variable T explicit value must have"
                + " uniform values and be non empty.*",
            ):
                # Passing a Dummy value instead of expected float
                l_bad = sp2.const({})

        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    def test_graph_output_type_checking(self):
        with self.assertRaises(TypeError):

            @sp2.graph
            def sub_graph() -> sp2.OutputBasket(typing.Dict[str, ts[int]]):
                return sp2.output({"x": sp2.const(5), "y": sp2.const(6.0)})

            def graph():
                sub_graph()

            build_graph(graph)

        with self.assertRaises(TypeError):

            @sp2.graph
            def sub_graph() -> sp2.OutputBasket(typing.List[ts[int]]):
                return sp2.output([sp2.const(5), sp2.const(6.0)])

            def graph():
                sub_graph()

            build_graph(graph)

        with self.assertRaises(TypeError):

            @sp2.graph
            def sub_graph() -> ts[int]:
                return sp2.output(sp2.const(6.0))

            def graph():
                sub_graph()

            build_graph(graph)

        with self.assertRaises(TypeError):

            @sp2.graph
            def sub_graph() -> sp2.Outputs(x=ts[int]):
                return sp2.output(sp2.const(6.0))

            def graph():
                sub_graph()

            build_graph(graph)

        with self.assertRaises(TypeError):

            @sp2.graph
            def sub_graph() -> sp2.Outputs(x=ts[int], y=ts[float]):
                return sp2.output(x=sp2.const(6.0), y=sp2.const(7.0))

            def graph():
                sub_graph()

            build_graph(graph)

        @sp2.graph
        def sub_graph() -> sp2.OutputBasket(typing.Dict[str, ts[int]]):
            return sp2.output({"x": sp2.const(5), "y": sp2.const(6)})

        def graph():
            sub_graph()

        build_graph(graph)

        @sp2.graph
        def sub_graph() -> sp2.OutputBasket(typing.List[ts[int]]):
            return sp2.output([sp2.const(5), sp2.const(6)])

        def graph():
            sub_graph()

        build_graph(graph)

        @sp2.graph
        def sub_graph() -> ts[int]:
            return sp2.output(sp2.const(6))

        def graph():
            sub_graph()

        build_graph(graph)

        @sp2.graph
        def sub_graph() -> sp2.Outputs(x=ts[int]):
            return sp2.output(x=sp2.const(6))

        def graph():
            sub_graph()

        build_graph(graph)

        @sp2.graph
        def sub_graph() -> sp2.Outputs(x=ts[float], y=ts[float]):
            return sp2.output(x=sp2.const(6.0), y=sp2.const(7.0))

        def graph():
            sub_graph()

        build_graph(graph)

    def test_basket_type_check_bug(self):
        # Tests a bug that wasn't covered in the initial implementation. The code below was crashing on _ForwardRef before the fix
        @sp2.node
        def dummy(x: sp2.ts[typing.List["T"]]):
            pass

        def g():
            dummy(sp2.const([1]))

        sp2.run(g, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 1))

    def test_graph_return_type_checking_bug(self):
        # There was a big where return order in the __return__ mattered, this tests that this bug is addressed
        @sp2.graph
        def foo() -> sp2.Outputs(x=ts[int], y=ts[str]):
            return sp2.output(y=sp2.const("hey"), x=sp2.const(1))

        sp2.run(foo, starttime=datetime.utcnow(), endtime=timedelta())

    def test_typed_to_untyped_container(self):
        @sp2.graph
        def g(d: sp2.ts[dict], s: sp2.ts[set], l: sp2.ts[list]):
            pass

        def main():
            g(
                d=sp2.const.using(T=typing.Dict[int, int])({}),
                s=sp2.const.using(T=typing.Set[int])(set()),
                l=sp2.const.using(T=typing.List[int])([]),
            )

        sp2.run(main, starttime=datetime.utcnow(), endtime=timedelta())

    def test_time_tzinfo(self):
        import pytz

        timetz = time(1, 2, 3, tzinfo=pytz.timezone("EST"))
        with self.assertRaisesRegex(TypeError, "sp2 time type does not support timezones"):
            # Now that Time is a native type it no longer supports ticking with tzinfo
            sp2.run(sp2.const, timetz, starttime=datetime.utcnow(), endtime=timedelta())

        res = sp2.run(sp2.const.using(T=object), timetz, starttime=datetime.utcnow(), endtime=timedelta())[0][0][1]
        self.assertEqual(res, timetz)

    def test_np_ndarray_ts_arg(self):
        @sp2.node
        def foo(arr: sp2.ts[np.ndarray]) -> sp2.ts[np.ndarray]:
            return arr

        inp_arr = np.zeros(shape=(2, 2))
        st = datetime(2020, 2, 7, 9)
        res = sp2.run(foo(sp2.const(inp_arr)), starttime=st, endtime=datetime(2020, 2, 7, 9, 1))  # should not raise
        self.assertEqual(res[0], [(st, inp_arr)])

    def test_pickle_type_resolver_errors(self):
        errors = [
            type_resolver.ContainerTypeVarResolutionError("g", "T", "NotT"),
            type_resolver.ArgTypeMismatchError("g", "T", "NotT", "Var", {"field": 1}),
            type_resolver.ArgContainerMismatchError("g", "T", "NotT", "Var"),
            type_resolver.TSArgTypeMismatchError("g", "T", "NotT", "Var"),
            type_resolver.TSDictBasketKeyMismatchError("g", "T", "Var"),
        ]

        for err in errors:
            pickled = pickle.loads(pickle.dumps(err))
            self.assertEqual(str(err), str(pickled))


if __name__ == "__main__":
    unittest.main()
