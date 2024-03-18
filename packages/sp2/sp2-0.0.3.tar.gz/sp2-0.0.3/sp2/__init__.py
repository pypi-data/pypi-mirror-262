import os

from sp2.baselib import *
from sp2.curve import curve
from sp2.dataframe import DataFrame
from sp2.impl.builtin_functions import *
from sp2.impl.config import Config
from sp2.impl.constants import UNSET
from sp2.impl.enum import DynamicEnum, Enum
from sp2.impl.error_handling import set_print_full_exception_stack
from sp2.impl.genericpushadapter import GenericPushAdapter
from sp2.impl.mem_cache import memoize, sp2_memoized
from sp2.impl.struct import Struct
from sp2.impl.types.common_definitions import OutputBasket, Outputs, OutputTypeError, PushMode
from sp2.impl.types.tstype import AttachType as attach, DynamicBasket, SnapKeyType as snapkey, SnapType as snap, ts
from sp2.impl.wiring import (
    DelayedEdge,
    Sp2ParseError,
    add_graph_output,
    build_graph,
    dynamic,
    feedback,
    graph,
    node,
    numba_node,
    run,
    run_on_thread,
)
from sp2.impl.wiring.context import clear_global_context, new_global_context
from sp2.math import *
from sp2.showgraph import show_graph

from . import cache_support, stats

__version__ = "0.0.3"


def get_include_path():
    return os.path.join(os.path.dirname(__file__), "include")


def get_lib_path():
    return os.path.join(os.path.dirname(__file__), "lib")
