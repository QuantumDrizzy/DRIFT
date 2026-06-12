"""
Phase 5 — Face ②: self-assembly (Wang tiles / aTAM).

A jigsaw of tiles binds by glue affinity. We build a tile set whose unique maximum-bond
arrangement renders a target shape (a 'plus'), scramble it hot, and let annealing settle
it. The assembled structure is, once more, a ground state — local matching rules producing
a global designed form. The constructive face of the nano story.

Understanding goal: watch a designed structure assemble itself from glue rules alone.

Run:  python experiments/phase5_tiles.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drift.builders import jigsaw, tiles_qubo, decode_tiling, count_bonds, render, qubo_to_ising  # noqa: E402
from drift.solvers.annealing import simulated_annealing  # noqa: E402
from drift import viz  # noqa: E402


def main() -> None:
    L = 3
    image = np.array([[0, 1, 0],
                      [1, 1, 1],
                      [0, 1, 0]], dtype=float)  # a 'plus' to assemble

    tiles, target = jigsaw(L, L, image)
    K = len(tiles)
    Q, _ = tiles_qubo(tiles, L, L, bond_reward=1.0)
    model, _ = qubo_to_ising(Q)
    max_bonds = count_bonds(tiles, target)

    # A hot, disordered snapshot for the "before" panel.
    rng = np.random.default_rng(0)
    hot = np.sign(rng.standard_normal(model.n)); hot[hot == 0] = 1
    dis_grid, _ = decode_tiling(hot, L, L, K)

    # Anneal with restarts — the jigsaw is a rigid, frustrated puzzle.
    best_e, best_s = np.inf, None
    for seed in range(8):
        s, e, _, _ = simulated_annealing(model, n_sweeps=20000, T0=5.0, T1=0.005, seed=seed)
        if e < best_e:
            best_e, best_s = e, s
    grid, valid = decode_tiling(best_s, L, L, K)
    bonds = count_bonds(tiles, grid)

    print(f"Wang tiles  {L}x{L} grid, {K} tile types -> {model.n} spins")
    print(f"  max bonds        : {max_bonds}")
    print(f"  assembled bonds  : {bonds}   (valid one-hot: {valid})")
    print(f"  matches target   : {bool(np.array_equal(grid, target))}")

    viz.plot_assembly(
        render(tiles, dis_grid), render(tiles, grid), L,
        bonds=bonds, max_bonds=max_bonds,
        title="Phase 5 - a structure assembling itself by minimizing bond energy",
        out="figures/phase5_assembly.png",
    )
    print("  figure -> figures/phase5_assembly.png")


if __name__ == "__main__":
    main()
