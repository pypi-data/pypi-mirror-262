import sp2
from sp2 import ts


def test_node_custom_name():
    @sp2.node(name="blerg")
    def _other_name(x: ts[int]) -> ts[int]:
        if sp2.ticked(x):
            return x

    assert _other_name.__name__ == "blerg"
