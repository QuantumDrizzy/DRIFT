"""
drift.ising — the Ising/QUBO core.

Energy of a spin configuration s ∈ {-1, +1}ⁿ:

    E(s) = -½ Σ_ij J_ij s_i s_j  -  Σ_i h_i s_i
         = -½ sᵀ J s  -  hᵀ s

with J a symmetric (n, n) coupling matrix (zero diagonal — self-coupling is
meaningless) and h an (n,) external field. The *ground state* is argmin_s E(s).

This single object is every face of DRIFT: a QUBO problem, a Hopfield memory, a
tile-assembly rule and a replication crystal are all just particular (J, h). The
builders in drift.builders produce them; the solvers find the ground state.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class IsingModel:
    """A classical Ising model. Spins are ±1. See module docstring for the energy."""

    J: np.ndarray
    h: np.ndarray

    def __post_init__(self) -> None:
        self.J = np.asarray(self.J, dtype=np.float64)
        self.h = np.asarray(self.h, dtype=np.float64)
        if self.h.ndim != 1:
            raise ValueError("h must be a 1-D field vector")
        n = self.h.shape[0]
        if self.J.shape != (n, n):
            raise ValueError(f"J must be ({n}, {n}) to match h, got {self.J.shape}")
        # Symmetrize and drop the diagonal so the energy is well defined and the
        # ½ factor never double-counts a bond.
        self.J = 0.5 * (self.J + self.J.T)
        np.fill_diagonal(self.J, 0.0)

    @property
    def n(self) -> int:
        """Number of spins."""
        return self.h.shape[0]

    # ── energy ────────────────────────────────────────────────────────────────
    def energy(self, s: np.ndarray) -> float:
        """E(s) for a single configuration s of shape (n,)."""
        s = np.asarray(s, dtype=np.float64)
        return float(-0.5 * s @ self.J @ s - self.h @ s)

    def energy_batch(self, S: np.ndarray) -> np.ndarray:
        """Energies of a batch S of shape (m, n) — vectorized over m."""
        S = np.asarray(S, dtype=np.float64)
        quad = -0.5 * np.einsum("mi,ij,mj->m", S, self.J, S, optimize=True)
        lin = -(S @ self.h)
        return quad + lin

    # ── single-spin updates (the workhorse of annealing) ──────────────────────
    def delta_energy_flip(self, s: np.ndarray, i: int) -> float:
        """ΔE if spin i flips (s_i → -s_i), computed locally in O(n), no full recompute.

        Derivation: only terms touching spin i change. ΔE = 2 s_i (Σ_j J_ij s_j + h_i).
        """
        return float(2.0 * s[i] * (self.J[i] @ s + self.h[i]))

    def local_fields(self, s: np.ndarray) -> np.ndarray:
        """Effective field on every spin: J s + h (shape (n,)). Useful for parallel/Hopfield updates."""
        return self.J @ s + self.h

    # ── diagnostics ───────────────────────────────────────────────────────────
    @property
    def nbonds(self) -> int:
        """Number of non-zero couplings (upper triangle)."""
        return int(np.count_nonzero(np.triu(self.J)))
