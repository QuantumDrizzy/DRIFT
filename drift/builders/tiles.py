"""
drift.builders.tiles — Face ②: self-assembly (Wang tiles / aTAM).

The abstract Tile Assembly Model: square tiles with a glue colour on each edge (N, E, S, W)
drop onto a grid and bind when touching edges share a glue. A target structure is the
arrangement that satisfies the most bonds — i.e. the **lowest-energy** placement. So
"a structure assembling itself" is, once again, a ground state.

Encoding (QUBO, one-hot over tile types per cell):

    x_{c,k} ∈ {0,1}   = "cell c holds tile type k"
    one-hot penalty   A·(Σ_k x_{c,k} - 1)²            (exactly one tile per cell)
    bond reward       -B·x_{a,k}·x_{b,l}  for every adjacency (a,b)
                       whose facing glues match  (tile k's E == tile l's W, etc.)

Minimising xᵀQx then maximises the number of satisfied bonds. We generate a *jigsaw*:
every internal edge gets its own unique glue, so the only arrangement that satisfies all
bonds is the intended one — a single, self-assembling ground state we can check against.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Glue 0 is the inert "border" colour: it faces outside the grid and never rewards a bond.
BORDER = 0


@dataclass(frozen=True)
class Tile:
    """A Wang tile: glue colours on its four edges, plus a value for rendering."""
    n: int
    e: int
    s: int
    w: int
    color: float = 0.0


def jigsaw(rows: int, cols: int, image: np.ndarray | None = None):
    """Build a jigsaw tile set whose unique max-bond tiling is the in-order arrangement.

    Returns (tiles, target_grid):
      tiles        list of `rows*cols` Tile objects, one per target cell (row-major)
      target_grid  (rows, cols) int array of tile indices = the intended assembly

    Each internal edge is given its own unique glue colour shared by exactly the two tiles
    that meet there; border-facing edges get glue 0. With all-distinct internal glues, the
    bond constraints are rigid and the intended arrangement is the only one satisfying them.
    `image` (rows×cols) optionally colours the tiles so the assembled grid renders a picture.
    """
    if image is None:
        image = np.arange(rows * cols, dtype=float).reshape(rows, cols)
    image = np.asarray(image, dtype=float)

    n_glue = {}  # north glue per cell
    w_glue = {}  # west glue per cell
    e_glue = {}  # east glue per cell
    s_glue = {}  # south glue per cell
    g = BORDER + 1

    for r in range(rows):
        for c in range(cols):
            # Horizontal edge to the east neighbour gets a fresh shared glue.
            if c + 1 < cols:
                e_glue[(r, c)] = g
                w_glue[(r, c + 1)] = g
                g += 1
            else:
                e_glue[(r, c)] = BORDER
            # Vertical edge to the south neighbour gets a fresh shared glue.
            if r + 1 < rows:
                s_glue[(r, c)] = g
                n_glue[(r + 1, c)] = g
                g += 1
            else:
                s_glue[(r, c)] = BORDER
            w_glue.setdefault((r, c), BORDER)
            n_glue.setdefault((r, c), BORDER)

    tiles = []
    target = np.zeros((rows, cols), dtype=int)
    for r in range(rows):
        for c in range(cols):
            target[r, c] = r * cols + c
            tiles.append(Tile(n_glue[(r, c)], e_glue[(r, c)], s_glue[(r, c)],
                              w_glue[(r, c)], float(image[r, c])))
    return tiles, target


def tiles_qubo(tiles, rows, cols, *, bond_reward=1.0, onehot_penalty=None):
    """Assemble the QUBO matrix Q (n×n, n = rows*cols*K) and an index map.

    Returns (Q, index_of) where index_of(cell, k) -> spin index for tile type k at cell.
    Off-diagonals are written in the upper triangle; after symmetrisation the effective
    coefficient of x_i x_j (i<j) in xᵀQx equals the value stored at Q[i, j].
    """
    K = len(tiles)
    ncell = rows * cols
    n = ncell * K
    B = float(bond_reward)
    # One-hot must outweigh any bond gain from cheating: a cell touches ≤4 edges.
    A = float(onehot_penalty) if onehot_penalty is not None else 5.0 * B

    def index_of(cell, k):
        return cell * K + k

    Q = np.zeros((n, n))

    # One-hot per cell: A·(Σ_k x - 1)² → diagonal -A, intra-cell pair +2A.
    for cell in range(ncell):
        for k in range(K):
            i = index_of(cell, k)
            Q[i, i] += -A
            for l in range(k + 1, K):
                Q[i, index_of(cell, l)] += 2.0 * A

    def cell_id(r, c):
        return r * cols + c

    # Bond rewards across every internal adjacency.
    for r in range(rows):
        for c in range(cols):
            a = cell_id(r, c)
            if c + 1 < cols:  # east neighbour: a.E must equal b.W
                b = cell_id(r, c + 1)
                for k, tk in enumerate(tiles):
                    for l, tl in enumerate(tiles):
                        if tk.e != BORDER and tk.e == tl.w:
                            i, j = index_of(a, k), index_of(b, l)
                            lo, hi = min(i, j), max(i, j)
                            Q[lo, hi] += -B
            if r + 1 < rows:  # south neighbour: a.S must equal b.N
                b = cell_id(r + 1, c)
                for k, tk in enumerate(tiles):
                    for l, tl in enumerate(tiles):
                        if tk.s != BORDER and tk.s == tl.n:
                            i, j = index_of(a, k), index_of(b, l)
                            lo, hi = min(i, j), max(i, j)
                            Q[lo, hi] += -B
    return Q, index_of


def decode_tiling(bits, rows, cols, K):
    """Turn a bit/spin vector into a (rows, cols) grid of tile indices (argmax per cell).

    Accepts ±1 spins or {0,1} bits. Returns (grid, valid) where valid is False if any
    cell is not exactly one-hot.
    """
    x = (np.asarray(bits, dtype=float) + 1.0) / 2.0 if np.min(bits) < 0 else np.asarray(bits, float)
    ncell = rows * cols
    x = x.reshape(ncell, K)
    grid = np.argmax(x, axis=1).reshape(rows, cols)
    valid = bool(np.all(x.sum(axis=1) == 1))
    return grid, valid


def count_bonds(tiles, grid):
    """Number of internal edges whose facing glues match, for a (rows, cols) tile grid."""
    grid = np.asarray(grid)
    rows, cols = grid.shape
    bonds = 0
    for r in range(rows):
        for c in range(cols):
            tk = tiles[grid[r, c]]
            if c + 1 < cols:
                tl = tiles[grid[r, c + 1]]
                if tk.e != BORDER and tk.e == tl.w:
                    bonds += 1
            if r + 1 < rows:
                tl = tiles[grid[r + 1, c]]
                if tk.s != BORDER and tk.s == tl.n:
                    bonds += 1
    return bonds


def render(tiles, grid):
    """Map a tile-index grid to its colour values (the assembled picture)."""
    grid = np.asarray(grid)
    return np.vectorize(lambda idx: tiles[idx].color)(grid)
