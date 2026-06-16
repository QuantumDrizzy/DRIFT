"""Validate frustration: a ferromagnet has one basin, a spin glass has many."""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drift.frustration import (  # noqa: E402
    count_local_minima,
    greedy_descent,
    random_couplings,
    ruggedness_scan,
)


def test_ferromagnet_has_single_basin():
    m = random_couplings(24, p_negative=0.0, seed=0)
    assert count_local_minima(m, trials=150) == 1      # all-aligned, one minimum (mod flip)


def test_spin_glass_has_many_minima():
    m = random_couplings(24, p_negative=0.5, seed=0)
    assert count_local_minima(m, trials=200) > 10      # rugged landscape, many traps


def test_ruggedness_increases_with_frustration():
    p, mins = ruggedness_scan(n=24, p_values=np.array([0.0, 0.5]), trials=150)
    assert mins[-1] > 5 * mins[0]


def test_greedy_descent_reaches_local_minimum():
    m = random_couplings(20, p_negative=0.5, seed=1)
    rng = np.random.default_rng(2)
    s = np.where(rng.random(20) < 0.5, -1.0, 1.0)
    sm = greedy_descent(m, s)
    # at a local minimum, no single flip lowers the energy
    deltas = 2.0 * sm * m.local_fields(sm)
    assert np.all(deltas >= -1e-9)
