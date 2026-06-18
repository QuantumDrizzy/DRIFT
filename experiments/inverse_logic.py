"""Experiment: inverse computronium — synthesise a QUBO from a target truth table.

    python -m experiments.inverse_logic

Forward (logic.py): a hand-written penalty -> a gate. Inverse (here): a target truth table
-> the penalty, by linear feasibility. The figure shows a *synthesised* AND landscape (valid
rows pinned to 0, invalid lifted above a gap), the honest XOR limit, and the synthesised
penalty being annealed by DRIFT's own spine down to a valid row.
"""

from __future__ import annotations

import itertools
import os

from drift.logic import TRUTH
from drift.solvers import simulated_annealing
from drift.inverse_logic import (
    NotQuadratic,
    qubo_energy,
    qubo_to_ising,
    spins_to_bits,
    synthesize,
    truth_from_fn,
    xor_via_composition,
)


def main(outdir: str = "figures") -> None:
    Q, off = synthesize(TRUTH["AND"], 3)                # target truth table -> QUBO
    configs = list(itertools.product((0, 1), repeat=3))
    labels = ["".join(map(str, c)) for c in configs]
    E = [qubo_energy(Q, off, c) for c in configs]

    print("Inverse computronium — synthesised AND penalty (x y z -> E):\n")
    for c, e in zip(configs, E):
        tag = "  <- ground (valid)" if abs(e) < 1e-6 else ""
        print(f"   {c[0]} {c[1]} {c[2]} -> {e:+.2f}{tag}")
    try:
        synthesize(truth_from_fn(lambda x, y: x ^ y, 2), 3)
    except NotQuadratic:
        print("\n   XOR: NotQuadratic (no 2-local QUBO) — recovered by composition:",
              xor_via_composition() == truth_from_fn(lambda x, y: x ^ y, 2))

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    _, _, traj, _ = simulated_annealing(qubo_to_ising(Q, off), n_sweeps=300, seed=0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    colors = ["#2ca02c" if abs(e) < 1e-6 else "#d62728" for e in E]
    ax1.bar(labels, E, color=colors)
    ax1.axhline(0, color="k", lw=0.8)
    ax1.set_title("Synthesised AND: target table -> QUBO\n(green E=0 = the rows we asked for)")
    ax1.set_xlabel("x y z"); ax1.set_ylabel("synthesised penalty energy")

    ax2.plot(traj, color="#1f77b4")
    ax2.set_title("DRIFT's annealer relaxes the synthesised QUBO\nto a ground state (a valid AND row)")
    ax2.set_xlabel("sweep"); ax2.set_ylabel("Ising energy")

    fig.suptitle("Inverse design of computation: ask for a truth table, get the couplings — "
                 "then let matter compute it by relaxing", fontsize=11)
    fig.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "inverse_computronium.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"\n  saved {path}")


if __name__ == "__main__":
    main()
