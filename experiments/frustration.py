"""Experiment: ruggedness vs frustration — why annealing exists.

    python -m experiments.frustration
"""

from __future__ import annotations

import os

import numpy as np

from drift.frustration import ruggedness_scan


def main(outdir: str = "figures") -> None:
    p, mins = ruggedness_scan(n=24, p_values=np.linspace(0.0, 0.5, 11), trials=300)
    print("  p(antiferro)   distinct local minima")
    for pi, mi in zip(p, mins):
        print(f"   {pi:.2f}          {mi}")
    print(f"\n  ferromagnet: {mins[0]} basin -> spin glass: {mins[-1]} traps "
          f"({mins[-1] / max(mins[0], 1):.0f}x). Greedy descent can't cope -> anneal.")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(p, np.maximum(mins, 1), "o-", color="#d62728", lw=2)
    ax.set_xlabel("fraction of antiferromagnetic bonds")
    ax.set_ylabel("distinct local minima (log)")
    ax.set_title("Frustration shatters the landscape:\n"
                 "one basin (ferromagnet) → exponentially many traps (spin glass)")
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "frustration_ruggedness.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  saved {path}")


if __name__ == "__main__":
    main()
