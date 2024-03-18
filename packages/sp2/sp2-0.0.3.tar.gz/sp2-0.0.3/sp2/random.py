import numpy as np
from datetime import timedelta
from typing import TypeVar

import sp2
from sp2 import ts
from sp2.stats import numpy_to_list
from sp2.typing import Numpy1DArray, NumpyNDArray

__all__ = ("poisson_timer", "brownian_motion", "brownian_motion_1d")


T = TypeVar("T")


@sp2.node
def poisson_timer(rate: ts[float], seed: object, value: "~T" = True) -> ts["T"]:
    """Generate events according to a Poisson process with time-varying rate.
    For a fixed-interval timer see sp2.timer.

    Args:
        rate: The rate of the Poisson process (per second), must be non-negative
        seed: The seed for the numpy random Generator. Can be anything accepted by np.random.default_rng
        value: The value to tick when there are events (similar to sp2.timer)
    """
    with sp2.alarms():
        event = sp2.alarm(bool)

    with sp2.state():
        s_rng = np.random.default_rng(seed)
        s_scheduled_event = None

    if sp2.ticked(rate):
        if rate < 0:
            raise ValueError(f"{sp2.now()}: rate must be non-negative")
        if s_scheduled_event:
            sp2.cancel_alarm(event, s_scheduled_event)
        if rate > 0:
            seconds = s_rng.exponential(1.0 / rate)
            s_scheduled_event = sp2.schedule_alarm(event, timedelta(seconds=seconds), True)

    if sp2.ticked(event):
        seconds = s_rng.exponential(1.0 / rate)
        s_scheduled_event = sp2.schedule_alarm(event, timedelta(seconds=seconds), True)
        return value


def _make_brownian_increment(t, s_rng, drift, s_cov_decomp):
    # Make the brownian increment as efficiently as possible
    values = s_rng.normal(scale=np.sqrt(t), size=drift.size)
    np.dot(s_cov_decomp, values, out=values)
    np.add(drift * t, values, out=values)
    return values


def _matrix_decomposition(matrix, now):
    # Split matrix decomposition into its own function to help with profiling and make it easier to replace
    # We use SVD instead of Cholesky because it's more stable and handles the zero variance case.
    # Could also use eigenvalue decomposition, but we choose svd because it's the default for np.random.Generator.multivariate_normal
    U, S, Vt = np.linalg.svd(matrix)
    if not np.allclose(matrix, matrix.T):
        raise ValueError(f"{now}: covariance not symmetric")
    if not np.allclose(U, Vt):
        raise ValueError(f"{now}: covariance not positive semidefinite")
    return np.dot(U, np.sqrt(np.diag(S)), out=U)


@sp2.node
def brownian_motion(
    trigger: ts[object],
    drift: ts[Numpy1DArray[float]],
    covariance: ts[NumpyNDArray[float]],
    seed: object,
    return_increments: bool = False,
) -> ts[Numpy1DArray[float]]:
    """Generate multi-dimensional Brownian motion (or increments) at the trigger times, with time-varying drift and covariance.
    The Brownian motion starts once drift and covariance have at least 1 tick each, and will start from zero.
    To use a different start value, use sp2.const(initial_value) + brownian_motion(...)

    Args:
        trigger: When to return the value of the process
        drift: Drift parameter (per second), i.e. array of length n
        covariance: Covariance matrix (per second), i.e. array of size nxn
        seed: The seed for the numpy random Generator. Can be anything accepted by np.random.default_rng
        return_increments: Whether to return increments of the brownian motion at trigger times instead of the process itself
    """
    with sp2.state():
        s_rng = np.random.default_rng(seed)
        s_cov_decomp = None  # Placeholder for covariance matrix decomposition
        s_last_change = None  # Placeholder for last sp2.now()
        s_last_drift = None  # Placeholder for last value of drift
        s_last_value = None  # Placeholder for cumulative value between trigger ticks

    if sp2.ticked(drift, covariance) and sp2.valid(drift, covariance):
        if s_last_change is None:
            if not drift.ndim == 1:
                raise ValueError(f"{sp2.now()}: drift must be 1-dimensional")
            if not covariance.ndim == 2:
                raise ValueError(f"{sp2.now()}: covariance must be 2-dimensional")
            if not drift.size == covariance.shape[0]:
                raise ValueError(f"{sp2.now()}: drift and covariance must have same length")
            s_last_value = np.zeros_like(drift)
        else:
            t = (sp2.now() - s_last_change).total_seconds()
            values = _make_brownian_increment(t, s_rng, s_last_drift, s_cov_decomp)
            np.add(values, s_last_value, out=s_last_value)
        s_last_change = sp2.now()
        if s_last_drift is not None and drift.shape != s_last_drift.shape:
            raise ValueError(f"{sp2.now()}: shape of drift is not allowed to change")
        s_last_drift = drift

    if sp2.ticked(covariance):
        # Only do the covariance decomposition when it changes
        if s_cov_decomp is not None and covariance.shape != s_cov_decomp.shape:
            raise ValueError(f"{sp2.now()}: shape of covariance is not allowed to change")
        s_cov_decomp = _matrix_decomposition(covariance, sp2.now())

    if sp2.ticked(trigger) and sp2.valid(drift, covariance):
        if s_last_change is not None:
            t = (sp2.now() - s_last_change).total_seconds()
            values = _make_brownian_increment(t, s_rng, s_last_drift, s_cov_decomp)
            s_last_change = sp2.now()
            if return_increments:
                # Add in "last value" in case drift/covariance changed in between trigger updates
                np.add(s_last_value, values, out=values)
                s_last_value.fill(0.0)
                return values
            else:
                np.add(s_last_value, values, out=s_last_value)
                return s_last_value


@sp2.graph
def brownian_motion_1d(
    trigger: ts[object], drift: ts[float], variance: ts[float], seed: object, return_increments: bool = False
) -> ts[float]:
    """Generate one-dimensional Brownian motion at the trigger times, with time-varying drift and variance.
    The Brownian motion starts once drift and covariance have at least 1 tick each, and will start from zero.
    To use a different start value, use sp2.const(initial_value) + brownian_motion_1d(...)

    Args:
        trigger: When to return the value of the process
        drift: Drift parameter (per second)
        variance: Variance parameter (per second)
        seed: The seed for the numpy random Generator. Can be anything accepted by np.random.default_rng
        return_increments: Whether to return increments of the brownian motion at trigger times instead of the process itself
    """
    drift = sp2.apply(drift, lambda x: np.array([x]), Numpy1DArray[float])
    covariance = sp2.apply(variance, lambda x: np.array([[x]]), NumpyNDArray[float])
    bm = brownian_motion(trigger, drift, covariance, seed=seed, return_increments=return_increments)
    return numpy_to_list(bm, 1)[0]
