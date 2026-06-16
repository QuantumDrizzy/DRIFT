"""Experiment: the energy price of computation — capacity vs dissipation vs ρ.

    python -m experiments.compute_cost
"""

from __future__ import annotations

import os

import numpy as np

from drift.compute_cost import capacity_cost_sweep


def main(outdir: str = "figures") -> None:
    radii = np.linspace(0.3, 1.4, 16)
    r, mc, diss, eff = capacity_cost_sweep(radii, n=120)

    print("  rho   MC     churn   efficiency")
    for i in range(len(r)):
        print(f"  {r[i]:.2f}  {mc[i]:6.2f}  {diss[i]:.3f}   {eff[i]:.2f}")
    print(f"\n  MC peaks at rho = {r[np.argmax(mc)]:.2f} (edge of chaos); "
          f"cost rises monotonically -> efficiency favours low rho = {r[np.argmax(eff)]:.2f}.")
    print("  => the edge maximises CAPACITY, not efficiency: peak capability is not the cheapest point.")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("  (matplotlib not installed — skipping figure)")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(r, mc / mc.max(), "o-", color="#2ca02c", lw=2, label="memory capacity (norm.)")
    ax.plot(r, diss / diss.max(), "s-", color="#d62728", lw=2, label="cost: recurrent drive ‖W·x‖ (norm.)")
    ax.axvline(1.0, color="#888", ls="--", lw=1.5)
    ax.annotate("edge of chaos\n(max capacity)", (1.03, 0.45), fontsize=8, color="#555")
    ax.set_xlabel("spectral radius  ρ")
    ax.set_ylabel("normalised")
    ax.set_title("The energy price of computation:\n"
                 "capacity peaks at the edge, but cost keeps rising — peak capability isn't free")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "compute_cost.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  saved {path}")


if __name__ == "__main__":
    main()
