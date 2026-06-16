"""Frustration & spin glasses — why optimization is hard, measured.

DRIFT's Ising engine solves problems by rolling downhill to a ground state. How
hard that is depends on the *landscape*. With uniform ferromagnetic couplings the
landscape has essentially one basin (all spins aligned) — greedy descent always
finds it. Flip a fraction of the couplings to antiferromagnetic and you get
**frustration**: loops of bonds that cannot all be satisfied at once. The energy
landscape shatters into exponentially many local minima — a **spin glass** — and
greedy descent gets trapped in a different one almost every time.

This is the microscopic reason simulated/quantum annealing exists: a glassy QUBO
has a rugged landscape, so you must heat-and-cool to escape traps rather than
descend once. We measure ruggedness directly: the number of distinct local minima
reached by greedy descent from many random starts, as a function of the fraction
of antiferromagnetic bonds.
"""

from __future__ import annotations

import numpy as np

from drift.ising import IsingModel


def random_couplings(n: int, p_negative: float, seed: int = 0) -> IsingModel:
    """Fully-connected Ising with a fraction `p_negative` of antiferromagnetic bonds."""
    rng = np.random.default_rng(seed)
    J = np.ones((n, n))
    neg = rng.random((n, n)) < p_negative
    neg = np.triu(neg, 1)
    neg = neg | neg.T
    J[neg] = -1.0
    np.fill_diagonal(J, 0.0)
    return IsingModel(J=J, h=np.zeros(n))


def greedy_descent(model: IsingModel, s: np.ndarray, max_iter: int = 5000) -> np.ndarray:
    """Flip the most energy-lowering spin until none lowers it (a local minimum)."""
    s = s.copy()
    for _ in range(max_iter):
        deltas = 2.0 * s * model.local_fields(s)     # ΔE for flipping each spin
        i = int(np.argmin(deltas))
        if deltas[i] >= -1e-12:
            break
        s[i] = -s[i]
    return s


def _canonical(s: np.ndarray) -> tuple:
    # fix the global up/down (Z2) symmetry so mirror states aren't double-counted
    return tuple(s if s[0] > 0 else -s)


def count_local_minima(model: IsingModel, trials: int = 200, seed: int = 0) -> int:
    rng = np.random.default_rng(seed)
    n = model.n
    minima = set()
    for _ in range(trials):
        s0 = np.where(rng.random(n) < 0.5, -1.0, 1.0)
        minima.add(_canonical(greedy_descent(model, s0)))
    return len(minima)


def ruggedness_scan(n: int = 24, p_values=None, trials: int = 200, seed: int = 0):
    """Distinct local minima vs the fraction of antiferromagnetic bonds."""
    if p_values is None:
        p_values = np.linspace(0.0, 0.5, 11)
    return np.asarray(p_values), np.array(
        [count_local_minima(random_couplings(n, float(p), seed), trials, seed) for p in p_values]
    )
