"""
Phase 4 — Face ④: neural memory (Hopfield).

Store a few visual patterns as energy minima with the Hebbian rule, corrupt one with
noise, and let the Hopfield dynamics relax it back. The same engine as every other phase
(an Ising model), now with synaptic couplings — and "remembering" is literally relaxing
to the nearest attractor. The neuroscience face. (Hopfield, Nobel Physics 2024.)

Understanding goal: watch a noisy cue self-assemble back into a clean stored memory.

Run:  python experiments/phase4_hopfield.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from drift.builders import hopfield_model, recall, add_noise, overlap  # noqa: E402
from drift import viz  # noqa: E402


def make_patterns(L: int = 10) -> np.ndarray:
    """Three recognizable L×L patterns as ±1 vectors: an X, a frame, and a T."""
    x = -np.ones((L, L))
    for i in range(L):
        x[i, i] = 1.0
        x[i, L - 1 - i] = 1.0
    fr = -np.ones((L, L))
    fr[0, :] = fr[-1, :] = fr[:, 0] = fr[:, -1] = 1.0
    t = -np.ones((L, L))
    t[0:2, :] = 1.0
    t[:, L // 2 - 1:L // 2 + 1] = 1.0
    return np.array([x.ravel(), fr.ravel(), t.ravel()])


def main() -> None:
    L = 10
    patterns = make_patterns(L)
    n = L * L
    model = hopfield_model(patterns)

    target = 0  # the X
    cue = add_noise(patterns[target], flip_frac=0.25, seed=2)
    rec = recall(model, cue, seed=1)

    m_cue = overlap(cue, patterns[target])
    m_rec = overlap(rec, patterns[target])

    print(f"Hopfield  n={n} neurons, {len(patterns)} memories (capacity ~{0.138 * n:.0f})")
    print(f"  noisy cue overlap : {m_cue:+.3f}   (25% of bits flipped)")
    print(f"  recovered overlap : {m_rec:+.3f}")
    print(f"  perfect recall    : {bool(np.allclose(rec, patterns[target]))}")

    viz.plot_recall(
        patterns[target], cue, rec, L, overlaps=(m_cue, m_rec),
        title="Phase 4 - memory is the self-assembly of an attractor",
        out="figures/phase4_recall.png",
    )
    print("  figure -> figures/phase4_recall.png")


if __name__ == "__main__":
    main()
