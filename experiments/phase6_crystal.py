"""
Phase 6 — Face ③: self-replication (crystallization).

Translation-invariant, frustrated couplings (J1 ferro nearest, J2 antiferro next-nearest,
Jy ferro between rows) whose ground state is a striped crystal. From a hot disordered melt,
annealing settles into the period-4 ↑↑↓↓ pattern: a width-2 stripe — the unit cell —
replicated across the whole lattice. Replication, read as a periodic ground state.

Crucially the answer is nowhere encoded per site: the periodicity *emerges* from the local
rules. (Replication-as-crystallization — the contained, physical version of the grey-goo
story, not a universal constructor.)

Understanding goal: watch a motif copy itself across a lattice purely from local couplings.

Run:  python experiments/phase6_crystal.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drift.builders import crystal_2d, column_period  # noqa: E402
from drift.solvers.exact import exact_ground_state  # noqa: E402
from drift.solvers.annealing import simulated_annealing  # noqa: E402
from drift import viz  # noqa: E402


def main() -> None:
    # 1) Exact check on a small lattice: the ground state really is the stripe crystal.
    small = crystal_2d(4, 4)
    s4, e4, _ = exact_ground_state(small, max_n=18)
    p4 = column_period(s4.reshape(4, 4))
    print(f"exact 4x4   : E = {e4:.1f}  (= -2n)   unit-cell period = {p4}")

    # 2) Grow a larger crystal from a hot melt by annealing.
    rows = cols = 12
    model = crystal_2d(rows, cols)
    n = rows * cols

    rng = np.random.default_rng(3)
    melt = np.sign(rng.standard_normal(n)); melt[melt == 0] = 1

    best_e, best_s = np.inf, None
    for seed in range(6):
        s, e, _, _ = simulated_annealing(model, n_sweeps=8000, T0=4.0, T1=0.01, seed=seed)
        if e < best_e:
            best_e, best_s = e, s
    period = column_period(best_s.reshape(rows, cols))

    print(f"anneal {rows}x{cols}: E = {best_e:.1f}  (= -2n)   unit-cell period = {period}")
    print(f"  crystallized cleanly (period 4): {period == 4}")

    viz.plot_crystal(
        melt, best_s, rows, cols, period=period,
        title="Phase 6 - a motif replicating itself across the lattice",
        out="figures/phase6_crystal.png",
    )
    print("  figure -> figures/phase6_crystal.png")


if __name__ == "__main__":
    main()
