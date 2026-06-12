"""
Phase 2 — Face ①: optimization. MaxCut on a random graph.

MaxCut: split a graph's nodes into two sides to maximize the weight of edges that cross
the cut. As an Ising model this is purely antiferromagnetic (J = -W, h = 0): every edge
wants its endpoints on opposite sides, so the maximum cut **is the ground state**.

Understanding goal: watch optimization *be* a ground-state search. The same engine from
Phase 1, fed a different (J, h), now solves a real combinatorial problem — and we check
the annealer against the exact optimum.

Run:  python experiments/phase2_maxcut.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drift import exact_ground_state, simulated_annealing  # noqa: E402
from drift.builders import maxcut_ising, cut_value, random_graph  # noqa: E402
from drift.metrics import success  # noqa: E402
from drift import viz  # noqa: E402


def main() -> None:
    n, p, seed = 14, 0.5, 3
    W = random_graph(n, p=p, seed=seed, weighted=False)
    n_edges = int((W != 0).sum() // 2)
    model = maxcut_ising(W)

    # Honest baseline: exact ground state (14 spins -> 16 384 configs).
    s_exact, e_exact, traj_E = exact_ground_state(model)
    cut_exact = cut_value(W, s_exact)

    # The physics computing: anneal it.
    s_sa, e_sa, traj, Ts = simulated_annealing(model, n_sweeps=600, T0=4.0, T1=1e-2, seed=1)
    cut_sa = cut_value(W, s_sa)
    reached = success(e_sa, e_exact)

    print(f"MaxCut  n={n}, edges={n_edges}  (G(n,p={p}))")
    print(f"  exact max cut    : {cut_exact:.0f}  (ground energy {e_exact:.3f})")
    print(f"  annealing cut    : {cut_sa:.0f}  (energy {e_sa:.3f})")
    print(f"  annealing reached the optimum: {reached}")

    viz.plot_relaxation(
        traj, e_ground=e_exact, Ts=Ts,
        title="Phase 2 - optimization IS a ground-state search",
        out="figures/phase2_relaxation.png",
    )
    viz.plot_graph_cut(
        W, s_sa,
        title=f"MaxCut - {cut_sa:.0f} of {n_edges} edges cut (optimum)",
        out="figures/phase2_maxcut.png",
    )
    print("  figures -> figures/phase2_{relaxation,maxcut}.png")


if __name__ == "__main__":
    main()
