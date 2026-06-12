"""
drift.builders.crystal — Face ③: self-replication (crystallization).

Replication, contained: a motif that copies itself across the lattice. Read physically,
that is a **periodic ground state** — a crystal. The key honesty is that the periodicity
is not painted in by per-site fields encoding the answer; it *emerges* from translation-
invariant, frustrated couplings. Nowhere is any cell told what to be.

Along one axis we use the axial-frustrated (ANNNI-at-T=0) recipe:

    nearest-neighbour      J1 > 0   (ferromagnetic: align)
    next-nearest-neighbour J2 < 0   (antiferromagnetic: anti-align at distance 2)

For |J2| > J1/2 the 1-D ground state is the period-4  ↑↑↓↓  phase: a two-up/two-down
unit cell tiling the chain. Along the other axis a ferromagnetic coupling makes every row
copy its neighbour, so the motif replicates in 2-D into clean vertical stripes — a crystal
grown from purely local rules. (Replication-as-crystallization; not a universal
constructor — see CONCEPTS honesty tags.)
"""

from __future__ import annotations

import numpy as np

from ..ising import IsingModel


def crystal_2d(rows: int, cols: int, *, j1: float = 1.0, j2: float = -1.0,
               jy: float = 1.0, periodic: bool = True) -> IsingModel:
    """Translation-invariant frustrated couplings whose ground state is a striped crystal.

    Along x: nearest `j1` (ferro) + next-nearest `j2` (antiferro) → period-4 ↑↑↓↓.
    Along y: nearest `jy` (ferro) → rows copy each other. With `|j2| > j1/2` the ground
    state is vertical stripes of width 2 (the replicated unit cell).
    """
    n = rows * cols
    J = np.zeros((n, n))

    def idx(r, c):
        return r * cols + c

    def add(a, b, w):
        J[a, b] += w
        J[b, a] += w

    for r in range(rows):
        for c in range(cols):
            a = idx(r, c)
            # x: nearest and next-nearest neighbours
            for dc, w in ((1, j1), (2, j2)):
                cc = c + dc
                if cc < cols:
                    add(a, idx(r, cc), w)
                elif periodic:
                    add(a, idx(r, cc % cols), w)
            # y: nearest neighbour (rows replicate)
            rr = r + 1
            if rr < rows:
                add(a, idx(rr, c), jy)
            elif periodic:
                add(a, idx(rr % rows, c), jy)
    return IsingModel(J, np.zeros(n))


def column_period(grid: np.ndarray) -> int:
    """Smallest horizontal period p such that column c == column c+p for all c (else cols).

    The order parameter of the crystal: how large the replicated unit cell is along x.
    """
    grid = np.asarray(grid)
    cols = grid.shape[1]
    for p in range(1, cols):
        if cols % p == 0 and np.all(grid == np.roll(grid, p, axis=1)):
            return p
    return cols


def is_striped(grid: np.ndarray) -> bool:
    """True if the configuration is the defect-free period-4 vertical-stripe crystal."""
    return column_period(np.asarray(grid)) == 4
