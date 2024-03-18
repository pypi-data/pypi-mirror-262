from datetime import timedelta
from typing import Dict, List, TypeVar

import sp2
from sp2 import ts
from sp2.lib import _sp2basketlibimpl

__all__ = ["sync", "sync_dict", "sync_list"]
T = TypeVar("T")
K = TypeVar("K")
Y = TypeVar("Y")


@sp2.node(cppimpl=_sp2basketlibimpl._sync_list)
def sync_list(x: [ts["T"]], threshold: timedelta, output_incomplete: bool = True) -> sp2.OutputBasket(
    List[ts["T"]], shape_of="x"
):
    with sp2.alarms():
        a_end = sp2.alarm(bool)

    with sp2.state():
        s_current = {}
        s_alarm_handle = None

    if sp2.ticked(x):
        if not s_alarm_handle:
            s_alarm_handle = sp2.schedule_alarm(a_end, threshold, True)
        s_current.update(x.tickeditems())

    if sp2.ticked(a_end) or len(s_current) == len(x):
        if len(s_current) == len(x) or output_incomplete:
            sp2.output(s_current)
        if s_alarm_handle:
            sp2.cancel_alarm(a_end, s_alarm_handle)
            s_alarm_handle = None
        s_current = {}


@sp2.graph
def sync_dict(x: {"K": ts["T"]}, threshold: timedelta, output_incomplete: bool = True) -> sp2.OutputBasket(
    Dict["K", ts["T"]], shape_of="x"
):
    values = list(x.values())
    synced = sync_list(values, threshold, output_incomplete)
    return {k: v for k, v in zip(x.keys(), synced)}


def sync(x, threshold: timedelta, output_incomplete: bool = True):
    if isinstance(x, list):
        return sync_list(x, threshold, output_incomplete)
    elif isinstance(x, dict):
        return sync_dict(x, threshold, output_incomplete)
    raise ValueError(f"Input must be list or dict basket, got: {type(x)}")


@sp2.node(cppimpl=_sp2basketlibimpl._sample_list)
def sample_list(trigger: ts["Y"], x: [ts["T"]]) -> sp2.OutputBasket(List[ts["T"]], shape_of="x"):
    """will return valid items in x on trigger"""
    with sp2.start():
        sp2.make_passive(x)

    if sp2.ticked(trigger):
        result = {k: v for k, v in x.validitems()}
        if result:
            return result


@sp2.graph()
def sample_dict(trigger: ts["Y"], x: {"K": ts["T"]}) -> sp2.OutputBasket(Dict["K", ts["T"]], shape_of="x"):
    """will return valid items in x on trigger"""
    values = list(x.values())
    sampled_values = sample_list(trigger, values)
    return {key: value for key, value in zip(x.keys(), sampled_values)}


def sample_basket(trigger, x):
    """will return valid items in x on trigger"""
    if isinstance(x, list):
        return sample_list(trigger, x)
    elif isinstance(x, dict):
        return sample_dict(trigger, x)
    raise ValueError(f"Input must be a list or dict basket, got: {type(x)}")
