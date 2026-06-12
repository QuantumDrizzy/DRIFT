"""
drift.builders.qubo — Face ①: optimization.

A QUBO is `min_{x∈{0,1}ⁿ} xᵀ Q x`. Substituting `x = (s+1)/2` turns it into an Ising
Hamiltonian, so **solving the optimization problem is finding the ground state**:

    J_ij = -½ Q_ij        (i ≠ j)
    h_i  = -½ Σ_j Q_ij
    E_ising(s) = xᵀ Q x - offset          (same argmin)

MaxCut is the cleanest special case — and the cleanest physics. Partition a graph's
nodes into two sides to maximize the weight of edges crossing the cut. As an Ising it is
purely **antiferromagnetic** (`J = -W`, `h = 0`): every edge *wants* its two endpoints
on opposite sides (i.e. cut), so the maximum cut is literally the ground state of an
anti-aligning spin system.
"""

from __future__ import annotations

import numpy as np

from ..ising import IsingModel


def qubo_to_ising(Q: np.ndarray) -> tuple[IsingModel, float]:
    """Map a QUBO matrix Q to (IsingModel, offset), with E_ising(s) = xᵀQx - offset."""
    Q = np.asarray(Q, dtype=np.float64)
    Qs = 0.5 * (Q + Q.T)
    n = Qs.shape[0]
    J = -0.5 * Qs.copy()
    np.fill_diagonal(J, 0.0)
    h = -0.5 * Qs.sum(axis=1)
    model = IsingModel(J, h)
    # Pin the constant offset by matching both expressions at x = s = all-ones.
    ones = np.ones(n)
    offset = float(ones @ Qs @ ones - model.energy(ones))
    return model, offset


def maxcut_ising(W: np.ndarray) -> IsingModel:
    """MaxCut on weighted adjacency W (symmetric, zero diagonal) → antiferromagnetic Ising."""
    W = np.asarray(W, dtype=np.float64)
    W = 0.5 * (W + W.T)
    np.fill_diagonal(W, 0.0)
    return IsingModel(-W, np.zeros(W.shape[0]))


def cut_value(W: np.ndarray, s: np.ndarray) -> float:
    """Total weight of edges cut by partition s (±1): Σ_{i<j} W_ij·(1 - s_i s_j)/2."""
    W = np.asarray(W, dtype=np.float64)
    s = np.asarray(s, dtype=np.float64)
    return float(0.25 * np.sum(W * (1.0 - np.outer(s, s))))


def random_graph(n: int, p: float = 0.5, seed: int = 0, weighted: bool = False) -> np.ndarray:
    """Erdős–Rényi G(n, p) as a symmetric weight matrix. Unweighted → all edges = 1."""
    rng = np.random.default_rng(seed)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                w = rng.uniform(0.5, 2.0) if weighted else 1.0
                W[i, j] = W[j, i] = w
    return W
