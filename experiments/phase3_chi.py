"""
Phase 3 — the χ thermometer. How much does a state compute?

We leave the classical ground state behind and turn on quantum mechanics: the
transverse-field Ising chain H = -Σ J Z_i Z_j - Γ Σ X_i. Its ground state is a
superposition whose entanglement we can read off as an entropy S and an effective bond
dimension χ — the χ a matrix-product state would need to store it.

Understanding goal: sweep the field Γ and watch S and χ **peak at the quantum phase
transition** (Γ_c = J for the 1-D chain). Away from the transition the state is nearly a
product state (χ small, cheap); at criticality it is maximally entangled (χ large,
expensive). χ measures *how much computation lives in the state* — the central idea of
DRIFT, made into a curve.

Run:  python experiments/phase3_chi.py   (a few seconds for n=12)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Γ etc. on Windows cp1252 consoles
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drift.quantum import (  # noqa: E402
    ising_chain_1d, tfim_terms, ground_state, entanglement_entropy, effective_chi,
)
from drift import viz  # noqa: E402


def main() -> None:
    n, j = 14, 1.0
    J = ising_chain_1d(n, j=j, periodic=False)
    H_zz, H_x = tfim_terms(J)  # H(Γ) = H_zz + Γ·H_x, ZZ part reused across the sweep

    # Start at Γ=0.15: at Γ→0 the Z2-degenerate ground space (|↑…↑⟩, |↓…↓⟩) is only
    # split by an exponentially small gap, so Lanczos returns a numerically arbitrary
    # member of it and the entropy there is not robust. From Γ≳0.15 the gap is resolved.
    gammas = np.linspace(0.15, 2.0, 28)
    entropies, chis = [], []
    for g in gammas:
        _, psi = ground_state(H_zz + g * H_x)
        S, schmidt = entanglement_entropy(psi, n, cut=n // 2)
        entropies.append(S)
        chis.append(effective_chi(schmidt))

    entropies = np.array(entropies)
    chis = np.array(chis)
    i_peak = int(np.argmax(chis))

    print(f"transverse-field Ising chain  n={n}, J={j}  (Γ_c = J = {j})")
    print(f"  Γ at peak χ : {gammas[i_peak]:.3f}   (theory Γ_c = {j}; finite size shifts it below)")
    print(f"  χ at Γ={gammas[0]:.2f} : {chis[0]:>3d}   S = {entropies[0]:.3f} bits   (ordered / cat state, cheap)")
    print(f"  χ at peak   : {chis[i_peak]:>3d}   S = {entropies[i_peak]:.3f} bits   (critical, most entangled)")
    print(f"  χ at Γ={gammas[-1]:.2f} : {chis[-1]:>3d}   S = {entropies[-1]:.3f} bits   (field-polarized, cheap)")

    viz.plot_chi_sweep(
        gammas, entropies, chis, gamma_c=j,
        title="Phase 3 - χ peaks at the quantum phase transition",
        out="figures/phase3_chi.png",
    )
    print("  figure -> figures/phase3_chi.png")


if __name__ == "__main__":
    main()
