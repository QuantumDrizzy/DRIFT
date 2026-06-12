"""
drift.builders.hopfield — Face ④: neural memory.

A Hopfield network IS an Ising model: neurons = spins, synaptic weights = J, and stored
memories = energy minima (attractors). Storing patterns with the Hebbian rule

    J_ij = (1/N) Σ_μ ξ_i^μ ξ_j^μ        (J_ii = 0)

makes each pattern ξ^μ a local energy minimum; recalling a memory from a noisy cue is
just relaxing to the nearest attractor. So "remembering" is the self-assembly of an
attractor — the same engine as the crystal in Phase 6, wearing a neuroscience hat.

(Hopfield, PNAS 1982; Nobel Prize in Physics 2024. Capacity ≈ 0.138·N patterns before
memories start to interfere — see CONCEPTS.md.)
"""

from __future__ import annotations

import numpy as np

from ..ising import IsingModel


def hopfield_model(patterns: np.ndarray) -> IsingModel:
    """Hebbian couplings from stored patterns (each ±1; shape (P, N)) → IsingModel (h = 0)."""
    P = np.asarray(patterns, dtype=np.float64)
    if P.ndim == 1:
        P = P[None, :]
    n = P.shape[1]
    J = (P.T @ P) / n
    np.fill_diagonal(J, 0.0)
    return IsingModel(J, np.zeros(n))


def recall(model: IsingModel, cue: np.ndarray, *, max_iter: int = 100, seed: int = 0) -> np.ndarray:
    """Asynchronous Hopfield dynamics — deterministic relaxation to the nearest attractor.

    Repeatedly update s_i ← sign(Σ_j J_ij s_j) in random order until a fixed point. The
    fixed point is the recovered memory. (No temperature; this is the zero-T limit of the
    annealer, the classic associative-recall rule.)
    """
    rng = np.random.default_rng(seed)
    s = np.asarray(cue, dtype=np.float64).copy()
    n = len(s)
    for _ in range(max_iter):
        changed = False
        for i in rng.permutation(n):
            new = 1.0 if (model.J[i] @ s) >= 0.0 else -1.0
            if new != s[i]:
                s[i] = new
                changed = True
        if not changed:
            break
    return s


def add_noise(pattern: np.ndarray, *, flip_frac: float = 0.2, seed: int = 0) -> np.ndarray:
    """Corrupt a pattern by flipping a fraction of its bits — a noisy recall cue."""
    rng = np.random.default_rng(seed)
    s = np.asarray(pattern, dtype=np.float64).copy()
    n = len(s)
    k = int(round(flip_frac * n))
    if k > 0:
        s[rng.choice(n, size=k, replace=False)] *= -1.0
    return s


def overlap(s: np.ndarray, pattern: np.ndarray) -> float:
    """Normalized overlap (1/N) s·ξ ∈ [-1, 1]. 1 = perfect recall, -1 = the inverse memory."""
    return float(np.mean(np.asarray(s) * np.asarray(pattern)))
