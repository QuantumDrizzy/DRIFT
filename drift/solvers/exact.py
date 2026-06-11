"""
drift.solvers.exact — exact ground state by brute-force enumeration.

The honest baseline: enumerate all 2ⁿ spin configurations and take the minimum. Only
tractable for small n (≈ 22 spins is ~4M configs), which is exactly the regime where
*understanding* starts — small enough to know the right answer, so every other solver
can be checked against it.

Also returns the full energy spectrum, which is the raw material for the energy
landscape visual.
"""

from __future__ import annotations

import numpy as np

from ..ising import IsingModel


def all_configs(n: int) -> np.ndarray:
    """All 2ⁿ spin configurations as a (2ⁿ, n) array of ±1.

    Bit b of the row index maps to spin (1 - 2b): bit 0 → +1, bit 1 → -1.
    """
    if n > 24:
        raise ValueError(f"2^{n} configurations is too many to enumerate")
    idx = np.arange(1 << n, dtype=np.uint64)
    # Cast bits to a SIGNED type before (1 - 2*bits): in unsigned arithmetic
    # 1 - 2 wraps to a huge value, turning -1 spins into ~4.3e9.
    bits = ((idx[:, None] >> np.arange(n, dtype=np.uint64)[None, :]) & 1).astype(np.int8)
    return (1 - 2 * bits).astype(np.float64)


def exact_ground_state(model: IsingModel, max_n: int = 22):
    """Return (s_min, e_min, all_energies).

    s_min          ground-state spin configuration, shape (n,)
    e_min          its energy
    all_energies   energy of every one of the 2ⁿ configurations (for the landscape)
    """
    n = model.n
    if n > max_n:
        raise ValueError(
            f"exact ground state only up to {max_n} spins (got {n}); use annealing instead"
        )
    S = all_configs(n)
    E = model.energy_batch(S)
    i = int(np.argmin(E))
    return S[i].copy(), float(E[i]), E
