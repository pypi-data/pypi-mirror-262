import typing
import unittest
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List

import sp2
from sp2 import ts
from sp2.impl.wiring.runtime import build_graph
from sp2.tests.utils.typed_curve_generator import TypedCurveGenerator


class Trade(sp2.Struct):
    price: float
    size: int
    account: str
    symbol: str


class BasketType(Enum):
    ListBasket = auto()
    DictBasket = auto()


class TestBasketOutputs(unittest.TestCase):
    accounts = ["TEST1", "TEST2", "ALL"]
    st = datetime(2020, 1, 1)
    trade_list = [
        (st + timedelta(seconds=1), Trade(price=100.0, size=50, account="TEST1", symbol="AAPL")),
        (st + timedelta(seconds=2), Trade(price=101.5, size=500, account="TEST1", symbol="AAPL")),
        (st + timedelta(seconds=3), Trade(price=100.50, size=100, account="TEST1", symbol="AAPL")),
        (st + timedelta(seconds=4), Trade(price=101.2, size=500, account="TEST2", symbol="IBM")),
        (st + timedelta(seconds=5), Trade(price=101.3, size=500, account="TEST2", symbol="IBM")),
        (st + timedelta(seconds=6), Trade(price=101.4, size=500, account="TEST2", symbol="IBM")),
    ]
    debug_print = False

    def basket_test(self, node, basket_type, named_output):
        def test():
            trades = sp2.curve(Trade, self.trade_list)

            if named_output:
                demuxed = node(trades, self.accounts).x
            else:
                demuxed = node(trades, self.accounts)

            if basket_type == BasketType.DictBasket:
                demuxed_test1 = demuxed["TEST1"]
                demuxed_test2 = demuxed["TEST2"]
                demuxed_all = demuxed["ALL"]

            else:
                assert basket_type == BasketType.ListBasket
                demuxed_test1 = demuxed[0]
                demuxed_test2 = demuxed[1]
                demuxed_all = demuxed[2]

            sp2.add_graph_output("demuxed_test1", demuxed_test1)
            sp2.add_graph_output("demuxed_test2", demuxed_test2)
            sp2.add_graph_output("demuxed_all", demuxed_all)

        graph = build_graph(test)
        result = sp2.run(test, starttime=self.st)

        assert result["demuxed_test1"] == [trade for trade in self.trade_list if trade[1].account == "TEST1"]
        assert result["demuxed_test2"] == [trade for trade in self.trade_list if trade[1].account == "TEST2"]
        assert result["demuxed_all"] == self.trade_list

    def non_basket_test(self, node, named_output):
        def test():
            trades = sp2.curve(Trade, self.trade_list)
            if named_output:
                repeated = node(trades).x
            else:
                repeated = node(trades)
            sp2.add_graph_output("repeated", repeated)

        graph = build_graph(test)
        result = sp2.run(test, starttime=self.st)
        assert result["repeated"] == self.trade_list

    def test_nodes_with_dict_syntax(self):
        # output to multiple keys: sp2.output(x = {k1:v1,k2:v2})
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts")
        ):
            if sp2.ticked(trade):
                sp2.output(x={trade.account: trade, "ALL": trade})

        self.basket_test(node=demux, basket_type=BasketType.DictBasket, named_output=True)

        # list version
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(List[ts[Trade]], shape_of="accounts")
        ):
            if sp2.ticked(trade):
                sp2.output(x={self.accounts.index(trade.account): trade, self.accounts.index("ALL"): trade})

        self.basket_test(node=demux, basket_type=BasketType.ListBasket, named_output=True)

        # unnamed output version
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts"):
            if sp2.ticked(trade):
                sp2.output({trade.account: trade, "ALL": trade})

        self.basket_test(node=demux, basket_type=BasketType.DictBasket, named_output=False)

        # output to multiple keys using PyBasketOutputProxy to handle the dict
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts")
        ):
            if sp2.ticked(trade):
                my_data = {trade.account: trade, "ALL": trade}
                sp2.output(x=my_data)

        self.basket_test(node=demux, basket_type=BasketType.DictBasket, named_output=True)

        # list version
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts")
        ):
            if sp2.ticked(trade):
                my_data = {self.accounts.index(trade.account): trade, self.accounts.index("ALL"): trade}
                sp2.output(x=my_data)

        # unnamed output version
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts")
        ):
            if sp2.ticked(trade):
                my_data = {trade.account: trade, "ALL": trade}
                sp2.output(my_data)

        self.basket_test(node=demux, basket_type=BasketType.DictBasket, named_output=False)

    def test_nodes_without_dict_syntax(self):
        # output to multiple keys: sp2.output(x[k1],v1); sp2.output(x[k2],v2)
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts")
        ):
            if sp2.ticked(trade):
                sp2.output(x[trade.account], trade)
                sp2.output(x["ALL"], trade)

        self.basket_test(node=demux, basket_type=BasketType.DictBasket, named_output=True)

        # list version
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(List[ts[Trade]], shape_of="accounts")
        ):
            if sp2.ticked(trade):
                sp2.output(x[self.accounts.index(trade.account)], trade)
                sp2.output(x[self.accounts.index("ALL")], trade)

        self.basket_test(node=demux, basket_type=BasketType.ListBasket, named_output=True)

    def test_output_syntax_with_non_basket_outputs(self):
        # basic unnamed output
        @sp2.node(debug_print=self.debug_print)
        def repeater(trade: ts[Trade]) -> ts[Trade]:
            if sp2.ticked(trade):
                sp2.output(trade)

        self.non_basket_test(node=repeater, named_output=False)

        # basic named output
        @sp2.node(debug_print=self.debug_print)
        def repeater(trade: ts[Trade]) -> sp2.Outputs(x=ts[Trade]):
            if sp2.ticked(trade):
                sp2.output(x, trade)

        self.non_basket_test(node=repeater, named_output=True)

        # basic named output, assignment syntax
        @sp2.node(debug_print=self.debug_print)
        def repeater(trade: ts[Trade]) -> sp2.Outputs(x=ts[Trade]):
            if sp2.ticked(trade):
                sp2.output(x=trade)

        self.non_basket_test(node=repeater, named_output=True)

    def test_typing_interface(self):
        # output to multiple keys: sp2.output(x = {k1:v1,k2:v2})
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(Dict[str, ts[Trade]], shape="accounts")
        ):
            if sp2.ticked(trade):
                sp2.output(x={trade.account: trade, "ALL": trade})

        self.basket_test(node=demux, basket_type=BasketType.DictBasket, named_output=True)

        # list version
        @sp2.node(debug_print=self.debug_print)
        def demux(trade: ts[Trade], accounts: [str]) -> sp2.Outputs(
            x=sp2.OutputBasket(List[ts[Trade]], shape_of="accounts")
        ):
            if sp2.ticked(trade):
                sp2.output(x={self.accounts.index(trade.account): trade, self.accounts.index("ALL"): trade})

        self.basket_test(node=demux, basket_type=BasketType.ListBasket, named_output=True)

    def test_main_graph_unnamed_basket_outputs(self):
        @sp2.graph
        def main_list_basket() -> sp2.OutputBasket(List[sp2.ts[int]]):
            curve_generator = TypedCurveGenerator()
            return [
                curve_generator.gen_int_curve(0, 10, 1, skip_indices=[5]),
                curve_generator.gen_int_curve(100, 10, 1, skip_indices=[4]),
            ]

        @sp2.graph
        def main_dict_basket() -> sp2.OutputBasket(Dict[str, ts[int]]):
            curve_generator = TypedCurveGenerator()
            return {
                "k1": curve_generator.gen_int_curve(0, 10, 1, skip_indices=[5]),
                "k2": curve_generator.gen_int_curve(100, 10, 1, skip_indices=[4]),
            }

        starttime = datetime(2021, 1, 1)
        g = sp2.run(main_list_basket, starttime=starttime, endtime=timedelta(seconds=15))
        self.assertEqual([0, 1], list(g.keys()))
        g2 = sp2.run(main_dict_basket, starttime=starttime, endtime=timedelta(seconds=15))
        self.assertEqual(["k1", "k2"], list(g2.keys()))
        expected_items0 = [(starttime + timedelta(seconds=i), i) for i in range(11) if i != 5]
        expected_items1 = [(starttime + timedelta(seconds=i), 100 + i) for i in range(11) if i != 4]
        self.assertEqual(expected_items0, g[0])
        self.assertEqual(expected_items1, g[1])
        self.assertEqual(expected_items0, g2["k1"])
        self.assertEqual(expected_items1, g2["k2"])

    def test_main_graph_named_basket_outputs(self):
        @sp2.graph
        def main() -> sp2.Outputs(l=sp2.OutputBasket(List[sp2.ts[int]]), d=sp2.OutputBasket(Dict[str, sp2.ts[int]])):
            curve_generator = TypedCurveGenerator()
            l = [
                curve_generator.gen_int_curve(0, 10, 1, skip_indices=[5]),
                curve_generator.gen_int_curve(100, 10, 1, skip_indices=[4]),
            ]
            d = {
                "k1": curve_generator.gen_int_curve(0, 10, 1, skip_indices=[5]),
                "k2": curve_generator.gen_int_curve(100, 10, 1, skip_indices=[4]),
            }
            return sp2.output(l=l, d=d)

        starttime = datetime(2021, 1, 1)
        g = sp2.run(main, starttime=starttime, endtime=timedelta(seconds=15))
        self.assertEqual(["l[0]", "l[1]", "d[k1]", "d[k2]"], list(g.keys()))
        expected_items0 = [(starttime + timedelta(seconds=i), i) for i in range(11) if i != 5]
        expected_items1 = [(starttime + timedelta(seconds=i), 100 + i) for i in range(11) if i != 4]
        self.assertEqual(expected_items0, g["l[0]"])
        self.assertEqual(expected_items0, g["d[k1]"])
        self.assertEqual(expected_items1, g["l[1]"])
        self.assertEqual(expected_items1, g["d[k2]"])


if __name__ == "__main__":
    unittest.main()
