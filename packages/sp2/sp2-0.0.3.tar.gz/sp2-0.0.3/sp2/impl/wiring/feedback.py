from typing import TypeVar

from sp2.impl.__sp2impl import _sp2impl
from sp2.impl.types import tstype
from sp2.impl.types.common_definitions import PushMode
from sp2.impl.types.container_type_normalizer import ContainerTypeNormalizer
from sp2.impl.types.tstype import ts
from sp2.impl.types.typing_utils import Sp2TypingUtils
from sp2.impl.wiring.context import Context
from sp2.impl.wiring.edge import Edge
from sp2.impl.wiring.graph import graph

__all__ = ["feedback"]

T = TypeVar("T")


# This represents a feedback's .out() which is the fed-back input adapter, this should only
# be _created directly from FeedbackOutputDef._create
class FeedbackInputDef:
    def __init__(self, typ):
        self._type = typ

    def ts_inputs(self):
        return ()

    def _create(self, engine, memo, from_output=False):
        # If from_output is false that means this is being created directly in create_engine
        # which implies this feedback .out() is being consumed but it was never bound
        if not from_output:
            raise RuntimeError("unbound sp2.feedback used in graph")
        normalized_type = ContainerTypeNormalizer.normalized_type_to_actual_python_type(self._type)
        return _sp2impl._feedback_input_adapter(None, engine, normalized_type, PushMode.NON_COLLAPSING, ())


# This represents the actual sp2.feedback object that has the bind/out calls
# It acts as the feedback output adapter, its _create ensures it creates the corresponding input
# at the same time and binds it to the output adapter being created
class FeedbackOutputDef:
    def __init__(self, typ):
        self._type = typ
        self._bound_input = None
        self._fb_input_def = FeedbackInputDef(typ)
        self._fb_input = Edge(tstype.ts[typ], self._fb_input_def, 0)

    @classmethod
    def _get_typ_name(cls, typ):
        if Sp2TypingUtils.is_generic_container(typ):
            return str(typ)
        else:
            return typ.__name__

    @graph(memoize=False)
    def _bind(self, x: ts["T"]):
        if self._bound_input is not None:
            raise RuntimeError("sp2.feedback is already bound")

        if not hasattr(Context.TLS, "instance"):
            raise RuntimeError("sp2.feedback bind must be created under a wiring context")

        Context.TLS.instance.roots.append(self)
        self._bound_input = x

    def bind(self, x):
        self._bind.using(T=self._type)(self, x)

    def out(self):
        return self._fb_input

    @property
    def _signature(self):
        return type(self)._signature

    def ts_inputs(self):
        return tuple([((0, -1), self._bound_input)])

    def _create(self, engine, memo):
        # We know output will get created first, force create and register feedback input
        # in memo so it doesnt create a differet instance
        fb_input_adapter = memo[self._fb_input_def] = self._fb_input_def._create(engine, memo, True)
        normalized_type = ContainerTypeNormalizer.normalized_type_to_actual_python_type(self._type)
        return _sp2impl._feedback_output_adapter(None, engine, (normalized_type, fb_input_adapter))


feedback = FeedbackOutputDef
