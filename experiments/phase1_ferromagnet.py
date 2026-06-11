"""
Phase 1 — the engine, validated on a system whose answer we already know.

A 2-D ferromagnetic Ising lattice (J > 0, periodic). Its ground state is trivial by
hand: every spin aligned, energy -2nJ. That is the point — small enough to *know* the
answer, so we can check that (a) brute force finds it and (b) simulated annealing
relaxes to it. Once the engine is trustworthy here, every later face rides on it.

Understanding goal: watch the energy drift downhill to the exact ground state — matter
computing, made into a figure.

Run:  python experiments/phase1_ferromagnet.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drift import IsingModel, exact_ground_state, simulated_annealing, magnetization  # noqa: E402
from drift.metrics import success  # noqa: E402
from drift import viz  # noqa: E402


def ferromagnet_2d(L: int, J: float = 1.0, h: float = 0.0) -> IsingModel:
    """L×L ferromagnetic Ising on a periodic lattice (each site bonds right + down)."""
    n = L * L
    Jmat = np.zeros((n, n))

    def idx(r: int, c: int) -> int:
        return (r % L) * L + (c % L)

    for r in range(L):
        for c in range(L):
            i = idx(r, c)
            for dr, dc in ((1, 0), (0, 1)):  # down, right neighbor (periodic)
                j = idx(r + dr, c + dc)
                Jmat[i, j] += J
                Jmat[j, i] += J
    return IsingModel(Jmat, np.full(n, h))


def main() -> None:
    L = 4
    model = ferromagnet_2d(L, J=1.0, h=0.0)

    # Honest baseline: exact ground state by enumeration (16 spins → 65 536 configs).
    s_exact, e_exact, all_E = exact_ground_state(model)

    # The physics computing: simulated annealing from a hot, random start.
    s_sa, e_sa, traj, Ts = simulated_annealing(model, n_sweeps=400, T0=4.0, T1=1e-2, seed=1)
    reached = success(e_sa, e_exact)

    print(f"2D ferromagnet  L={L}  ({model.n} spins, {model.nbonds} bonds)")
    print(f"  exact ground energy : {e_exact:8.3f}   (theory -2nJ = {-2*model.n:.0f})")
    print(f"  annealing energy    : {e_sa:8.3f}   m = {magnetization(s_sa):+.3f}")
    print(f"  SA reached the exact ground state: {reached}")

    viz.plot_relaxation(
        traj, e_ground=e_exact, Ts=Ts,
        title="Phase 1 - matter computes by drifting downhill",
        out="figures/phase1_relaxation.png",
    )
    viz.plot_spins(
        s_sa, grid_shape=(L, L),
        title=f"Ground state - all spins aligned (m = {magnetization(s_sa):+.0f})",
        out="figures/phase1_groundstate.png",
    )
    viz.plot_landscape(
        all_E, e_ground=e_exact,
        title="Energy landscape (all 2^16 configurations)",
        out="figures/phase1_landscape.png",
    )
    print("  figures -> figures/phase1_{relaxation,groundstate,landscape}.png")


if __name__ == "__main__":
    main()
