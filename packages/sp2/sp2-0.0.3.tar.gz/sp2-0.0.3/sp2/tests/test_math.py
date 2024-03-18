import math
import numpy as np
import unittest
from datetime import datetime, timedelta

import sp2


class TestMath(unittest.TestCase):
    def test_math_binary_ops(self):
        OPS = {
            sp2.add: lambda x, y: x + y,
            sp2.sub: lambda x, y: x - y,
            sp2.multiply: lambda x, y: x * y,
            sp2.divide: lambda x, y: x / y,
            sp2.pow: lambda x, y: x**y,
            sp2.min: lambda x, y: min(x, y),
            sp2.max: lambda x, y: max(x, y),
            sp2.floordiv: lambda x, y: x // y,
        }

        @sp2.graph
        def graph(use_promotion: bool):
            x = sp2.count(sp2.timer(timedelta(seconds=0.25)))
            if use_promotion:
                y = 10
                y_edge = sp2.const(y)
            else:
                y = sp2.default(sp2.count(sp2.timer(timedelta(seconds=1))), 1, delay=timedelta(seconds=0.25))
                y_edge = y

            sp2.add_graph_output("x", sp2.merge(x, sp2.sample(y_edge, x)))
            sp2.add_graph_output("y", sp2.merge(y_edge, sp2.sample(x, y_edge)))

            for op in OPS.keys():
                if use_promotion:
                    if op in [sp2.min, sp2.max]:
                        continue  # can't type promote, it's not being called ON an edge
                    p_op = OPS[op]
                    sp2.add_graph_output(op.__name__, p_op(x, y))
                    sp2.add_graph_output(op.__name__ + "-rev", p_op(y, x))
                else:
                    sp2.add_graph_output(op.__name__, op(x, y))
                    sp2.add_graph_output(op.__name__ + "-rev", op(y, x))

        for use_promotion in [False, True]:
            st = datetime(2020, 1, 1)
            results = sp2.run(graph, use_promotion, starttime=st, endtime=st + timedelta(seconds=3))
            xv = [v[1] for v in results["x"]]
            yv = [v[1] for v in results["y"]]

            for op, comp in OPS.items():
                if op in [sp2.min, sp2.max] and use_promotion:
                    continue
                self.assertEqual(
                    [v[1] for v in results[op.__name__]], [comp(x, y) for x, y in zip(xv, yv)], op.__name__
                )
                self.assertEqual(
                    [v[1] for v in results[op.__name__ + "-rev"]], [comp(y, x) for x, y in zip(xv, yv)], op.__name__
                )

    def test_math_binary_ops_numpy(self):
        OPS = {
            sp2.add: lambda x, y: x + y,
            sp2.sub: lambda x, y: x - y,
            sp2.multiply: lambda x, y: x * y,
            sp2.divide: lambda x, y: x / y,
            sp2.pow: lambda x, y: x**y,
            sp2.min: lambda x, y: np.minimum(x, y),
            sp2.max: lambda x, y: np.maximum(x, y),
            sp2.floordiv: lambda x, y: x // y,
        }

        @sp2.graph
        def graph(use_promotion: bool):
            x = sp2.count(sp2.timer(timedelta(seconds=0.25))) + sp2.const(np.random.rand(10))
            if use_promotion:
                y = 10
                y_edge = sp2.const(y)
            else:
                y = sp2.default(
                    sp2.count(sp2.timer(timedelta(seconds=1))), 1, delay=timedelta(seconds=0.25)
                ) * sp2.const(np.random.randint(1, 2, (10,)))
                y_edge = y

            sp2.add_graph_output("x", sp2.merge(x, sp2.sample(y_edge, x)))
            sp2.add_graph_output("y", sp2.merge(y_edge, sp2.sample(x, y_edge)))

            for op in OPS.keys():
                if use_promotion:
                    if op in [sp2.min, sp2.max]:
                        continue  # can't type promote, it's not being called ON an edge
                    p_op = OPS[op]
                    sp2.add_graph_output(op.__name__, p_op(x, y))
                    sp2.add_graph_output(op.__name__ + "-rev", p_op(y, x))
                else:
                    sp2.add_graph_output(op.__name__, op(x, y))
                    sp2.add_graph_output(op.__name__ + "-rev", op(y, x))

        for use_promotion in [False, True]:
            st = datetime(2020, 1, 1)
            results = sp2.run(graph, use_promotion, starttime=st, endtime=st + timedelta(seconds=3))
            xv = [v[1] for v in results["x"]]
            yv = [v[1] for v in results["y"]]

            for op, comp in OPS.items():
                if op in [sp2.min, sp2.max] and use_promotion:
                    continue
                for i, (_, result) in enumerate(results[op.__name__]):
                    reference = comp(xv[i], yv[i])
                    self.assertTrue((result == reference).all(), op.__name__)
                for i, (_, result) in enumerate(results[op.__name__ + "-rev"]):
                    reference = comp(yv[i], xv[i])
                    self.assertTrue((result == reference).all(), op.__name__)

    def test_math_unary_ops(self):
        OPS = {
            sp2.pos: lambda x: +x,
            sp2.neg: lambda x: -x,
            sp2.abs: lambda x: abs(x),
            sp2.ln: lambda x: math.log(x),
            sp2.log2: lambda x: math.log2(x),
            sp2.log10: lambda x: math.log10(x),
            sp2.exp: lambda x: math.exp(x),
            sp2.exp2: lambda x: 2**x,
            sp2.sin: lambda x: math.sin(x),
            sp2.cos: lambda x: math.cos(x),
            sp2.tan: lambda x: math.tan(x),
            sp2.arctan: lambda x: math.atan(x),
            sp2.sinh: lambda x: math.sinh(x),
            sp2.cosh: lambda x: math.cosh(x),
            sp2.tanh: lambda x: math.tanh(x),
            sp2.arcsinh: lambda x: math.asinh(x),
            sp2.arccosh: lambda x: math.acosh(x),
            sp2.erf: lambda x: math.erf(x),
        }

        @sp2.graph
        def graph():
            x = sp2.count(sp2.timer(timedelta(seconds=0.25)))
            sp2.add_graph_output("x", x)

            for op in OPS.keys():
                sp2.add_graph_output(op.__name__, op(x))

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st, endtime=st + timedelta(seconds=3))
        xv = [v[1] for v in results["x"]]

        for op, comp in OPS.items():
            self.assertEqual([v[1] for v in results[op.__name__]], [comp(x) for x in xv], op.__name__)

    def test_math_unary_ops_numpy(self):
        OPS = {
            sp2.abs: lambda x: np.abs(x),
            sp2.ln: lambda x: np.log(x),
            sp2.log2: lambda x: np.log2(x),
            sp2.log10: lambda x: np.log10(x),
            sp2.exp: lambda x: np.exp(x),
            sp2.exp2: lambda x: np.exp2(x),
            sp2.sin: lambda x: np.sin(x),
            sp2.cos: lambda x: np.cos(x),
            sp2.tan: lambda x: np.tan(x),
            sp2.arctan: lambda x: np.arctan(x),
            sp2.sinh: lambda x: np.sinh(x),
            sp2.cosh: lambda x: np.cosh(x),
            sp2.tanh: lambda x: np.tanh(x),
            sp2.arcsinh: lambda x: np.arcsinh(x),
            sp2.arccosh: lambda x: np.arccosh(x),
            # sp2.erf: lambda x: math.erf(x),
        }

        @sp2.graph
        def graph():
            x = sp2.count(sp2.timer(timedelta(seconds=0.25))) + sp2.const(np.random.rand(10))
            sp2.add_graph_output("x", x)

            for op in OPS.keys():
                sp2.add_graph_output(op.__name__, op(x))

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st, endtime=st + timedelta(seconds=3))
        xv = [v[1] for v in results["x"]]

        for op, comp in OPS.items():
            for i, (_, result) in enumerate(results[op.__name__]):
                reference = comp(xv[i])
                # drop nans
                result = result[~np.isnan(result)]
                reference = reference[~np.isnan(reference)]
                self.assertTrue((result == reference).all(), op.__name__)

    def test_math_unary_ops_other_domain(self):
        OPS = {
            sp2.arcsin: lambda x: math.asin(x),
            sp2.arccos: lambda x: math.acos(x),
            sp2.arctanh: lambda x: math.atanh(x),
        }

        @sp2.graph
        def graph():
            x = 1 / (sp2.count(sp2.timer(timedelta(seconds=0.25))) * math.pi)
            sp2.add_graph_output("x", x)

            for op in OPS.keys():
                sp2.add_graph_output(op.__name__, op(x))

        st = datetime(2020, 1, 1)
        results = sp2.run(graph, starttime=st, endtime=st + timedelta(seconds=3))
        xv = [v[1] for v in results["x"]]

        for op, comp in OPS.items():
            self.assertEqual([v[1] for v in results[op.__name__]], [comp(x) for x in xv], op.__name__)

    def test_comparisons(self):
        OPS = {
            sp2.gt: lambda x, y: x > y,
            sp2.ge: lambda x, y: x >= y,
            sp2.lt: lambda x, y: x < y,
            sp2.le: lambda x, y: x <= y,
            sp2.eq: lambda x, y: x == y,
            sp2.ne: lambda x, y: x != y,
        }

        @sp2.graph
        def graph(use_promotion: bool):
            x = sp2.count(sp2.timer(timedelta(seconds=0.25)))
            if use_promotion:
                y = 10
                y_edge = sp2.const(y)
            else:
                y = sp2.default(sp2.count(sp2.timer(timedelta(seconds=1))), 1, delay=timedelta(seconds=0.25))
                y_edge = y

            sp2.add_graph_output("x", sp2.merge(x, sp2.sample(y_edge, x)))
            sp2.add_graph_output("y", sp2.merge(y_edge, sp2.sample(x, y_edge)))

            for op in OPS.keys():
                if use_promotion:
                    p_op = OPS[op]
                    sp2.add_graph_output(op.__name__, p_op(x, y))
                    sp2.add_graph_output(op.__name__ + "-rev", p_op(y, x))
                else:
                    sp2.add_graph_output(op.__name__, op(x, y))
                    sp2.add_graph_output(op.__name__ + "-rev", op(y, x))

        for use_promotion in [False, True]:
            st = datetime(2020, 1, 1)
            results = sp2.run(graph, use_promotion, starttime=st, endtime=st + timedelta(seconds=10))
            xv = [v[1] for v in results["x"]]
            yv = [v[1] for v in results["y"]]

            for op, comp in OPS.items():
                self.assertEqual(
                    [v[1] for v in results[op.__name__]], [comp(x, y) for x, y in zip(xv, yv)], op.__name__
                )
                self.assertEqual(
                    [v[1] for v in results[op.__name__ + "-rev"]], [comp(y, x) for x, y in zip(xv, yv)], op.__name__
                )

    def test_boolean_ops(self):
        def graph():
            x = sp2.default(sp2.curve(bool, [(timedelta(seconds=s), s % 2 == 0) for s in range(1, 20)]), False)
            y = sp2.default(sp2.curve(bool, [(timedelta(seconds=s * 0.5), s % 2 == 0) for s in range(1, 40)]), False)
            z = sp2.default(sp2.curve(bool, [(timedelta(seconds=s * 2), s % 2 == 0) for s in range(1, 10)]), False)

            sp2.add_graph_output("rawx", x)
            sp2.add_graph_output("x", sp2.merge(x, sp2.merge(sp2.sample(y, x), sp2.sample(z, x))))
            sp2.add_graph_output("y", sp2.merge(y, sp2.merge(sp2.sample(x, y), sp2.sample(z, y))))
            sp2.add_graph_output("z", sp2.merge(z, sp2.merge(sp2.sample(x, z), sp2.sample(y, z))))

            sp2.add_graph_output("and_", sp2.and_(x, y, z))
            sp2.add_graph_output("or_", sp2.or_(x, y, z))
            sp2.add_graph_output("not_", sp2.not_(x))

        results = sp2.run(graph, starttime=datetime(2020, 5, 18))
        x = [v[1] for v in results["x"]]
        y = [v[1] for v in results["y"]]
        z = [v[1] for v in results["z"]]

        self.assertEqual([v[1] for v in results["and_"]], [all([a, b, c]) for a, b, c in zip(x, y, z)])
        self.assertEqual([v[1] for v in results["or_"]], [any([a, b, c]) for a, b, c in zip(x, y, z)])
        self.assertEqual([v[1] for v in results["not_"]], [not v[1] for v in results["rawx"]])
        pass


if __name__ == "__main__":
    unittest.main()
