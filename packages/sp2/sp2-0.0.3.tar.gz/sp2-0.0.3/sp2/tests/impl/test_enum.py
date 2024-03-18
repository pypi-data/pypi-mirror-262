import _pickle
import unittest
from datetime import datetime, timedelta

import sp2
from sp2 import ts


class MyEnum(sp2.Enum):
    A = 1
    B = 20
    C = 3


class MyEnum2(sp2.Enum):
    C = 10
    D = 20

    # Methods and properties allowed
    def f1(self):
        return self.value * 2

    @property
    def p1(self):
        return self.f1()

    @classmethod
    def c1(cls):
        return cls.C.value * 3

    @staticmethod
    def s1():
        return 123


MyDEnum = sp2.DynamicEnum("MyDEnum", ["A", "B", "C"])


class TestSp2Enum(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(MyEnum("A"), MyEnum.A)
        self.assertEqual(MyEnum(1), MyEnum.A)
        self.assertEqual(MyEnum("B"), MyEnum.B)
        self.assertEqual(MyEnum(20), MyEnum.B)
        self.assertNotEqual(MyEnum.A, MyEnum.B)
        self.assertNotEqual(MyEnum.A, 1)
        self.assertNotEqual(MyEnum.B, MyEnum2.D)

        self.assertEqual(MyEnum2.C.value, 10)
        self.assertEqual(MyEnum2.C.name, "C")

        self.assertEqual(list(MyEnum), [MyEnum.A, MyEnum.B, MyEnum.C])

        self.assertEqual(MyEnum2.C.f1(), 20)
        self.assertEqual(MyEnum2.D.p1, 40)
        self.assertEqual(MyEnum2.c1(), 30)
        self.assertEqual(MyEnum2.s1(), 123)

        with self.assertRaisesRegex(ValueError, "123 is not a valid value on sp2.enum type MyEnum"):
            MyEnum(123)

        with self.assertRaisesRegex(ValueError, "ABC is not a valid value on sp2.enum type MyEnum"):
            MyEnum("ABC")

        with self.assertRaisesRegex(TypeError, "sp2.Enum expected int enum value, got str for field B"):

            class FOO(sp2.Enum):
                A = 1
                B = "hey"

        # bracket access
        self.assertEqual(MyEnum["A"], MyEnum.A)

        # auto
        class MyEnum3(sp2.Enum):
            A = sp2.Enum.auto()
            B = 10
            C = sp2.Enum.auto()

        self.assertEqual(list(MyEnum3), [MyEnum3.A, MyEnum3.B, MyEnum3.C])
        self.assertEqual(MyEnum3.A.value, 0)
        self.assertEqual(MyEnum3.B.value, 10)
        self.assertEqual(MyEnum3.C.value, 11)

    def test_python_enum_compatibility(self):
        self.assertEqual(dict(MyEnum.__members__), dict(MyEnum.__metadata__))

    def test_node(self):
        """test ability of node to convert to/from enum types properly"""

        @sp2.node
        def enum_test_out(x: ts[int]) -> ts[MyEnum]:
            if sp2.ticked(x):
                return MyEnum(x)

        @sp2.node
        def enum_test_in(x: ts[MyEnum]) -> ts[int]:
            if sp2.ticked(x):
                return x.value

        @sp2.graph
        def graph():
            td = timedelta()
            x = sp2.curve(int, [(td, 3), (td, 20), (td, 1)], push_mode=sp2.PushMode.NON_COLLAPSING)

            eout = enum_test_out(x)
            ein = enum_test_in(eout)
            sp2.add_graph_output("eout", eout)
            sp2.add_graph_output("ein", ein)

        result = sp2.run(graph, starttime=datetime.utcnow())
        self.assertEqual([v[1] for v in result["eout"]], [MyEnum(3), MyEnum(20), MyEnum(1)])
        self.assertEqual([v[1] for v in result["ein"]], [3, 20, 1])

    def test_enum_type_check(self):
        class S(sp2.Struct):
            a: MyEnum

        with self.assertRaisesRegex(TypeError, "Invalid enum type, expected enum type MyEnum got MyEnum2"):
            S(a=MyEnum2.C)

    def test_dynamic_enum(self):
        DEnum = sp2.DynamicEnum("DEnum", ["A", "B", "C"])
        DEnum2 = sp2.DynamicEnum("DEnum", {"A": 5, "B": 6, "C": 20})

        self.assertEqual(list(DEnum), [DEnum.A, DEnum.B, DEnum.C])
        self.assertEqual(list(v.value for v in DEnum), [0, 1, 2])
        self.assertEqual(list(v.value for v in DEnum2), [5, 6, 20])

    def test_incref_crash(self):
        """original cut was missing incref"""
        for _ in range(5):
            _ = [MyEnum(1) for x in range(1000)]

    def test_pickle(self):
        x = _pickle.loads(_pickle.dumps(MyEnum.B))
        self.assertEqual(x, MyEnum.B)

        # Dynamic pickle
        x = _pickle.loads(_pickle.dumps(MyDEnum.C))
        self.assertEqual(x, MyDEnum.C)

    def test_subclassing(self):
        # subclassing an enum should raise an error similar to the standard Python enum.Enum
        class A(sp2.Enum):
            RED = 1

        with self.assertRaises(TypeError) as cm:

            class B(A):
                GREEN = 2

        self.assertEqual("Cannot extend sp2.Enum 'A': inheriting from an Enum is prohibited", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
