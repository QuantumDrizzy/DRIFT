"""Experiment: logic gates as Ising/QUBO ground states.

    python -m experiments.logic
"""

from __future__ import annotations

import itertools
import os

from drift.logic import and_energy, or_energy


def main(outdir: str = "figures") -> None:
    print("Boolean logic from energy minimisation (ground state E=0 -> valid row):\n")
    for name, fn in [("AND", and_energy), ("OR", or_energy)]:
        print(f"  {name}:  x y z -> E")
        for x, y, z in itertools.product((0, 1), repeat=3):
            tag = "  <- ground (valid)" if fn(x, y, z) == 0 else ""
            print(f"        {x} {y} {z} -> {fn(x, y, z):+d}{tag}")
        print()

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    configs = list(itertools.product((0, 1), repeat=3))
    labels = ["".join(map(str, c)) for c in configs]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, (name, fn) in zip(axes, [("AND", and_energy), ("OR", or_energy)]):
        E = [fn(*c) for c in configs]
        colors = ["#2ca02c" if e == 0 else "#d62728" for e in E]
        ax.bar(labels, E, color=colors)
        ax.set_title(f"{name}: ground states (E=0, green) = truth table")
        ax.set_xlabel("x y z"); ax.set_ylabel("penalty energy")
    fig.suptitle("Logic gates are ground states of an Ising/QUBO penalty "
                 "— the substrate computes by relaxing to a minimum", fontsize=11)
    fig.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "logic_gates.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  saved {path}")


if __name__ == "__main__":
    main()
