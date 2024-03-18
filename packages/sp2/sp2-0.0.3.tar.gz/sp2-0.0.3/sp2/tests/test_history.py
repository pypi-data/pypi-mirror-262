import numpy as np
import os
import psutil
import typing
import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import ts


class _Globals:
    _instance = None

    def __init__(self):
        self.values = {}
        self.timestamps = {}
        self.items = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = _Globals()
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = _Globals()


@sp2.node
def _collect_value(
    x: ts[int],
    getter_str: str,
    timestamp_delta: timedelta = None,
    fixed_time: datetime = None,
    force_min: int = 0,
    default_value: object = sp2.UNSET,
):
    with sp2.start():
        sp2.set_buffering_policy(x, 5, timedelta(1))
    if sp2.ticked(x):
        n_iter = 1 if fixed_time is not None else max(sp2.num_ticks(x), force_min)
        for i in range(n_iter):
            if fixed_time is not None:
                offset = min(fixed_time, sp2.now())
            else:
                offset = -i if timestamp_delta is None else -i * timestamp_delta
            if getter_str == "value":
                if default_value == sp2.UNSET:
                    _Globals.instance().values[i] = sp2.value_at(x, offset)
                else:
                    _Globals.instance().values[i] = sp2.value_at(x, offset, default=default_value)
            elif getter_str == "time":
                if default_value == sp2.UNSET:
                    _Globals.instance().timestamps[i] = sp2.time_at(x, offset)
                else:
                    _Globals.instance().timestamps[i] = sp2.time_at(x, offset, default=default_value)
            elif getter_str == "item":
                if default_value == sp2.UNSET:
                    _Globals.instance().items[i] = sp2.item_at(x, offset)
                else:
                    _Globals.instance().items[i] = sp2.item_at(x, offset, default=default_value)
            else:
                raise RuntimeError(f"Unrecognized getter_str {getter_str}")


class TestHistory(unittest.TestCase):
    def test_simple(self):
        @sp2.graph
        def graph():
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str="value")
            _collect_value(x, getter_str="time")
            _collect_value(x, getter_str="item")

        _Globals.reset()
        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5))

        self.assertEqual(_Globals.instance().values, {0: 4, 1: 3, 2: 2, 3: 1})

        self.assertEqual(
            _Globals.instance().timestamps,
            {
                0: datetime(2020, 2, 7, 9, 0, 4),
                1: datetime(2020, 2, 7, 9, 0, 3),
                2: datetime(2020, 2, 7, 9, 0, 2),
                3: datetime(2020, 2, 7, 9, 0, 1),
            },
        )

        self.assertEqual(
            _Globals.instance().items,
            {
                0: (datetime(2020, 2, 7, 9, 0, 4), 4),
                1: (datetime(2020, 2, 7, 9, 0, 3), 3),
                2: (datetime(2020, 2, 7, 9, 0, 2), 2),
                3: (datetime(2020, 2, 7, 9, 0, 1), 1),
            },
        )

    def test_range_access_invalid(self):
        @sp2.node
        def values_at(trigger: ts[object], x: ts[object]) -> ts[np.ndarray]:
            with sp2.start():
                sp2.set_buffering_policy(x, tick_count=3)
            if sp2.ticked(trigger):
                return sp2.values_at(x, -2, None)

        results = sp2.run(values_at, sp2.const(True), sp2.null_ts(int), starttime=datetime(2020, 1, 1))
        self.assertTrue(np.array_equal(results[0][0][1], np.array([])))

    def test_no_data(self):
        results = sp2.run(sp2.null_ts(bool), starttime=datetime(2020, 1, 1))
        results_np = sp2.run(sp2.null_ts(bool), starttime=datetime(2020, 1, 1), output_numpy=True)

        self.assertEqual(results[0], [])
        self.assertTrue(np.array_equal(results_np[0][0], np.array([])))
        self.assertTrue(np.array_equal(results_np[0][1], np.array([])))

    def test_range_access(self):
        class MyEnum(sp2.Enum):
            first = 0
            second = 1

        class MyStruct(sp2.Struct):
            i: int
            s: str
            b: bool

        numpyType = {
            "bool": np.dtype("bool"),
            "int": np.dtype("int64"),
            "float": np.dtype("float64"),
            "timedelta": np.dtype("timedelta64[ns]"),
            "datetime": np.dtype("datetime64[ns]"),
        }

        nonNativeType = {"enum": MyEnum, "list": list, "string": str, "struct": MyStruct}

        @sp2.node
        def collect_index(
            x: ts["T"],
            startIndex: int,
            endIndex: int,
            startIndexPolicy: sp2.TimeIndexPolicy,
            endIndexPolicy: sp2.TimeIndexPolicy,
        ) -> sp2.Outputs(values=ts[np.ndarray], timestamps=ts[np.ndarray], items=ts[tuple]):
            with sp2.start():
                sp2.set_buffering_policy(x, 5)
            if sp2.ticked(x):
                sp2.output(values, sp2.values_at(x, startIndex, endIndex, startIndexPolicy, endIndexPolicy))
                sp2.output(timestamps, sp2.times_at(x, startIndex, endIndex, startIndexPolicy, endIndexPolicy))
                sp2.output(items, sp2.items_at(x, startIndex, endIndex, startIndexPolicy, endIndexPolicy))

                with self.assertRaises(IndexError):
                    sp2.values_at(x, -10, 0, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE)

                with self.assertRaises(TypeError):
                    sp2.values_at(x, 0, 0, sp2.TimeIndexPolicy.EXCLUSIVE, sp2.TimeIndexPolicy.EXCLUSIVE)

                with self.assertRaises(RuntimeError):
                    sp2.items_at(x, -10, 0, False, False)

        @sp2.node
        def collect_timedelta(
            x: ts["T"],
            startIndex: timedelta,
            endIndex: timedelta,
            startIndexPolicy: sp2.TimeIndexPolicy,
            endIndexPolicy: sp2.TimeIndexPolicy,
            with_datetime: bool = False,
        ) -> sp2.Outputs(
            values=ts[np.ndarray], timestamps=ts[np.ndarray], items=ts[tuple], values_default=ts[np.ndarray]
        ):
            with sp2.start():
                sp2.set_buffering_policy(x, tick_history=timedelta(seconds=5))
            if sp2.ticked(x):
                if with_datetime:
                    sp2.output(
                        values,
                        sp2.values_at(
                            x, sp2.now() + startIndex, sp2.now() + endIndex, startIndexPolicy, endIndexPolicy
                        ),
                    )
                    sp2.output(
                        timestamps,
                        sp2.times_at(x, sp2.now() + startIndex, sp2.now() + endIndex, startIndexPolicy, endIndexPolicy),
                    )
                    sp2.output(
                        items,
                        sp2.items_at(x, sp2.now() + startIndex, sp2.now() + endIndex, startIndexPolicy, endIndexPolicy),
                    )
                else:
                    sp2.output(values, sp2.values_at(x, startIndex, endIndex, startIndexPolicy, endIndexPolicy))
                    sp2.output(timestamps, sp2.times_at(x, startIndex, endIndex, startIndexPolicy, endIndexPolicy))
                    sp2.output(items, sp2.items_at(x, startIndex, endIndex, startIndexPolicy, endIndexPolicy))

                sp2.output(values_default, sp2.values_at(x))

                with self.assertRaises(RuntimeError):
                    sp2.times_at(x, startIndex, endIndex, "abc", False)

        @sp2.node
        def collect_passive(
            x: ts["T"],
            t: ts[bool],
            startIndex: timedelta,
            endIndex: timedelta,
            startIndexPolicy: sp2.TimeIndexPolicy,
            endIndexPolicy: sp2.TimeIndexPolicy,
        ) -> sp2.Outputs(values=ts[np.ndarray], timestamps=ts[np.ndarray], items=ts[tuple]):
            with sp2.start():
                sp2.set_buffering_policy(x, tick_history=timedelta(seconds=5))
                sp2.make_passive(x)
            if sp2.ticked(t):
                sp2.output(
                    values,
                    sp2.values_at(x, sp2.now() + startIndex, sp2.now() + endIndex, startIndexPolicy, endIndexPolicy),
                )
                sp2.output(
                    timestamps,
                    sp2.times_at(x, sp2.now() + startIndex, sp2.now() + endIndex, startIndexPolicy, endIndexPolicy),
                )
                sp2.output(
                    items,
                    sp2.items_at(x, sp2.now() + startIndex, sp2.now() + endIndex, startIndexPolicy, endIndexPolicy),
                )

        @sp2.graph
        def graph():
            x_const = sp2.const(5)
            t = sp2.timer(timedelta(seconds=1))
            x_bool = sp2.curve(bool, [(timedelta(seconds=v + 1), True) for v in range(40)])
            x_int = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(40)])
            x_float = sp2.curve(float, [(timedelta(seconds=v + 1), v + 1) for v in range(40)])
            x_timedelta = sp2.curve(
                timedelta, [(timedelta(seconds=v + 1), timedelta(seconds=v + 1)) for v in range(40)]
            )
            x_enum = sp2.curve(MyEnum, [(timedelta(seconds=v + 1), MyEnum.first) for v in range(40)])
            x_list = sp2.curve(list, [(timedelta(seconds=v + 1), [1, 2, 3, 4]) for v in range(40)])
            x_string = sp2.curve(str, [(timedelta(seconds=v + 1), "v+1") for v in range(40)])
            x_struct = sp2.curve(
                MyStruct, [(timedelta(seconds=v + 1), MyStruct(i=v + 1, s="v+1", b=True)) for v in range(40)]
            )

            x_duplicate_timestamp = sp2.curve(
                int,
                [(timedelta(seconds=v + 1), v + 1) for v in range(35)]
                + [(timedelta(seconds=35), v + 1) for v in range(35, 38)]  # t = 35 should have 3 ticks
                + [(timedelta(seconds=v + 1), v + 1) for v in range(38, 40)],
            )
            x_duplicate_datetime = sp2.curve(
                int,
                [(timedelta(seconds=v + 1), v + 1) for v in range(35)]
                + [(timedelta(seconds=35), v + 1) for v in range(35, 38)]
                + [(timedelta(seconds=v + 1), v + 1) for v in range(38, 40)],
            )
            x_duplicate_enum = sp2.curve(
                MyEnum,
                [(timedelta(seconds=v + 1), MyEnum.first) for v in range(35)]
                + [(timedelta(seconds=35), MyEnum.second) for v in range(35, 38)]
                + [(timedelta(seconds=v + 1), MyEnum.first) for v in range(38, 40)],
            )

            c_bool = collect_timedelta(
                x_bool,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.INCLUSIVE,
                sp2.TimeIndexPolicy.INCLUSIVE,
            )  # length: 5
            c_int = collect_index(
                x_int, None, None, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 5
            c_float = collect_index(
                x_float, -3, -2, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 2
            c_timedelta = collect_index(
                x_timedelta, -4, -2, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 3
            c_enum = collect_index(
                x_enum, -3, -1, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 3
            c_list = collect_index(
                x_list, -3, -2, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 2
            c_string = collect_index(
                x_string, -3, -1, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 4
            c_struct = collect_index(
                x_struct, -4, -2, sp2.TimeIndexPolicy.INCLUSIVE, sp2.TimeIndexPolicy.INCLUSIVE
            )  # length: 4

            c_const_inclusive = collect_passive(
                x_const,
                t,
                -timedelta(seconds=5),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.INCLUSIVE,
                sp2.TimeIndexPolicy.INCLUSIVE,
            )
            c_const_exclusive = collect_passive(
                x_const,
                t,
                -timedelta(seconds=5),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.EXCLUSIVE,
                sp2.TimeIndexPolicy.EXCLUSIVE,
            )
            c_const_extrapolate = collect_passive(
                x_const,
                t,
                -timedelta(seconds=5),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.EXTRAPOLATE,
                sp2.TimeIndexPolicy.EXTRAPOLATE,
            )
            c_duplicate_timestamp_exclusive = collect_timedelta(
                x_duplicate_timestamp,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.EXCLUSIVE,
                sp2.TimeIndexPolicy.EXCLUSIVE,
            )
            c_duplicate_timestamp_inclusive = collect_timedelta(
                x_duplicate_timestamp,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.INCLUSIVE,
                sp2.TimeIndexPolicy.INCLUSIVE,
            )
            c_duplicate_timestamp_extrapolate = collect_timedelta(
                x_duplicate_timestamp,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.EXTRAPOLATE,
                sp2.TimeIndexPolicy.EXTRAPOLATE,
            )
            c_extrapolate_short_window = collect_timedelta(
                x_duplicate_timestamp,
                -timedelta(seconds=2),
                -timedelta(seconds=1),
                sp2.TimeIndexPolicy.EXTRAPOLATE,
                sp2.TimeIndexPolicy.EXTRAPOLATE,
            )
            c_extrapolate_enum = collect_timedelta(
                x_duplicate_enum,
                -timedelta(seconds=2),
                -timedelta(seconds=1),
                sp2.TimeIndexPolicy.EXTRAPOLATE,
                sp2.TimeIndexPolicy.EXTRAPOLATE,
            )
            c_enum_boundary = collect_timedelta(
                x_duplicate_enum,
                timedelta(seconds=-5),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.INCLUSIVE,
                sp2.TimeIndexPolicy.INCLUSIVE,
            )

            c_duplicate_datetime_exclusive = collect_timedelta(
                x_duplicate_datetime,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.EXCLUSIVE,
                sp2.TimeIndexPolicy.EXCLUSIVE,
                True,
            )
            c_duplicate_datetime_inclusive = collect_timedelta(
                x_duplicate_datetime,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.INCLUSIVE,
                sp2.TimeIndexPolicy.INCLUSIVE,
                True,
            )
            c_duplicate_datetime_extrapolate = collect_timedelta(
                x_duplicate_datetime,
                -timedelta(seconds=4),
                -timedelta(seconds=0),
                sp2.TimeIndexPolicy.EXTRAPOLATE,
                sp2.TimeIndexPolicy.EXTRAPOLATE,
                True,
            )

            for o in ["values", "timestamps", "items"]:
                sp2.add_graph_output(f"{o}_bool", c_bool[o])
                sp2.add_graph_output(f"{o}_int", c_int[o])
                sp2.add_graph_output(f"{o}_float", c_float[o])
                sp2.add_graph_output(f"{o}_timedelta", c_timedelta[o])
                sp2.add_graph_output(f"{o}_enum", c_enum[o])
                sp2.add_graph_output(f"{o}_list", c_list[o])
                sp2.add_graph_output(f"{o}_string", c_string[o])
                sp2.add_graph_output(f"{o}_struct", c_struct[o])

                sp2.add_graph_output(f"{o}_const_exclusive", c_const_exclusive[o])
                sp2.add_graph_output(f"{o}_const_inclusive", c_const_inclusive[o])
                sp2.add_graph_output(f"{o}_const_extrapolate", c_const_extrapolate[o])
                sp2.add_graph_output(f"{o}_timestamp_exclusive", c_duplicate_timestamp_exclusive[o])
                sp2.add_graph_output(f"{o}_timestamp_inclusive", c_duplicate_timestamp_inclusive[o])
                sp2.add_graph_output(f"{o}_timestamp_extrapolate", c_duplicate_timestamp_extrapolate[o])
                sp2.add_graph_output(f"{o}_extrapolate_short_window", c_extrapolate_short_window[o])
                sp2.add_graph_output(f"{o}_extrapolate_enum", c_extrapolate_enum[o])
                sp2.add_graph_output(f"{o}_enum_boundary", c_enum_boundary[o])
                sp2.add_graph_output(f"{o}_datetime_exclusive", c_duplicate_datetime_exclusive[o])
                sp2.add_graph_output(f"{o}_datetime_inclusive", c_duplicate_datetime_inclusive[o])
                sp2.add_graph_output(f"{o}_datetime_extrapolate", c_duplicate_datetime_extrapolate[o])

            sp2.add_graph_output("values_default", c_duplicate_datetime_extrapolate["values_default"])

        results = sp2.run(
            graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9) + timedelta(seconds=40)
        )

        # check types are correct
        for typ in ["bool", "int", "float", "timedelta", "enum", "list", "string", "struct"]:
            for o in ["values", "timestamps"]:
                self.assertIsInstance(results[f"{o}_{typ}"][-1][1], np.ndarray)

            self.assertIsInstance(results[f"items_{typ}"][-1][1], tuple)
            self.assertIsInstance(results[f"items_{typ}"][-1][1][0], np.ndarray)
            self.assertIsInstance(results[f"items_{typ}"][-1][1][1], np.ndarray)

            if typ in numpyType:
                self.assertEqual(results[f"values_{typ}"][-1][1].dtype, numpyType[typ])
            else:
                for elem in results[f"values_{typ}"][-1][1]:
                    self.assertIsInstance(elem, nonNativeType[typ])

            self.assertEqual(results[f"timestamps_{typ}"][-1][1].dtype, numpyType["datetime"])

        # check values are correct
        bool_values = [result[1] for result in results["values_bool"]]
        self.assertTrue(np.array_equal(bool_values[0], np.array([True])))
        self.assertTrue(np.array_equal(bool_values[1], np.array([True, True])))
        self.assertTrue(np.array_equal(bool_values[2], np.array([True, True, True])))
        self.assertTrue(np.array_equal(bool_values[3], np.array([True, True, True, True])))
        self.assertTrue(np.array_equal(bool_values[4], np.array([True, True, True, True, True])))
        self.assertTrue(np.array_equal(bool_values[-1], np.array([True, True, True, True, True])))

        int_values = [result[1] for result in results["values_int"]]
        self.assertTrue(np.array_equal(int_values[-1], np.array([36, 37, 38, 39, 40])))
        self.assertTrue(
            np.array_equal(int_values[-2], np.array([35, 36, 37, 38, 39]))
        )  # buffering policy is 5, so this tests wrap-around

        float_values = [result[1] for result in results["values_float"]]
        self.assertTrue(np.array_equal(float_values[-1], np.array([37, 38])))
        self.assertTrue(np.array_equal(float_values[-2], np.array([36, 37])))

        timedelta_values = [result[1] for result in results["values_timedelta"]]
        self.assertTrue(
            np.array_equal(
                timedelta_values[-1], np.array([np.timedelta64(timedelta(seconds=36 + i)) for i in range(3)])
            )
        )
        self.assertTrue(
            np.array_equal(
                timedelta_values[-2], np.array([np.timedelta64(timedelta(seconds=35 + i)) for i in range(3)])
            )
        )

        enum_values = [result[1] for result in results["values_enum"]]
        self.assertTrue(np.array_equal(enum_values[-1], np.array([MyEnum.first] * 3)))
        self.assertTrue(np.array_equal(enum_values[-2], np.array([MyEnum.first] * 3)))

        list_values = [result[1] for result in results["values_list"]]
        self.assertTrue(list_values[-1][0] == [1, 2, 3, 4])
        self.assertTrue(list_values[-1][1] == [1, 2, 3, 4])
        self.assertTrue(list_values[-2][0] == [1, 2, 3, 4])
        self.assertTrue(list_values[-2][1] == [1, 2, 3, 4])

        string_values = [result[1] for result in results["values_string"]]
        self.assertTrue(string_values[-1][0] == "v+1")

        struct_values = [result[1] for result in results["values_struct"]]
        self.assertTrue(struct_values[-1][2] == MyStruct(i=38, s="v+1", b=True))
        self.assertTrue(struct_values[-1][1] == MyStruct(i=37, s="v+1", b=True))
        self.assertTrue(struct_values[-1][0] == MyStruct(i=36, s="v+1", b=True))

        exclusive_const_values = [result[1] for result in results["values_const_exclusive"]]
        self.assertTrue(np.array_equal(exclusive_const_values[0], np.array([5])))
        self.assertTrue(np.array_equal(exclusive_const_values[3], np.array([5])))
        self.assertTrue(np.array_equal(exclusive_const_values[4], np.array([])))

        inclusive_const_values = [result[1] for result in results["values_const_inclusive"]]
        self.assertTrue(np.array_equal(inclusive_const_values[0], np.array([5])))
        self.assertTrue(np.array_equal(inclusive_const_values[4], np.array([5])))
        self.assertTrue(np.array_equal(inclusive_const_values[5], np.array([])))

        extrapolate_const_values = [result[1] for result in results["values_const_extrapolate"]]
        self.assertTrue(np.array_equal(extrapolate_const_values[0], np.array([5, 5])))
        self.assertTrue(np.array_equal(extrapolate_const_values[5], np.array([5, 5])))
        self.assertTrue(np.array_equal(extrapolate_const_values[-1], np.array([5, 5])))

        exclusive_timestamp_values = [result[1] for result in results["values_timestamp_exclusive"]]
        self.assertTrue(
            np.array_equal(exclusive_timestamp_values[-1], np.array([39]))
        )  # excludes 35, 36, 37, 38 since they were published at t=35
        self.assertTrue(np.array_equal(exclusive_timestamp_values[-2], np.array([])))  # includes t=35 to t=39 exclusive
        self.assertTrue(
            np.array_equal(exclusive_timestamp_values[-3], np.array([32, 33, 34]))
        )  # t=31 to t=35 exclusive
        self.assertTrue(
            np.array_equal(exclusive_timestamp_values[-4], np.array([32, 33, 34]))
        )  # 4 ticks at this timestamp
        self.assertTrue(np.array_equal(exclusive_timestamp_values[-5], np.array([32, 33, 34])))
        self.assertTrue(np.array_equal(exclusive_timestamp_values[-6], np.array([32, 33, 34])))
        self.assertTrue(
            np.array_equal(exclusive_timestamp_values[-7], np.array([31, 32, 33]))
        )  # t=30 to t=34 exclusive

        inclusive_timestamp_values = [result[1] for result in results["values_timestamp_inclusive"]]
        self.assertTrue(np.array_equal(inclusive_timestamp_values[-1], np.array([39, 40])))  # includes 36 to 40
        self.assertTrue(
            np.array_equal(inclusive_timestamp_values[-2], np.array([35, 36, 37, 38, 39]))
        )  # includes 35 to 39
        self.assertTrue(
            np.array_equal(inclusive_timestamp_values[-3], np.array([31, 32, 33, 34, 35, 36, 37, 38]))
        )  # includes 31 to 35
        self.assertTrue(np.array_equal(inclusive_timestamp_values[-4], np.array([31, 32, 33, 34, 35, 36, 37])))
        self.assertTrue(np.array_equal(inclusive_timestamp_values[-5], np.array([31, 32, 33, 34, 35, 36])))
        self.assertTrue(np.array_equal(inclusive_timestamp_values[-6], np.array([31, 32, 33, 34, 35])))
        self.assertTrue(np.array_equal(inclusive_timestamp_values[-7], np.array([30, 31, 32, 33, 34])))

        extrapolate_timestamp_values = [result[1] for result in results["values_timestamp_extrapolate"]]
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-1], np.array([38, 39, 40])))
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-2], np.array([38, 39])))
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-3], np.array([31, 32, 33, 34, 35, 36, 37, 38])))
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-4], np.array([31, 32, 33, 34, 35, 36, 37])))
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-5], np.array([31, 32, 33, 34, 35, 36])))
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-6], np.array([31, 32, 33, 34, 35])))
        self.assertTrue(np.array_equal(extrapolate_timestamp_values[-7], np.array([30, 31, 32, 33, 34])))

        extrapolate_timestamps = [result[1] for result in results["timestamps_timestamp_extrapolate"]]
        st = datetime(2020, 2, 7, 9)
        self.assertTrue(
            np.array_equal(
                extrapolate_timestamps[-1], np.array([np.datetime64(st + timedelta(seconds=i)) for i in [36, 39, 40]])
            )
        )
        self.assertTrue(
            np.array_equal(
                extrapolate_timestamps[-2], np.array([np.datetime64(st + timedelta(seconds=i)) for i in [35, 39]])
            )
        )
        self.assertTrue(
            np.array_equal(
                extrapolate_timestamps[-3],
                np.array([np.datetime64(st + timedelta(seconds=i)) for i in [31, 32, 33, 34, 35, 35, 35, 35]]),
            )
        )

        extrapolate_short_window_values = [result[1] for result in results["values_extrapolate_short_window"]]
        self.assertTrue(np.array_equal(extrapolate_short_window_values[-1], np.array([38, 39])))
        self.assertTrue(np.array_equal(extrapolate_short_window_values[-2], np.array([38, 38])))
        self.assertTrue(np.array_equal(extrapolate_short_window_values[-3], np.array([33, 34])))
        self.assertTrue(np.array_equal(extrapolate_short_window_values[-4], np.array([33, 34])))

        extrapolate_short_window_timestamps = [result[1] for result in results["timestamps_extrapolate_short_window"]]
        self.assertTrue(
            np.array_equal(
                extrapolate_short_window_timestamps[-1],
                np.array([np.datetime64(st + timedelta(seconds=i)) for i in [38, 39]]),
            )
        )
        self.assertTrue(
            np.array_equal(
                extrapolate_short_window_timestamps[-2],
                np.array([np.datetime64(st + timedelta(seconds=i)) for i in [37, 38]]),
            )
        )
        self.assertTrue(
            np.array_equal(
                extrapolate_short_window_timestamps[-3],
                np.array([np.datetime64(st + timedelta(seconds=i)) for i in [33, 34]]),
            )
        )
        self.assertTrue(
            np.array_equal(
                extrapolate_short_window_timestamps[-4],
                np.array([np.datetime64(st + timedelta(seconds=i)) for i in [33, 34]]),
            )
        )

        extrapolate_enum_values = [result[1] for result in results["values_extrapolate_enum"]]
        self.assertTrue(np.array_equal(extrapolate_enum_values[-1], np.array([MyEnum.second, MyEnum.first])))
        self.assertTrue(np.array_equal(extrapolate_enum_values[-2], np.array([MyEnum.second, MyEnum.second])))
        self.assertTrue(np.array_equal(extrapolate_enum_values[-3], np.array([MyEnum.first, MyEnum.first])))
        self.assertTrue(np.array_equal(extrapolate_enum_values[-4], np.array([MyEnum.first, MyEnum.first])))

        enum_boundary_values = [result[1] for result in results["values_enum_boundary"]]
        self.assertTrue(
            np.array_equal(
                enum_boundary_values[-1],
                np.array([MyEnum.first, MyEnum.second, MyEnum.second, MyEnum.second, MyEnum.first, MyEnum.first]),
            )
        )

        exclusive_datetime_values = [result[1] for result in results["values_datetime_exclusive"]]
        self.assertTrue(
            all(np.array_equal(exclusive_datetime_values[i], exclusive_timestamp_values[i]) for i in range(35))
        )

        inclusive_datetime_values = [result[1] for result in results["values_datetime_inclusive"]]
        self.assertTrue(
            all(np.array_equal(inclusive_datetime_values[i], inclusive_timestamp_values[i]) for i in range(35))
        )

        extrapolate_datetime_values = [result[1] for result in results["values_datetime_extrapolate"]]
        self.assertTrue(
            all(np.array_equal(extrapolate_datetime_values[i], extrapolate_timestamp_values[i]) for i in range(35))
        )

        extrapolate_datetime_timestamps = [result[1] for result in results["timestamps_datetime_extrapolate"]]
        self.assertTrue(
            all(np.array_equal(extrapolate_datetime_timestamps[i], extrapolate_timestamps[i]) for i in range(35))
        )

        # was a bug - tickbuffer would have garbage after being resized
        self.assertTrue(all(v <= 40 for v in results["values_default"][-1][1]))

    def test_leak(self):
        @sp2.node
        def n(x: sp2.ts[float]):
            with sp2.start():
                sp2.set_buffering_policy(x, tick_count=1000000)
            if sp2.ticked(x):
                if sp2.num_ticks(x) == 10000:
                    i = 0
                    while i < 10000:
                        _ = sp2.values_at(x)
                        _ = sp2.times_at(x)
                        _ = sp2.items_at(x)
                        i += 1

        def g():
            n(sp2.unroll(sp2.const.using(T=[int])(list(range(100000)))))

        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        sp2.run(g, starttime=datetime.utcnow(), endtime=timedelta(seconds=1))
        mem_after = process.memory_info().rss
        self.assertTrue(mem_after < mem_before * 10)

    def test_timedelta(self):
        @sp2.graph
        def graph():
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str="value", timestamp_delta=timedelta(seconds=1))
            _collect_value(x, getter_str="time", timestamp_delta=timedelta(seconds=1))
            _collect_value(x, getter_str="item", timestamp_delta=timedelta(seconds=1))

        _Globals.reset()
        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5))

        self.assertEqual({0: 4, 1: 3, 2: 2, 3: 1}, _Globals.instance().values)

        self.assertEqual(
            {
                0: datetime(2020, 2, 7, 9, 0, 4),
                1: datetime(2020, 2, 7, 9, 0, 3),
                2: datetime(2020, 2, 7, 9, 0, 2),
                3: datetime(2020, 2, 7, 9, 0, 1),
            },
            _Globals.instance().timestamps,
        )

        self.assertEqual(
            {
                0: (datetime(2020, 2, 7, 9, 0, 4), 4),
                1: (datetime(2020, 2, 7, 9, 0, 3), 3),
                2: (datetime(2020, 2, 7, 9, 0, 2), 2),
                3: (datetime(2020, 2, 7, 9, 0, 1), 1),
            },
            _Globals.instance().items,
        )

    def test_fixed_time(self):
        @sp2.graph
        def graph():
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str="value", fixed_time=datetime(2020, 2, 7, 9, 0, 2))
            _collect_value(x, getter_str="time", fixed_time=datetime(2020, 2, 7, 9, 0, 2))
            _collect_value(x, getter_str="item", fixed_time=datetime(2020, 2, 7, 9, 0, 2))

        @sp2.graph
        def graph_with_micros():
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str="value", fixed_time=datetime(2020, 2, 7, 9, 0, 2, 7))
            _collect_value(x, getter_str="time", fixed_time=datetime(2020, 2, 7, 9, 0, 2, 7))
            _collect_value(x, getter_str="item", fixed_time=datetime(2020, 2, 7, 9, 0, 2, 7))

        _Globals.reset()
        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5))

        self.assertEqual({0: 2}, _Globals.instance().values)
        self.assertEqual({0: datetime(2020, 2, 7, 9, 0, 2)}, _Globals.instance().timestamps)
        self.assertEqual({0: (datetime(2020, 2, 7, 9, 0, 2), 2)}, _Globals.instance().items)

        _Globals.reset()
        sp2.run(graph_with_micros, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5))

        self.assertEqual({0: 2}, _Globals.instance().values)
        self.assertEqual({0: datetime(2020, 2, 7, 9, 0, 2)}, _Globals.instance().timestamps)
        self.assertEqual({0: (datetime(2020, 2, 7, 9, 0, 2), 2)}, _Globals.instance().items)

    def test_timedelta_less_than_tick(self):
        @sp2.graph
        def graph():
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(5)])
            _collect_value(x, getter_str="value", timestamp_delta=timedelta(seconds=0.5))
            _collect_value(x, getter_str="time", timestamp_delta=timedelta(seconds=0.5))
            _collect_value(x, getter_str="item", timestamp_delta=timedelta(seconds=0.5))

        _Globals.reset()
        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5))

        self.assertEqual({0: 5, 1: 4, 2: 4, 3: 3, 4: 3}, _Globals.instance().values)

        self.assertEqual(
            {
                0: datetime(2020, 2, 7, 9, 0, 5),
                1: datetime(2020, 2, 7, 9, 0, 4),
                2: datetime(2020, 2, 7, 9, 0, 4),
                3: datetime(2020, 2, 7, 9, 0, 3),
                4: datetime(2020, 2, 7, 9, 0, 3),
            },
            _Globals.instance().timestamps,
        )
        self.assertEqual(
            {
                0: (datetime(2020, 2, 7, 9, 0, 5), 5),
                1: (datetime(2020, 2, 7, 9, 0, 4), 4),
                2: (datetime(2020, 2, 7, 9, 0, 4), 4),
                3: (datetime(2020, 2, 7, 9, 0, 3), 3),
                4: (datetime(2020, 2, 7, 9, 0, 3), 3),
            },
            _Globals.instance().items,
        )

    def test_missing_values(self):
        @sp2.node
        def no_ticks(x: ts["T"]) -> ts["T"]:
            return x

        @sp2.graph
        def graph():
            x = no_ticks(sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)]))
            _collect_value(x, getter_str="value")
            _collect_value(x, getter_str="time")
            _collect_value(x, getter_str="item")

        @sp2.graph
        def raising_graph(value_type: str, default_value: object = sp2.UNSET):
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str=value_type, force_min=5, default_value=default_value)

        @sp2.graph
        def raising_graph_time_delta(value_type: str, default_value: object = sp2.UNSET):
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str=value_type, timestamp_delta=timedelta(seconds=1), force_min=5)

        @sp2.graph
        def raising_graph_fixed_time(value_type: str, default_value: object = sp2.UNSET):
            x = sp2.curve(int, [(timedelta(seconds=v + 1), v + 1) for v in range(4)])
            _collect_value(x, getter_str=value_type, fixed_time=datetime(2020, 2, 7, 8), force_min=5)

        _Globals.reset()
        sp2.run(graph, starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5))

        _Globals.reset()
        sp2.run(
            lambda: raising_graph("value", 42), starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5)
        )
        self.assertEqual({0: 4, 1: 3, 2: 2, 3: 1, 4: 42}, _Globals.instance().values)

        _Globals.reset()
        sp2.run(
            lambda: raising_graph("time", datetime(2020, 2, 7, 8, 0, 0)),
            starttime=datetime(2020, 2, 7, 9),
            endtime=datetime(2020, 2, 7, 9, 5),
        )
        self.assertEqual(
            {
                0: datetime(2020, 2, 7, 9, 0, 4),
                1: datetime(2020, 2, 7, 9, 0, 3),
                2: datetime(2020, 2, 7, 9, 0, 2),
                3: datetime(2020, 2, 7, 9, 0, 1),
                4: datetime(2020, 2, 7, 8, 0),
            },
            _Globals.instance().timestamps,
        )

        _Globals.reset()
        sp2.run(
            lambda: raising_graph("item", (datetime(2020, 2, 7, 8, 0, 0), 42)),
            starttime=datetime(2020, 2, 7, 9),
            endtime=datetime(2020, 2, 7, 9, 5),
        )
        self.assertEqual(
            {
                0: (datetime(2020, 2, 7, 9, 0, 4), 4),
                1: (datetime(2020, 2, 7, 9, 0, 3), 3),
                2: (datetime(2020, 2, 7, 9, 0, 2), 2),
                3: (datetime(2020, 2, 7, 9, 0, 1), 1),
                4: (datetime(2020, 2, 7, 8, 0), 42),
            },
            _Globals.instance().items,
        )

        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph("value"), starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5)
            )
        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph("time"), starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5)
            )
        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph("item"), starttime=datetime(2020, 2, 7, 9), endtime=datetime(2020, 2, 7, 9, 5)
            )

        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph_time_delta("value"),
                starttime=datetime(2020, 2, 7, 9),
                endtime=datetime(2020, 2, 7, 9, 5),
            )
        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph_time_delta("time"),
                starttime=datetime(2020, 2, 7, 9),
                endtime=datetime(2020, 2, 7, 9, 5),
            )
        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph_time_delta("item"),
                starttime=datetime(2020, 2, 7, 9),
                endtime=datetime(2020, 2, 7, 9, 5),
            )

        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph_fixed_time("value"),
                starttime=datetime(2020, 2, 7, 9),
                endtime=datetime(2020, 2, 7, 9, 5),
            )
        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph_fixed_time("time"),
                starttime=datetime(2020, 2, 7, 9),
                endtime=datetime(2020, 2, 7, 9, 5),
            )
        with self.assertRaisesRegex(OverflowError, ".*No matching value found"):
            sp2.run(
                lambda: raising_graph_fixed_time("item"),
                starttime=datetime(2020, 2, 7, 9),
                endtime=datetime(2020, 2, 7, 9, 5),
            )

    def test_duplicate_policy(self):
        @sp2.node
        def check_value(x: ts[int], policy: sp2.DuplicatePolicy, count: int):
            with sp2.start():
                sp2.set_buffering_policy(x, tick_history=timedelta(seconds=1))

            if sp2.ticked(x) and sp2.num_ticks(x) == count + 1:
                t, v = sp2.item_at(x, timedelta(seconds=-1), duplicate_policy=policy)
                self.assertEqual(t, sp2.now() - timedelta(seconds=1))
                if policy == sp2.DuplicatePolicy.LAST_VALUE:
                    self.assertEqual(v, count)
                else:
                    self.assertEqual(v, 1)

        def graph(policy: sp2.DuplicatePolicy, num_ticks: int):
            c = sp2.curve(
                int,
                [(timedelta(seconds=0), v + 1) for v in range(0, num_ticks)] + [(timedelta(seconds=1), num_ticks + 1)],
            )
            check_value(c, policy, num_ticks)

        for count in range(1, 10):
            sp2.run(graph, sp2.DuplicatePolicy.FIRST_VALUE, count, starttime=datetime(2020, 6, 18))
            sp2.run(graph, sp2.DuplicatePolicy.LAST_VALUE, count, starttime=datetime(2020, 6, 18))

    def test_out_of_bounds_exceptions(self):
        @sp2.node
        def check(x: ts[object], index: int = None, td: timedelta = None, fixed: datetime = None):
            with sp2.start():
                sp2.set_buffering_policy(x, 10, timedelta(seconds=10))

            if sp2.ticked(x):
                if index is not None:
                    dummy = sp2.value_at(x, index, default=0)
                if td is not None:
                    dummy = sp2.value_at(x, td, default=0)
                if fixed is not None:
                    dummy = sp2.value_at(x, fixed, default=0)

        x = sp2.const(1)
        # control
        sp2.run(check, x, 0, starttime=datetime(2020, 11, 11))
        sp2.run(check, x, None, -timedelta(seconds=1), starttime=datetime(2020, 11, 11))
        sp2.run(check, x, None, None, datetime(2020, 11, 11), starttime=datetime(2020, 11, 11))

        with self.assertRaisesRegex(
            IndexError, "requesting data at index 20 with buffer policy set to 10 ticks in node 'check'"
        ):
            sp2.run(check, x, -20, starttime=datetime(2020, 11, 11))

        with self.assertRaisesRegex(
            IndexError,
            "requesting data at timedelta -1 day, 23:59:40 with buffer policy set to 0:00:10 in node 'check'",
        ):
            sp2.run(check, x, None, -timedelta(seconds=20), starttime=datetime(2020, 11, 11))

        with self.assertRaisesRegex(
            IndexError,
            "requesting datetime 2020-11-10 00:00:00 at time 2020-11-11 00:00:00 "
            "with buffer time window policy set to 0:00:10 in node 'check'",
        ):
            sp2.run(check, x, None, None, datetime(2020, 11, 10), starttime=datetime(2020, 11, 11))

    def test_graph_output(self):
        # This wa a bug when only setting time_history without tickcount, it wasnt taking effect
        def graph(x):
            # We samepl to avoid setting multiple policies on same input
            sp2.add_graph_output("1sec", sp2.sample(x, x), tick_history=timedelta(seconds=1))
            sp2.add_graph_output("1tick", sp2.sample(x, x), tick_count=1)
            sp2.add_graph_output("default", sp2.sample(x, x))

        with sp2.memoize(False):
            rv = sp2.run(
                graph,
                sp2.count(sp2.timer(timedelta(seconds=1))),
                starttime=datetime(2021, 1, 1),
                endtime=timedelta(seconds=5),
            )
        self.assertEqual(len(rv["1sec"]), 2)

        self.assertEqual(len(rv["1tick"]), 1)
        self.assertEqual(rv["1tick"][0][1], 5)

        self.assertEqual(len(rv["default"]), 5)


if __name__ == "__main__":
    unittest.main()
