import sys
import unittest
from datetime import date, datetime, timedelta
from typing import Callable, Dict, List

import sp2
from sp2 import OutputBasket, Outputs, OutputTypeError, Sp2ParseError, __outputs__, __return__, ts
from sp2.impl.types.instantiation_type_resolver import ArgTypeMismatchError


class TestParsing(unittest.TestCase):
    def test_parse_errors(self):
        # These are roughly in order of exceptions that are thrown in node_parser.py ( as of the time of this writing )

        with self.assertRaisesRegex(Sp2ParseError, "Passing arguments with \\* is unsupported for make_passive"):

            @sp2.node
            def foo():
                args = []
                sp2.make_passive(*args)

        with self.assertRaisesRegex(Sp2ParseError, "Passing arguments with \\*\\* is unsupported for make_passive"):

            @sp2.node
            def foo(x: ts[int]):
                kwargs = {}
                sp2.make_passive(x, **kwargs)

        with self.assertRaisesRegex(Sp2ParseError, "make_passive expects a timeseries as first positional argument"):

            @sp2.node
            def foo():
                sp2.make_passive(x=1)

        with self.assertRaisesRegex(Sp2ParseError, "make_passive expects a timeseries as first positional argument"):

            @sp2.node
            def foo():
                sp2.make_passive()

        with self.assertRaisesRegex(Sp2ParseError, "value_at\\(\\) got multiple values for argument 'index_or_time'"):

            @sp2.node
            def foo(x: ts[int]):
                sp2.value_at(x, 1, index_or_time=1)

        with self.assertRaisesRegex(Sp2ParseError, "Invalid use of 'with_shape'"):

            @sp2.node
            def foo(x: [str]):
                __outputs__([ts[int]].with_shape(x=1))
                pass

        with self.assertRaisesRegex(Sp2ParseError, "__outputs__ must all be named or be single output, cant be both"):

            @sp2.node
            def foo(x: [str]):
                __outputs__(ts[int], x=ts[bool])
                pass

        with self.assertRaisesRegex(Sp2ParseError, "__outputs__ single unnamed arg only"):

            @sp2.node
            def foo(x: [str]):
                __outputs__(ts[int], ts[bool])
                pass

        with self.assertRaisesRegex(
            OutputTypeError, "Outputs must all be named or be a single unnamed output, cant be both"
        ):

            @sp2.node
            def foo(x: [str]) -> Outputs(ts[int], ts[bool]):
                pass

        with self.assertRaisesRegex(
            OutputTypeError, "Outputs must all be named or be a single unnamed output, cant be both"
        ):

            @sp2.node
            def foo(x: [str]) -> Outputs(ts[int], x=ts[bool]):
                pass

        with self.assertRaisesRegex(
            Sp2ParseError, "sp2.node and sp2.graph outputs must be via return annotation or __outputs__ call, not both"
        ):

            @sp2.node
            def foo(x: [str]) -> Outputs(ts[int]):
                __outputs__(ts[int])
                pass

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Invalid usage of __outputs__, it should appear at the beginning of the function \\(consult documentation for details\\)",
        ):

            @sp2.node
            def foo(x: [str]):
                x = 1
                __outputs__(ts[int])

        with self.assertRaisesRegex(Sp2ParseError, "\\*args and \\*\\*kwargs arguments are not supported in sp2 nodes"):

            @sp2.node
            def foo(*args):
                __outputs__(ts[int])
                pass

        if sys.version_info.major > 3 or sys.version_info.minor >= 8:
            with self.assertRaisesRegex(Sp2ParseError, "position only arguments are not supported in sp2 nodes"):

                @sp2.node
                def posonly_sample(
                    posonlyargs,
                    /,
                ):
                    __outputs__(ts[int])
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.node and sp2.graph args must be type annotated"):

            @sp2.node
            def foo(x):
                __outputs__(ts[int])
                pass

        with self.assertRaisesRegex(Sp2ParseError, "__alarms__ does not accept positional arguments"):

            @sp2.node
            def foo():
                __alarms__(x)
                pass

        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def foo():
                with __alarms__():
                    x = 5
                pass

        with self.assertRaisesRegex(Sp2ParseError, "alarms must be ts types"):

            @sp2.node
            def foo():
                __alarms__(x=int)
                pass

        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def foo():
                with __alarms__():
                    x: int = 5
                pass

        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def foo():
                with __alarms__():
                    x: ts[int]
                pass

        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def foo():
                with __alarms__():
                    x: ts[int] = 5
                pass

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized input 'z'"):

            @sp2.node
            def foo():
                sp2.make_passive(z)

        with self.assertRaisesRegex(Sp2ParseError, "expected 'z' to be a timeseries input"):

            @sp2.node
            def foo(z: int):
                sp2.make_passive(z)

        with self.assertRaisesRegex(Sp2ParseError, "invalid sp2 call sp2.make_cpassive"):

            @sp2.node
            def foo():
                sp2.make_cpassive()

        with self.assertRaisesRegex(Sp2ParseError, "returning from within a for or while loop is not supported"):

            @sp2.node
            def foo():
                __outputs__(ts[int])
                for _ in range(10):
                    return 1

        with self.assertRaisesRegex(Sp2ParseError, "returning from within a for or while loop is not supported"):

            @sp2.node
            def foo() -> Outputs(ts[int]):
                for _ in range(10):
                    return 1

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def foo():
                __outputs__(x=ts[int], y=ts[int])
                return 1

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def foo() -> Outputs(x=ts[int], y=ts[int]):
                return 1

        with self.assertRaisesRegex(Sp2ParseError, ".*single unnamed arg in node returning 2 outputs.*"):

            @sp2.node
            def foo():
                __outputs__(x=ts[int], y=ts[int])
                __return__(1)

        with self.assertRaisesRegex(Sp2ParseError, ".*single unnamed arg in node returning 2 outputs.*"):

            @sp2.node
            def foo() -> Outputs(x=ts[int], y=ts[int]):
                __return__(1)

        with self.assertRaisesRegex(Sp2ParseError, "returning from node without any outputs defined"):

            @sp2.node
            def foo(x: ts[int]):
                return 1

        with self.assertRaisesRegex(Sp2ParseError, "returning from node without any outputs defined"):

            @sp2.node
            def foo(x: ts[int]):
                return __return__(1)

        with self.assertRaisesRegex(
            Sp2ParseError,
            "sp2.output expects to be called with \\(output, value\\) or \\(output = value, output2 = value2\\)",
        ):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(ts[int])
                sp2.output(1, 2, 3)

        with self.assertRaisesRegex(
            Sp2ParseError,
            "sp2.output expects to be called with \\(output, value\\) or \\(output = value, output2 = value2\\)",
        ):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(ts[int]):
                sp2.output(1, 2, 3)

        with self.assertRaisesRegex(
            Sp2ParseError,
            "return expects to be called with \\(output, value\\) or \\(output = value, output2 = value2\\)",
        ):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(ts[int])
                __return__(1, 2, 3)

        with self.assertRaisesRegex(
            Sp2ParseError,
            "return expects to be called with \\(output, value\\) or \\(output = value, output2 = value2\\)",
        ):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(ts[int]):
                __return__(1, 2, 3)

        with self.assertRaisesRegex(Sp2ParseError, "cannot sp2.output single unnamed arg in node returning 2 outputs"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(x=ts[int], y=ts[bool])
                sp2.output(5)

        with self.assertRaisesRegex(Sp2ParseError, "cannot sp2.output single unnamed arg in node returning 2 outputs"):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(x=ts[int], y=ts[bool]):
                sp2.output(5)

        with self.assertRaisesRegex(Sp2ParseError, "cannot return single unnamed arg in node returning 2 outputs"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(x=ts[int], y=ts[bool])
                __return__(5)

        with self.assertRaisesRegex(Sp2ParseError, "cannot return single unnamed arg in node returning 2 outputs"):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(x=ts[int], y=ts[bool]):
                __return__(5)

        with self.assertRaisesRegex(Sp2ParseError, "returning from node without any outputs defined"):

            @sp2.node
            def foo(x: ts[int]):
                sp2.output(5)

        with self.assertRaisesRegex(Sp2ParseError, "returning from node without any outputs defined"):

            @sp2.node
            def foo(x: ts[int]):
                __return__(5)

        with self.assertRaisesRegex(
            Sp2ParseError, "sp2.output\\(x\\[k\\],v\\) syntax can only be used on basket outputs"
        ):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(x=ts[bool])
                sp2.output(x[1], 7)

        with self.assertRaisesRegex(
            Sp2ParseError, "sp2.output\\(x\\[k\\],v\\) syntax can only be used on basket outputs"
        ):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(x=ts[bool]):
                sp2.output(x[1], 7)

        with self.assertRaisesRegex(
            Sp2ParseError, "Invalid use of return basket element returns is not possible with return"
        ):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(x=ts[bool])
                __return__(x[1], 7)

        with self.assertRaisesRegex(
            Sp2ParseError, "Invalid use of return basket element returns is not possible with return"
        ):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(x=ts[bool]):
                __return__(x[1], 7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(z=ts[bool])
                sp2.output(x, 7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(z=ts[bool]):
                sp2.output(x, 7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(z=ts[bool])
                __return__(x, 7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(z=ts[bool]):
                __return__(x, 7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(z=ts[bool])
                sp2.output(x=7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(z=ts[bool]):
                sp2.output(x=7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(z=ts[bool])
                __return__(x=7)

        with self.assertRaisesRegex(Sp2ParseError, "unrecognized output 'x'"):

            @sp2.node
            def foo(x: ts[int]) -> Outputs(z=ts[bool]):
                __return__(x=7)

        with self.assertRaisesRegex(Sp2ParseError, "sp2.now takes no arguments"):

            @sp2.node
            def foo(x: ts[int]):
                sp2.now(5)

        with self.assertRaisesRegex(Sp2ParseError, "sp2.now takes no arguments"):

            @sp2.node
            def foo(x: ts[int]):
                sp2.now(x=5)

        with self.assertRaisesRegex(Sp2ParseError, "cannot schedule alarm on non-alarm input 'x'"):

            @sp2.node
            def foo(x: ts[int]):
                sp2.schedule_alarm(x)

        with self.assertRaisesRegex(
            Sp2ParseError, "node has __outputs__ defined but no return or sp2.output statements"
        ):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(ts[int])
                if sp2.ticked(x):
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "output 'y' is never returned"):

            @sp2.node
            def foo(x: ts[int]):
                __outputs__(x=ts[int], y=ts[int])
                if sp2.ticked(x):
                    sp2.output(x=1)

        with self.assertRaisesRegex(Sp2ParseError, r"outputs must be ts\[\] or basket types, got <class \'dict\'\>"):

            @sp2.node
            def foo():
                __outputs__(dict)
                pass

        with self.assertRaisesRegex(
            Sp2ParseError, "output baskets must define shape using with_shape or with_shape_of"
        ):

            @sp2.node
            def foo():
                __outputs__(x={str: ts[int]})
                pass

        with self.assertRaisesRegex(
            Sp2ParseError, "output baskets must define shape using with_shape or with_shape_of"
        ):

            @sp2.node
            def foo():
                __outputs__(x=[ts[int]])
                pass

    def test_special_block(self):
        with self.assertRaisesRegex(Sp2ParseError, "__outputs__ can not be used in a with statement"):

            @sp2.node
            def foo():
                with __outputs__():
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "__start__ must be used in a with statement"):

            @sp2.node
            def foo():
                __start__()

        with self.assertRaisesRegex(Sp2ParseError, "__stop__ must be used in a with statement"):

            @sp2.node
            def foo():
                __stop__()

        @sp2.node
        def foo():
            __alarms__()

        @sp2.node
        def foo():
            __state__(x=10)

        @sp2.node
        def foo():
            __alarms__()
            __state__(x=10)

        @sp2.node
        def foo():
            with __alarms__():
                pass

        @sp2.node
        def foo():
            with __alarms__():
                ...

        @sp2.node
        def foo():
            with __state__(x=10):
                pass

        @sp2.node
        def foo():
            with __state__(x=10):
                ...

        @sp2.node
        def foo():
            with __alarms__():
                pass
            with __state__(x=10):
                pass

        @sp2.node
        def foo():
            with __alarms__(y=ts[int]):
                pass
            with __state__(x=10):
                pass

        @sp2.node
        def foo():
            with __alarms__():
                y: ts[int] = sp2.alarm(int)
            with __state__(x=10):
                pass

        @sp2.node
        def foo():
            with __alarms__():
                y: ts[bool] = sp2.alarm(bool)
            with __state__(x=10):
                pass
            with __start__():
                sp2.schedule_alarm(y, 4, True)

        with self.assertRaisesRegex(Sp2ParseError, "__alarms__ does not accept positional arguments"):

            @sp2.node
            def foo():
                with __alarms__(ts[int]):
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "__alarms__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with __alarms__:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "__state__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with __state__:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.__state__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.__state__:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "__start__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with __start__:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.__start__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.__start__:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "__stop__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with __stop__:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.__stop__ must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.__stop__:
                    pass

        @sp2.node
        def foo():
            __outputs__(x=ts[int])
            __alarms__(y=ts[int])
            __state__(z=1)
            with __start__():
                pass
            with __stop__():
                pass
            __return__(x=1)

        @sp2.node
        def foo():
            __outputs__(x=ts[int])
            __alarms__(y=ts[int])
            __state__(z=1)
            with __start__():
                ...
            with __stop__():
                ...
            __return__(x=1)

        @sp2.node
        def foo():
            return

        with self.assertRaisesRegex(Sp2ParseError, "__outputs__ must be declared before __stop__"):

            @sp2.node
            def foo():
                __alarms__(y=ts[int])
                __state__(z=1)
                with __start__():
                    pass
                with __stop__():
                    pass
                __outputs__(x=ts[int])

                __return__(x=1)

        with self.assertRaisesRegex(Sp2ParseError, "__alarms__ must be declared before __state__"):

            @sp2.node
            def foo():
                __outputs__(x=ts[int])
                __state__(z=1)
                __alarms__(y=ts[int])
                with __start__():
                    pass
                with __stop__():
                    pass

                __return__(x=1)

        with self.assertRaisesRegex(Sp2ParseError, "__state__ must be declared before __start__"):

            @sp2.node
            def foo():
                __outputs__(x=ts[int])
                __alarms__(y=ts[int])
                with __start__():
                    pass
                __state__(z=1)
                with __stop__():
                    pass

                __return__(x=1)

        with self.assertRaisesRegex(Sp2ParseError, "__start__ must be declared before __stop__"):

            @sp2.node
            def foo():
                __outputs__(x=ts[int])
                __alarms__(y=ts[int])
                __state__(z=1)
                with __stop__():
                    pass
                with __start__():
                    pass

                __return__(x=1)

        with self.assertRaisesRegex(Sp2ParseError, "start must be declared before __stop__"):

            @sp2.node
            def foo():
                with __stop__():
                    pass
                with sp2.start():
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "__start__ must be declared before stop"):

            @sp2.node
            def foo():
                with sp2.stop():
                    pass
                with __start__():
                    pass

        #  test with mixed pythonic/dunder syntax
        @sp2.node
        def foo():
            with sp2.start():
                pass
            with __stop__():
                pass

        @sp2.node
        def foo():
            with __start__():
                pass
            with sp2.stop():
                pass

        with self.assertRaisesRegex(Sp2ParseError, "Invalid usage of __stop__, .*"):

            @sp2.node
            def foo():
                __outputs__(x=ts[int])
                __alarms__(y=ts[int])
                __state__(z=1)
                with __start__():
                    pass
                __return__(x=1)
                with __stop__():
                    pass

    def test_method_parsing(self):
        class C:
            @sp2.node
            def f(self, x: int):
                pass

        with self.assertRaises(Sp2ParseError):

            class C:
                @sp2.node
                def f(self, x):
                    pass

        with self.assertRaises(Sp2ParseError):

            @sp2.node
            def f(self, x: int):
                pass

        class C:
            @sp2.graph
            def f(self, x: int):
                pass

        with self.assertRaises(Sp2ParseError):

            class C:
                @sp2.graph
                def f(self, x):
                    pass

        with self.assertRaises(Sp2ParseError):

            @sp2.graph
            def f(self, x: int):
                pass

    def test_classmethod_parsing(self):
        class C:
            @classmethod
            @sp2.node
            def f(cls, x: int):
                pass

        with self.assertRaises(Sp2ParseError):

            class C:
                @sp2.node
                def f(cls, x):
                    pass

        with self.assertRaises(Sp2ParseError):

            @sp2.node
            def f(cls, x: int):
                pass

        class C:
            @classmethod
            @sp2.graph
            def f(cls, x: int):
                pass

        with self.assertRaises(Sp2ParseError):

            class C:
                @sp2.graph
                def f(cls, x):
                    pass

        with self.assertRaises(Sp2ParseError):

            @sp2.graph
            def f(cls, x: int):
                pass

    def test_graph_return_parsing(self):
        @sp2.graph
        def graph():
            __outputs__(ts[int])
            return sp2.const(5)

        @sp2.graph
        def graph():
            __outputs__(ts[int])
            __return__(sp2.const(5))

        @sp2.graph
        def graph():
            __outputs__(ts[int])
            __return__(sp2.const(5))

        @sp2.graph
        def graph():
            __outputs__(x=ts[int])
            return sp2.const(5)

        @sp2.graph
        def graph():
            __outputs__(x=ts[int])
            __return__(sp2.const(5))

        @sp2.graph
        def graph():
            __outputs__(x=ts[int])
            __return__(x=sp2.const(5))

        @sp2.graph
        def graph():
            __outputs__(x=ts[int], y=ts[float])
            __return__(x=sp2.const(5), y=sp2.const(6.0))

        with self.assertRaisesRegex(Sp2ParseError, "return does not return values with non empty outputs"):

            @sp2.graph
            def graph():
                __outputs__(ts[int])
                return

        with self.assertRaisesRegex(Sp2ParseError, "return does not return values with non empty outputs"):

            @sp2.graph
            def graph() -> Outputs(ts[int]):
                return

        with self.assertRaisesRegex(Sp2ParseError, "return does not return values with non empty outputs"):

            @sp2.graph
            def graph():
                __outputs__(ts[int])
                __return__()

        with self.assertRaisesRegex(Sp2ParseError, "return does not return values with non empty outputs"):

            @sp2.graph
            def graph() -> Outputs(ts[int]):
                __return__()

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.graph
            def graph():
                __outputs__(x=ts[int], y=ts[int])
                return sp2.const(5)

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.graph
            def graph() -> Outputs(x=ts[int], y=ts[int]):
                return sp2.const(5)

        with self.assertRaisesRegex(Sp2ParseError, "cannot return single unnamed arg in graph returning 2 outputs"):

            @sp2.graph
            def graph():
                __outputs__(x=ts[int], y=ts[int])
                __return__(sp2.const(5))

        with self.assertRaisesRegex(Sp2ParseError, "cannot return single unnamed arg in graph returning 2 outputs"):

            @sp2.graph
            def graph() -> Outputs(x=ts[int], y=ts[int]):
                __return__(sp2.const(5))

        with self.assertRaisesRegex(
            Sp2ParseError, "return expects to be called with \\(value\\) or \\(output = value, output2 = value2\\)"
        ):

            @sp2.graph
            def graph():
                __outputs__(x=ts[int], y=ts[float])
                __return__(sp2.const(5), sp2.const(6.0))

        with self.assertRaisesRegex(
            Sp2ParseError, "return expects to be called with \\(value\\) or \\(output = value, output2 = value2\\)"
        ):

            @sp2.graph
            def graph() -> Outputs(x=ts[int], y=ts[float]):
                __return__(sp2.const(5), sp2.const(6.0))

        # Test basket output types
        @sp2.graph
        def graph():
            __outputs__({str: ts[int]})
            return {"x": sp2.const(5), "y": sp2.const(6.0)}

        @sp2.graph
        def graph():
            __outputs__([ts[int]])
            return [sp2.const(5), sp2.const(6.0)]

        @sp2.graph
        def graph() -> Outputs({str: ts[int]}):
            return {"x": sp2.const(5), "y": sp2.const(6.0)}

        @sp2.graph
        def graph() -> {str: ts[int]}:
            return {"x": sp2.const(5), "y": sp2.const(6.0)}

        @sp2.graph
        def graph() -> Outputs([ts[int]]):
            return [sp2.const(5), sp2.const(6.0)]

        @sp2.graph
        def graph() -> [ts[int]]:
            return [sp2.const(5), sp2.const(6.0)]

        # basket types with promotion
        @sp2.graph
        def graph():
            __outputs__({str: ts[int]})
            __return__({"x": sp2.const(5), "y": sp2.const(6.0)})

        @sp2.graph
        def graph():
            __outputs__([ts[int]])
            __return__([sp2.const(5), sp2.const(6.0)])

        @sp2.graph
        def graph() -> Outputs({str: ts[int]}):
            __return__({"x": sp2.const(5), "y": sp2.const(6.0)})

        @sp2.graph
        def graph() -> {str: ts[int]}:
            __return__({"x": sp2.const(5), "y": sp2.const(6.0)})

        @sp2.graph
        def graph() -> Outputs([ts[int]]):
            __return__([sp2.const(5), sp2.const(6.0)])

        @sp2.graph
        def graph() -> [ts[int]]:
            __return__([sp2.const(5), sp2.const(6.0)])

    def test_list_inside_callable(self):
        """was a bug "Empty list inside callable annotation raises exception" """

        @sp2.graph
        def graph(v: Dict[str, Callable[[], str]]):
            pass

    def test_graph_caching_parsing(self):
        with self.assertRaisesRegex(
            NotImplementedError, "Caching is unsupported for argument type typing.List\\[int\\] \\(argument x\\)"
        ):

            @sp2.graph(cache=True)
            def graph(x: List[int]):
                __outputs__(o=ts[int])
                pass

        with self.assertRaisesRegex(
            NotImplementedError, "Caching is unsupported for argument type typing.Dict\\[int, int\\] \\(argument x\\)"
        ):

            @sp2.graph(cache=True)
            def graph(x: Dict[int, int]):
                __outputs__(o=ts[int])
                pass

        with self.assertRaisesRegex(NotImplementedError, "Caching of list basket outputs is unsupported"):

            @sp2.graph(cache=True)
            def graph():
                __outputs__(o=[ts[int]])
                pass

        @sp2.graph(cache=True)
        def graph(a1: datetime, a2: date, a3: int, a4: float, a5: str, a6: bool):
            __outputs__(o=ts[int])
            pass

    def test_list_default_value(self):
        # There was a bug parsing list default value
        @sp2.graph
        def g(x: List[int] = [1, 2, 3]):
            pass

    def test_wrong_parse_error(self):
        @sp2.graph
        def g(x: {str: sp2.ts[float]}):
            pass

        @sp2.graph
        def g2():
            __outputs__({str: sp2.ts[object]})
            return {"A": sp2.null_ts(object)}

        def main():
            g(g2())

        with self.assertRaisesRegex(ArgTypeMismatchError, ".*Expected typing.Dict.*got.*"):
            main()

    def test_bad_parse_message(self):
        with self.assertRaisesRegex(Sp2ParseError, "Invalid use of sp2.output please consult documentation"):

            @sp2.node
            def x():
                __outputs__(x=ts[int])
                sp2.output("x", 1)

    def test_output_annotation_parsing_nodes(self):
        @sp2.node
        def my_node(x: ts[int], y: ts[int]) -> Outputs(ts[int]):
            if sp2.ticked(x, y):
                __return__(x + y)

        @sp2.node
        def my_node2(x: ts[int], y: ts[int]) -> Outputs(my_output=ts[int]):
            if sp2.ticked(x, y):
                __return__(my_output=x + y)

        @sp2.node
        def my_node3(x: ts[int], y: ts[int]) -> Outputs(x=ts[int], y=ts[int]):
            if sp2.ticked(x):
                sp2.output(x=x)
            if sp2.ticked(y):
                __return__(y=y)

        class MyOutputs(Outputs):
            x: ts[int]
            y: ts[int]

        @sp2.node
        def my_node4(x: ts[int], y: ts[int]) -> MyOutputs:
            if sp2.ticked(x):
                sp2.output(x=x)
            if sp2.ticked(y):
                __return__(y=y)

        @sp2.node
        def my_node5(x: ts[int], y: ts[int]) -> ts[int]:
            if sp2.ticked(x, y):
                return x + y

        # @sp2.graph
        # def my_graph():
        #     sp2.print("out1", my_node(sp2.const(1), sp2.const(2)))
        #     sp2.print("out2", my_node2(sp2.const(1), sp2.const(2)))

        #     node3 = my_node3(sp2.const(1), sp2.const(2))
        #     sp2.print("out3.x", node3.x)
        #     sp2.print("out3.y", node3.y)

        #     node4 = my_node4(sp2.const(1), sp2.const(2))
        #     sp2.print("out4.x", node4.x)
        #     sp2.print("out4.y", node4.y)

        #     sp2.print("out5", my_node5(sp2.const(1), sp2.const(2)))

    def test_output_annotation_parsing_graphs(self):
        @sp2.graph
        def graph() -> Outputs({str: ts[int]}):
            return {"x": sp2.const(5), "y": sp2.const(6.0)}

        @sp2.graph
        def graph() -> {str: ts[int]}:
            return {"x": sp2.const(5), "y": sp2.const(6.0)}

        @sp2.graph
        def graph() -> Outputs([ts[int]]):
            return [sp2.const(5), sp2.const(6.0)]

        @sp2.graph
        def graph() -> [ts[int]]:
            return [sp2.const(5), sp2.const(6.0)]

        @sp2.graph
        def graph() -> Outputs({str: ts[int]}):
            __return__({"x": sp2.const(5), "y": sp2.const(6.0)})

        @sp2.graph
        def graph() -> {str: ts[int]}:
            __return__({"x": sp2.const(5), "y": sp2.const(6.0)})

        @sp2.graph
        def graph() -> Outputs([ts[int]]):
            __return__([sp2.const(5), sp2.const(6.0)])

        @sp2.graph
        def graph() -> [ts[int]]:
            __return__([sp2.const(5), sp2.const(6.0)])

    def test_output_annotation_parsing_baskets(self):
        @sp2.node
        def my_node_1_1(x: Dict[str, ts[str]], y: List[str]) -> Outputs(OutputBasket(Dict[str, ts[str]], shape="y")):
            if sp2.ticked(x):
                return x

        my_node_1_1({"x": sp2.const("x ")}, ["x"])

        @sp2.node
        def my_node_1_2(x: Dict[str, ts[str]]) -> Outputs(OutputBasket(Dict[str, ts[str]], shape_of="x")):
            if sp2.ticked(x):
                return x

        my_node_1_2({"x": sp2.const("x ")})

        @sp2.node
        def my_node_2_1(x: Dict[str, ts[str]], y: List[str]) -> Outputs(OutputBasket({str: ts[str]}, shape="y")):
            if sp2.ticked(x):
                return x

        my_node_2_1({"x": sp2.const("x ")}, ["x"])

        @sp2.node
        def my_node_2_2(x: Dict[str, ts[str]]) -> Outputs(OutputBasket({str: ts[str]}, shape_of="x")):
            if sp2.ticked(x):
                return x

        my_node_2_2({"x": sp2.const("x")})

        @sp2.node
        def my_node_3_1(x: List[ts[str]], y: int) -> OutputBasket(List[ts[str]], shape="y"):
            if sp2.ticked(x):
                return x

        my_node_3_1([sp2.const("x")], 1)

        @sp2.node
        def my_node_3_2(x: List[ts[str]]) -> OutputBasket(List[ts[str]], shape_of="x"):
            if sp2.ticked(x):
                return x

        my_node_3_2([sp2.const("x")])

        @sp2.node
        def my_node_4_1(x: List[ts[str]], y: int) -> Outputs(OutputBasket(List[ts[str]], shape="y")):
            if sp2.ticked(x):
                return x

        my_node_4_1([sp2.const("x")], 1)

        @sp2.node
        def my_node_4_2(x: List[ts[str]]) -> Outputs(OutputBasket(List[ts[str]], shape_of="x")):
            if sp2.ticked(x):
                return x

        my_node_4_2([sp2.const("x")])

        @sp2.node
        def my_node_4_3(x: ts[int]) -> Outputs(OutputBasket(Dict[str, ts[str]], shape=["a", "b", "c"])):
            if sp2.ticked(x):
                return x

        my_node_4_3(sp2.const(1))

        @sp2.node
        def my_node_4_4(x: ts[int]) -> Outputs(OutputBasket(List[ts[int]], shape=10)):
            if sp2.ticked(x):
                return x

        my_node_4_4(sp2.const(1))

        @sp2.node
        def my_node_5_1(x: ts[int]) -> {ts[str]: ts[str]}:
            return {}

        my_node_5_1(sp2.const(1))

        @sp2.node
        def my_node_5_2(x: ts[int]) -> OutputBasket({ts[str]: ts[str]}):
            return {}

        my_node_5_2(sp2.const(1))

    def test_output_annotation_parsing_graph_baskets(self):
        @sp2.graph
        def my_graph_1_1(x: Dict[str, ts[str]], y: List[str]) -> Outputs(OutputBasket(Dict[str, ts[str]], shape="y")):
            return x

        my_graph_1_1({"x": sp2.const("x ")}, ["x"])

        @sp2.graph
        def my_graph_1_2(x: Dict[str, ts[str]]) -> Outputs(OutputBasket(Dict[str, ts[str]], shape_of="x")):
            return x

        my_graph_1_2({"x": sp2.const("x ")})

        @sp2.graph
        def my_graph_1_3(x: Dict["K", ts[str]]) -> OutputBasket({"K": ts[str]}, shape_of="x"):
            return x

        my_graph_1_3({"x": sp2.const("x ")})

        @sp2.graph
        def my_graph_2_1(x: Dict[str, ts[str]], y: List[str]) -> Outputs(OutputBasket({str: ts[str]}, shape="y")):
            return x

        my_graph_2_1({"x": sp2.const("x ")}, ["x"])

        @sp2.graph
        def my_graph_2_2(x: Dict[str, ts[str]]) -> Outputs(OutputBasket({str: ts[str]}, shape_of="x")):
            return x

        my_graph_2_2({"x": sp2.const("x ")})

        @sp2.graph
        def my_graph_3_1(x: List[ts[str]], y: int) -> OutputBasket(List[ts[str]], shape="y"):
            return x

        my_graph_3_1([sp2.const("x")], 1)

        @sp2.graph
        def my_graph_3_2(x: List[ts[str]]) -> OutputBasket(List[ts[str]], shape_of="x"):
            return x

        my_graph_3_2([sp2.const("x")])

        @sp2.graph
        def my_graph_3_3(x: List[ts["T"]]) -> OutputBasket(List[ts["T"]], shape_of="x"):
            return x

        my_graph_3_3([sp2.const("x")])

        @sp2.graph
        def my_graph_4_1(x: List[ts[str]], y: int) -> Outputs(OutputBasket(List[ts[str]], shape="y")):
            return x

        my_graph_4_1([sp2.const("x")], 1)

        @sp2.graph
        def my_graph_4_2(x: List[ts[str]]) -> Outputs(OutputBasket(List[ts[str]], shape_of="x")):
            return x

        my_graph_4_2([sp2.const("x")])

        @sp2.graph
        def my_graph_4_3(x: ts[int]) -> Outputs(OutputBasket(Dict[str, ts[str]], shape=["a", "b", "c"])):
            return {k: sp2.const(k) for k in "abc"}

        my_graph_4_3(sp2.const(1))

        @sp2.graph
        def my_graph_4_4(x: ts[int]) -> Outputs(OutputBasket(List[ts[int]], shape=10)):
            return [sp2.const(1)] * 10

        my_graph_4_4(sp2.const(1))

        @sp2.node()
        def _dyn_basket() -> {ts[str]: ts[str]}:
            return {}

        @sp2.graph
        def my_graph_5_1(x: ts[int]) -> {ts[str]: ts[str]}:
            return _dyn_basket()

        my_graph_5_1(sp2.const(1))

        @sp2.graph
        def my_graph_5_2(x: ts[int]) -> OutputBasket({ts[str]: ts[str]}):
            return _dyn_basket()

        my_graph_5_2(sp2.const(1))

        # tests bug found with shape arguments + scalar inputs
        @sp2.graph
        def my_graph_5_3(x: str) -> OutputBasket({str: ts[str]}, shape=["x", "y"]):
            return {"x": sp2.const("a"), "y": sp2.const(x)}

        st = datetime(2020, 1, 1)
        res1 = sp2.run(my_graph_5_3, "b", starttime=st, endtime=timedelta())
        exp_out = {"x": [(st, "a")], "y": [(st, "b")]}
        self.assertEqual(res1, exp_out)

        # tests bug found with multiple dictionary baskets getting bound to same shape
        @sp2.graph
        def g() -> (
            sp2.Outputs(
                i=sp2.OutputBasket(Dict[str, sp2.ts[int]], shape=["V1"]),
                s=sp2.OutputBasket(Dict[str, sp2.ts[str]], shape=["V2"]),
            )
        ):
            i_v1 = sp2.curve(int, [(timedelta(hours=10), 1), (timedelta(hours=30), 1)])
            s_v2 = sp2.curve(str, [(timedelta(hours=30), "val1")])
            __return__(i={"V1": i_v1}, s={"V2": s_v2})

        sp2.run(g, starttime=datetime(2020, 1, 1), endtime=timedelta())

    def test_pythonic_node_syntax(self):
        # Proper parse errors
        node_specific = [
            ("state", sp2.state),
            ("alarms", sp2.alarms),
            ("start", sp2.start),
            ("stop", sp2.stop),
            ("__state__", sp2.__state__),
            ("__alarms__", sp2.__alarms__),
            ("__start__", sp2.__start__),
            ("__stop__", sp2.__stop__),
        ]
        for fn, func in node_specific:
            with self.assertRaisesRegex(RuntimeError, f"Unexpected use of {fn}, possibly using outside of @node?"):
                func()
            with self.assertRaisesRegex(RuntimeError, f"Unexpected use of {fn}, possibly using outside of @node?"):

                @sp2.graph
                def g():
                    func()

                sp2.run(g, starttime=datetime(2020, 1, 1), endtime=timedelta())

        node_or_graph = [("__return__", __return__), ("__outputs__", __outputs__), ("sp2.output", sp2.output)]
        for fn, func in node_or_graph:
            with self.assertRaisesRegex(
                RuntimeError, f"Unexpected use of {fn}, possibly using outside of @graph and @node?"
            ):
                func()

        with self.assertRaisesRegex(Sp2ParseError, "sp2.state must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.state:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.alarms must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.alarms:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.start must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.start:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "sp2.stop must be called, cannot use as a bare name"):

            @sp2.node
            def foo():
                with sp2.stop:
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "state must be used in a with statement"):

            @sp2.node
            def foo():
                sp2.state()

        with self.assertRaisesRegex(Sp2ParseError, "alarms must be used in a with statement"):

            @sp2.node
            def foo():
                sp2.alarms()

        with self.assertRaisesRegex(Sp2ParseError, "start must be used in a with statement"):

            @sp2.node
            def foo():
                sp2.start()

        with self.assertRaisesRegex(Sp2ParseError, "stop must be used in a with statement"):

            @sp2.node
            def foo():
                sp2.stop()

        with self.assertRaisesRegex(Sp2ParseError, "alarms must be declared before state"):

            @sp2.node
            def foo():
                with sp2.state():
                    pass
                with sp2.alarms():
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "state must be declared before start"):

            @sp2.node
            def foo():
                with sp2.start():
                    pass
                with sp2.state():
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "start must be declared before stop"):

            @sp2.node
            def foo():
                with sp2.stop():
                    pass
                with sp2.start():
                    pass

        with self.assertRaisesRegex(Sp2ParseError, "Invalid usage of stop, .*"):

            @sp2.node
            def foo() -> Outputs(x=ts[int]):
                __return__(x=1)
                with sp2.stop():
                    pass

        # Verify state works properly
        @sp2.node
        def lagger(x: ts[int]) -> ts[int]:
            with sp2.state():
                s_x = 0

            past = s_x
            s_x = x
            return past

        @sp2.node
        def history(x: ts[int]) -> ts[dict]:
            with sp2.state():
                s_i = 0
                s_x = {}

            s_x[s_i] = x
            s_i += 1
            return s_x.copy()

        st = datetime(2020, 1, 1)

        @sp2.graph
        def g():
            x = sp2.curve(typ=int, data=[(st + timedelta(i), i + 1) for i in range(3)])
            lag = lagger(x)
            hist = history(x)
            sp2.add_graph_output("lag", lag)
            sp2.add_graph_output("hist", hist)

        res = sp2.run(g, starttime=st, endtime=timedelta(4))

        exp_lag = [(st + timedelta(i), i) for i in range(3)]
        exp_hist = [(st, {0: 1}), (st + timedelta(1), {0: 1, 1: 2}), (st + timedelta(2), {0: 1, 1: 2, 2: 3})]
        self.assertEqual(exp_lag, res["lag"])
        self.assertEqual(exp_hist, res["hist"])

        # Verify alarms, start, stop

        class MyClass:
            self.x = 0

        @sp2.node
        def n1(my_class: MyClass) -> ts[int]:
            with sp2.alarms():
                alarm: ts[bool] = sp2.alarm(bool)

            with sp2.start():
                sp2.schedule_alarm(alarm, timedelta(1), True)

            with sp2.stop():
                my_class.x = 1

            if sp2.ticked(alarm):
                return 1

        @sp2.node
        def n2(x: ts[int]) -> ts[int]:
            with sp2.alarms():
                alarm: ts[int] = sp2.alarm(int)

            if sp2.ticked(x):
                sp2.schedule_alarm(alarm, timedelta(1), 1)

            if sp2.ticked(alarm):
                return alarm

        my_class = MyClass()

        @sp2.graph
        def g():
            x = n1(my_class)
            y = n2(x)
            sp2.add_graph_output("x", x)
            sp2.add_graph_output("y", y)

        res = sp2.run(g, starttime=st, endtime=timedelta(4))

        exp_x = [(st + timedelta(1), 1)]
        exp_y = [(st + timedelta(2), 1)]
        self.assertEqual(exp_x, res["x"])
        self.assertEqual(exp_y, res["y"])
        self.assertEqual(my_class.x, 1)

        # Make sure function call dunders are accounted for
        @sp2.node
        def n1():
            sp2.__state__(x=5)

        @sp2.node
        def n2():
            with sp2.__state__(x=5):
                pass

    def test_state_context_logic(self):
        # Enforce that no logic other than variable assignments/inits can be within a state context

        with self.assertWarnsRegex(
            DeprecationWarning,
            "Only variable assignments and declarations should be present in a sp2.state block. Any logic should be moved to sp2.start",
        ):

            @sp2.node
            def n1():
                with sp2.state():
                    i = 0
                    for x in range(10):
                        i += x
                    s_y = x

        with self.assertWarnsRegex(
            DeprecationWarning,
            "Only variable assignments and declarations should be present in a sp2.state block. Any logic should be moved to sp2.start",
        ):

            @sp2.node
            def n2():
                with sp2.state():
                    i = 0
                    if i > 0:
                        s_y = i

        with self.assertWarnsRegex(
            DeprecationWarning,
            "Only variable assignments and declarations should be present in a sp2.state block. Any logic should be moved to sp2.start",
        ):

            @sp2.node
            def n3():
                with sp2.state():
                    i = 10
                    while i > 0:
                        i -= 1
                    s_y = i

        # This is fine, though - just assignments
        @sp2.node
        def n4():
            with sp2.state():
                x = 2
                y = x
                z = x**2

        # This is also fine - annotated assignments
        class A:
            pass

        @sp2.node
        def n4():
            with sp2.state():
                x: int = 2
                y: set[bool] = {True, False}
                z: A = A()

    def test_pythonic_alarm_syntax(self):
        st = datetime(2020, 1, 1)

        # test new alarm syntax
        class ClassA:
            def __init__(self):
                self.my_member = 1

        class StructA(sp2.Struct):
            a: int
            b: str

        class StructB(sp2.Struct):
            c: int
            d: StructA

        @sp2.node
        def n5() -> ts[int]:
            with sp2.alarms():
                a = sp2.alarm(int)
                b = sp2.alarm(StructA)
                c = sp2.alarm(StructB)
                d = sp2.alarm(ClassA)

            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)
                sp2.schedule_alarm(b, timedelta(seconds=2), StructA())
                sp2.schedule_alarm(c, timedelta(seconds=3), StructB())
                sp2.schedule_alarm(d, timedelta(seconds=4), ClassA())

            if sp2.ticked(a):
                return 1
            if sp2.ticked(b):
                return 2
            if sp2.ticked(c):
                return 3
            if sp2.ticked(d):
                return 4

        @sp2.node
        def n6() -> ts[int]:
            with sp2.alarms():
                a: ts[int] = sp2.alarm(int)
                b: ts[StructA] = sp2.alarm(StructA)
                c: ts[StructB] = sp2.alarm(StructB)
                d: ts[ClassA] = sp2.alarm(ClassA)

            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)
                sp2.schedule_alarm(b, timedelta(seconds=2), StructA())
                sp2.schedule_alarm(c, timedelta(seconds=3), StructB())
                sp2.schedule_alarm(d, timedelta(seconds=4), ClassA())

            if sp2.ticked(a):
                return 1
            if sp2.ticked(b):
                return 2
            if sp2.ticked(c):
                return 3
            if sp2.ticked(d):
                return 4

        @sp2.graph
        def g1():
            sp2.add_graph_output("x", n5())
            sp2.add_graph_output("y", n6())

        res = sp2.run(g1, starttime=st, endtime=timedelta(10))
        exp_out = [(st + timedelta(seconds=(i + 1)), i + 1) for i in range(4)]
        self.assertEqual(res["x"], exp_out)
        self.assertEqual(res["y"], exp_out)

        # Now verify a ton of error messages
        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def n():
                with sp2.alarms():
                    a: ts[int]

        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def n():
                with sp2.alarms():
                    a: ts[int] = sp2.foo()

        with self.assertRaisesRegex(TypeError, "function `sp2.alarm` does not take keyword arguments"):

            @sp2.node
            def n():
                with sp2.alarms():
                    a: ts[int] = sp2.alarm(typ=int)

        with self.assertRaisesRegex(
            TypeError, "function `sp2.alarm` requires a single type argument: 0 arguments given"
        ):

            @sp2.node
            def n():
                with sp2.alarms():
                    a: ts[int] = sp2.alarm()

        with self.assertRaisesRegex(
            TypeError, "function `sp2.alarm` requires a single type argument: 2 arguments given"
        ):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm(int, bool)

        foo = lambda: int

        @sp2.node
        def n():
            with sp2.alarms():
                a = sp2.alarm(foo())

        with self.assertRaisesRegex(
            TypeError, "function `sp2.alarm` requires a single type argument: 2 arguments given"
        ):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm(int, bool)

        # we don't check type annotations
        @sp2.node
        def n():
            with sp2.alarms():
                a: ts[StructA] = sp2.alarm(StructB)

        with self.assertRaisesRegex(Sp2ParseError, "Alarms must be initialized with sp2.alarm in __alarms__ block"):

            @sp2.node
            def n():
                with sp2.alarms():
                    x = 5

        with self.assertRaisesRegex(Sp2ParseError, "Only alarm assignments are allowed in sp2.alarms block"):

            @sp2.node
            def n():
                with sp2.alarms():
                    print()

        with self.assertRaisesRegex(Sp2ParseError, "Exactly one alarm can be assigned per line"):

            @sp2.node
            def n():
                with sp2.alarms():
                    a, b = sp2.alarm(int), sp2.alarm(bool)

        # test generic alarms
        @sp2.node
        def n_gen(x: ts["T"]) -> ts["T"]:
            with sp2.alarms():
                a = sp2.alarm("T")
                b: ts["T"] = sp2.alarm("T")

            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)
                sp2.schedule_alarm(b, timedelta(seconds=2), 2)

            if sp2.ticked(a):
                return a

            if sp2.ticked(b):
                return b

            if sp2.ticked(x):
                return x

        @sp2.graph
        def g_gen():
            sp2.add_graph_output("z", n_gen(sp2.const(0)))

        res = sp2.run(g_gen, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(res["z"], [(st + timedelta(seconds=i), i) for i in range(3)])

        # test container alarms
        @sp2.node
        def n_cont() -> ts[bool]:
            with sp2.alarms():
                a: ts[[bool]] = sp2.alarm([bool])
                b: ts[[[int]]] = sp2.alarm([[int]])
                c: ts[{str: int}] = sp2.alarm({str: int})
                d: ts[{str: [int]}] = sp2.alarm({str: [int]})  # dict of lists
                e: ts[[{str: bool}]] = sp2.alarm([{str: bool}])  # list of dicts

            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), [True])
                sp2.schedule_alarm(b, timedelta(seconds=2), [[1]])
                sp2.schedule_alarm(c, timedelta(seconds=3), {"a": 1})
                sp2.schedule_alarm(d, timedelta(seconds=4), {"a": [1]})
                sp2.schedule_alarm(e, timedelta(seconds=5), [{"a": True}])

            return True

        @sp2.graph
        def g_cont():
            sp2.add_graph_output("u", n_cont())

        res = sp2.run(g_cont, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(res["u"], [(st + timedelta(seconds=i + 1), True) for i in range(5)])

        with self.assertRaises(TypeError):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm([bool, int])

        with self.assertRaises(TypeError):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm([bool, [bool]])

        with self.assertRaises(TypeError):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm([])

        with self.assertRaises(TypeError):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm({})

        with self.assertRaises(TypeError):

            @sp2.node
            def n():
                with sp2.alarms():
                    a = sp2.alarm({str: int, StructA: bool})

    def test_return(self):
        # basic test
        @sp2.node
        def n(x: ts[bool]) -> sp2.Outputs(x=ts[int], y=ts[int]):
            return sp2.output(x=1, y=2)

        @sp2.graph
        def g() -> sp2.Outputs(a=ts[int], b=ts[int]):
            node_out = n(sp2.timer(timedelta(seconds=1), True))
            return sp2.output(a=node_out.x, b=node_out.y)

        st = datetime(2020, 1, 1)
        res = sp2.run(g, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(res["a"], [(st + timedelta(seconds=i + 1), 1) for i in range(10)])
        self.assertEqual(res["b"], [(st + timedelta(seconds=i + 1), 2) for i in range(10)])

        # test different tstypes
        @sp2.node
        def n1(a: ts[int], b: ts[str]) -> sp2.Outputs(x=ts[int], y=ts[str]):
            return sp2.output(x=a, y=b)

        @sp2.graph
        def g1() -> sp2.Outputs(a=ts[int], b=ts[str]):
            int_data = sp2.timer(timedelta(seconds=1), 1)
            str_data = sp2.timer(timedelta(seconds=1), "a")
            node_out = n1(int_data, str_data)
            return sp2.output(a=node_out.x, b=node_out.y)

        res = sp2.run(g1, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(res["a"], [(st + timedelta(seconds=i + 1), 1) for i in range(10)])
        self.assertEqual(res["b"], [(st + timedelta(seconds=i + 1), "a") for i in range(10)])

        # test graph baskets: lists
        # unnamed single
        @sp2.graph
        def g2() -> sp2.OutputBasket(List[ts[int]], shape=3):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            return [x1, x2, x3]

        @sp2.graph
        def g3() -> sp2.OutputBasket(List[ts[int]], shape=3):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            return sp2.output([x1, x2, x3])

        r2 = sp2.run(g2, starttime=st, endtime=timedelta(seconds=10))
        r3 = sp2.run(g3, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r2, r3)

        # named single
        @sp2.graph
        def g4() -> sp2.Outputs(l=sp2.OutputBasket(List[ts[int]], shape=3)):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            return sp2.output(l=[x1, x2, x3])

        r4 = sp2.run(g4, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r2[0], r4["l[0]"])
        self.assertEqual(r2[1], r4["l[1]"])
        self.assertEqual(r2[2], r4["l[2]"])

        # named multiple
        @sp2.graph
        def g5() -> sp2.Outputs(l=sp2.OutputBasket(List[ts[int]], shape=2), m=sp2.OutputBasket(List[ts[int]], shape=2)):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            x4 = sp2.timer(timedelta(seconds=1), 4)
            __return__(l=[x1, x2], m=[x3, x4])

        @sp2.graph
        def g6() -> sp2.Outputs(l=sp2.OutputBasket(List[ts[int]], shape=2), m=sp2.OutputBasket(List[ts[int]], shape=2)):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            x4 = sp2.timer(timedelta(seconds=1), 4)
            return sp2.output(l=[x1, x2], m=[x3, x4])

        r5 = sp2.run(g5, starttime=st, endtime=timedelta(seconds=10))
        r6 = sp2.run(g6, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r5, r6)

        # test graph baskets: dictionaries
        # unnamed single
        @sp2.graph
        def g7() -> sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"]):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            return {"v1": x1, "v2": x2}

        @sp2.graph
        def g8() -> sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"]):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            return sp2.output({"v1": x1, "v2": x2})

        r7 = sp2.run(g7, starttime=st, endtime=timedelta(seconds=10))
        r8 = sp2.run(g8, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r7, r8)

        # named single
        @sp2.graph
        def g9() -> sp2.Outputs(d=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"])):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            __return__(d={"v1": x1, "v2": x2})

        @sp2.graph
        def g10() -> sp2.Outputs(d=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"])):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            return sp2.output(d={"v1": x1, "v2": x2})

        r9 = sp2.run(g9, starttime=st, endtime=timedelta(seconds=10))
        r10 = sp2.run(g10, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r9, r10)

        # named multiple
        @sp2.graph
        def g11() -> (
            sp2.Outputs(
                d1=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"]),
                d2=sp2.OutputBasket(Dict[str, ts[int]], shape=["v3", "v4"]),
            )
        ):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            x4 = sp2.timer(timedelta(seconds=1), 4)
            __return__(d1={"v1": x1, "v2": x2}, d2={"v3": x3, "v4": x4})

        @sp2.graph
        def g12() -> (
            sp2.Outputs(
                d1=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"]),
                d2=sp2.OutputBasket(Dict[str, ts[int]], shape=["v3", "v4"]),
            )
        ):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x2 = sp2.timer(timedelta(seconds=1), 2)
            x3 = sp2.timer(timedelta(seconds=1), 3)
            x4 = sp2.timer(timedelta(seconds=1), 4)
            return sp2.output(d1={"v1": x1, "v2": x2}, d2={"v3": x3, "v4": x4})

        r11 = sp2.run(g11, starttime=st, endtime=timedelta(seconds=10))
        r12 = sp2.run(g12, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r11, r12)

        # smorgasbord
        @sp2.node
        def n2(x: ts["T"]) -> sp2.Outputs(
            l=sp2.OutputBasket(List[ts[int]], shape=2), d=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"])
        ):
            sp2.output(l[0], 1)
            sp2.output(l[1], 2)
            sp2.output(d["v1"], 3)
            sp2.output(d["v2"], 4)

        @sp2.graph
        def g13() -> (
            sp2.Outputs(
                l=sp2.OutputBasket(List[ts[int]], shape=2),
                d=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"]),
                s=ts[str],
            )
        ):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x = n2(x1)
            __return__(l=x.l, d=x.d, s=sp2.timer(timedelta(seconds=1), "a"))

        @sp2.graph
        def g14() -> (
            sp2.Outputs(
                l=sp2.OutputBasket(List[ts[int]], shape=2),
                d=sp2.OutputBasket(Dict[str, ts[int]], shape=["v1", "v2"]),
                s=ts[str],
            )
        ):
            x1 = sp2.timer(timedelta(seconds=1), 1)
            x = n2(x1)
            return sp2.output(l=x.l, d=x.d, s=sp2.timer(timedelta(seconds=1), "a"))

        r13 = sp2.run(g13, starttime=st, endtime=timedelta(seconds=10))
        r14 = sp2.run(g14, starttime=st, endtime=timedelta(seconds=10))
        self.assertEqual(r13, r14)

        # empty return statements
        @sp2.node
        def n():
            return

        @sp2.graph
        def g():
            return

        @sp2.node
        def n(x: ts[int]) -> ts[int]:
            if x > 0:
                return
            return 1

        @sp2.node
        def n(z: ts[int]) -> sp2.Outputs(x=ts[int], y=ts[str]):
            if z > 0:
                return
            return sp2.output(x=1, y=2)

        with self.assertRaisesRegex(Sp2ParseError, "return does not return values with non empty outputs"):

            @sp2.graph
            def g() -> ts[int]:
                return

        # verify error messages
        with self.assertRaisesRegex(Sp2ParseError, "return does not return values with non empty outputs"):

            @sp2.graph
            def g() -> sp2.Outputs(x=ts[int], y=ts[str]):
                return

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def n() -> sp2.Outputs(x=ts[int], y=ts[str]):
                return 1, "a"

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def n() -> sp2.Outputs(x=ts[int], y=ts[str]):
                return (1, "a")

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def n() -> sp2.Outputs(x=ts[int], y=ts[str]):
                return sp2.output()

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def n() -> sp2.Outputs(x=ts[int], y=ts[str]):
                return sp2.outputs(x=1, y="a")  # note the s

        with self.assertRaisesRegex(
            Sp2ParseError,
            "Returning multiple outputs must use the following syntax: return sp2.output\\(out1=val1, \\.\\.\\.\\)",
        ):

            @sp2.node
            def n() -> sp2.Outputs(x=ts[int], y=ts[str]):
                return output(x=1, y="a")

        # test running a node directly
        @sp2.node
        def n() -> sp2.Outputs(x=sp2.ts[int]):
            with sp2.alarms():
                a = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(), 0)
            return sp2.output(x=a)

        sp2.run(n, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=1))

        # test sp2 node builtins within the output statement
        @sp2.node
        def n() -> sp2.Outputs(ts[datetime]):
            with sp2.alarms():
                a = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)

            if sp2.ticked(a):
                return sp2.now()

        r15 = sp2.run(n, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=1))

        @sp2.node
        def n() -> sp2.Outputs(ts[datetime]):
            with sp2.alarms():
                a = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)

            if sp2.ticked(a):
                return sp2.output(sp2.now())

        r16 = sp2.run(n, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=1))
        self.assertEqual(r15, r16)

        @sp2.node
        def n() -> sp2.Outputs(c=ts[datetime]):
            with sp2.alarms():
                a = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)

            if sp2.ticked(a):
                return sp2.output(c=sp2.now())

        sp2.run(n, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=1))

        @sp2.node
        def n() -> sp2.Outputs(c=ts[datetime], d=ts[datetime]):
            with sp2.alarms():
                a = sp2.alarm(int)
            with sp2.start():
                sp2.schedule_alarm(a, timedelta(seconds=1), 1)

            if sp2.ticked(a):
                return sp2.output(c=sp2.now(), d=sp2.now())

        sp2.run(n, starttime=datetime(2020, 1, 1), endtime=timedelta(seconds=1))

    def test_pythonic_depr_warning(self):
        original_setting = sp2.impl.warnings.set_deprecation_warning(True)

        # alarm
        with self.assertWarnsRegex(DeprecationWarning, "Calling __alarms__ is deprecated: *"):

            @sp2.node
            def n():
                __alarms__(a=ts[bool])
                pass

        @sp2.node
        def n():
            with sp2.alarms():
                a = sp2.alarm(bool)
            pass

        # state
        with self.assertWarnsRegex(DeprecationWarning, "Calling __state__ is deprecated: *"):

            @sp2.node
            def n():
                __state__(a=int)
                pass

        @sp2.node
        def n():
            with sp2.state():
                a = 1
            pass

        # start
        with self.assertWarnsRegex(DeprecationWarning, "Calling __start__ is deprecated: *"):

            @sp2.node
            def n():
                with __start__():
                    pass
                pass

        @sp2.node
        def n():
            with sp2.start():
                pass
            pass

        # stop
        with self.assertWarnsRegex(DeprecationWarning, "Calling __stop__ is deprecated: *"):

            @sp2.node
            def n():
                with __stop__():
                    pass
                pass

        @sp2.node
        def n():
            with sp2.stop():
                pass
            pass

        # outputs
        with self.assertWarnsRegex(DeprecationWarning, "Declaring __outputs__ is deprecated; *"):

            @sp2.node
            def n():
                __outputs__(ts[int])
                return 1

        with self.assertWarnsRegex(DeprecationWarning, "Declaring __outputs__ is deprecated; *"):

            @sp2.graph
            def g():
                __outputs__(a=ts[int], b=ts[str])
                pass

        @sp2.node
        def n() -> ts[int]:
            return 1

        # return
        with self.assertWarnsRegex(DeprecationWarning, "Calling __return__ is deprecated*"):

            @sp2.node
            def n() -> sp2.Outputs(x=ts[int]):
                __return__(x=1)

        with self.assertWarnsRegex(DeprecationWarning, "Calling __return__ is deprecated*"):

            @sp2.graph
            def g() -> sp2.Outputs(x=ts[int], y=ts[int]):
                __return__(x=1, y=2)

        @sp2.node
        def n() -> ts[int]:
            return sp2.output(1)

        # catch variable declarations within a state/alarm call
        with self.assertWarnsRegex(DeprecationWarning, "Variable declarations within alarms\\(\\) are deprecated*"):

            @sp2.node
            def n():
                with sp2.alarms(a=ts[bool]):
                    pass

        with self.assertWarnsRegex(DeprecationWarning, "Variable declarations within state\\(\\) are deprecated*"):

            @sp2.node
            def n():
                with sp2.state(s=0):
                    pass

        # reset the opt-in settings now that the test is done
        sp2.impl.warnings.set_deprecation_warning(original_setting)


if __name__ == "__main__":
    unittest.main()
