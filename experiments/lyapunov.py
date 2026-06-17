"""Experiment: the rigorous edge of chaos — Lyapunov exponent vs spectral radius.

Shows the honest gap between the spectral proxy (rho=1) and the true dynamical
edge (lambda=0), with the memory-capacity peak in between.

    python -m experiments.lyapunov
"""

from __future__ import annotations

import os

import numpy as np

from drift.lyapunov import edge_radius, lyapunov_sweep
from drift.reservoir import IsingReservoir, memory_capacity


def main(outdir: str = "figures") -> None:
    radii = np.linspace(0.4, 2.2, 19)
    r, lam = lyapunov_sweep(radii, n=100)
    rc = edge_radius(r, lam)

    mc = np.array([memory_capacity(IsingReservoir(n=100, spectral_radius=float(ri),
                                                  leak=0.3))[0] for ri in radii])
    r_mc = radii[int(np.argmax(mc))]

    print("  rho    lambda    MC")
    for ri, li, mi in zip(r, lam, mc):
        print(f"  {ri:4.2f}  {li:+.4f}  {mi:5.1f}")
    print(f"\n  spectral proxy : rho = 1.00")
    print(f"  MC peak        : rho ~ {r_mc:.2f}")
    print(f"  true edge (l=0): rho ~ {rc:.2f}")
    print("  => rho=1 underestimates the driven edge; best computation is just inside the ordered side.")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("  (matplotlib not installed — skipping figure)")
        return

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.axhline(0.0, color="#444", lw=1)
    ax.plot(r, lam, "o-", color="#1f77b4", lw=2, label=r"max Lyapunov $\lambda(\rho)$")
    ax.fill_between(r, lam, 0, where=(lam < 0), color="#2ca02c", alpha=0.12)
    ax.fill_between(r, lam, 0, where=(lam > 0), color="#d62728", alpha=0.12)

    ax.axvline(1.0, color="#888", ls="--", lw=1.3)
    ax.annotate("spectral proxy\nρ=1", (1.0, ax.get_ylim()[0] * 0.7),
                ha="center", fontsize=8, color="#555")
    ax.axvline(r_mc, color="#2ca02c", ls=":", lw=1.5)
    ax.annotate(f"MC peak\nρ≈{r_mc:.2f}", (r_mc, ax.get_ylim()[1] * 0.55),
                ha="center", fontsize=8, color="#2ca02c")
    if rc == rc:
        ax.axvline(rc, color="#d62728", ls=":", lw=1.5)
        ax.annotate(f"true edge λ=0\nρ≈{rc:.2f}", (rc, ax.get_ylim()[1] * 0.85),
                    ha="center", fontsize=8, color="#d62728")

    ax.text(0.55, ax.get_ylim()[0] * 0.45, "ordered\n(fading memory)", fontsize=8, color="#2ca02c")
    ax.text(1.95, ax.get_ylim()[1] * 0.45, "chaotic\n(ESP lost)", fontsize=8, color="#d62728")
    ax.set_xlabel(r"spectral radius  $\rho$")
    ax.set_ylabel(r"maximal Lyapunov exponent  $\lambda$")
    ax.set_title("The rigorous edge of chaos:\n"
                 "ρ=1 is a lower bound — the driven tanh edge (λ=0) sits above it")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "lyapunov_edge.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  saved {path}")


if __name__ == "__main__":
    main()
