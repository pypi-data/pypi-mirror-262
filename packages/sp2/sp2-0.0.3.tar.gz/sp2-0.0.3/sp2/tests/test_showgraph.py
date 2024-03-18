import pytest

import sp2
from sp2.showgraph import _build_graphviz_graph


def _cant_find_graphviz():
    try:
        from graphviz import Digraph

        Digraph().pipe()
    except BaseException:
        return True
    return False


@pytest.mark.skipif(_cant_find_graphviz(), reason="cannot find graphviz installation")
def test_showgraph_names():
    # Simple test to assert that node names
    # are properly propagated into graph viewer
    x = sp2.const(5)
    y = sp2.const(6)

    x.nodedef.__name__ = "x"
    y.nodedef.__name__ = "y"

    @sp2.graph
    def graph():
        sp2.print("x", x)
        sp2.print("y", y)

    g = _build_graphviz_graph(graph)
    print(g.source)
    assert "{} [label=x".format(id(x.nodedef)) in g.source
    assert "{} [label=y".format(id(y.nodedef)) in g.source
    assert "[label=print " in g.source
