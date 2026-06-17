"""Validate the maximal Lyapunov exponent: sign by regime, edge above rho=1."""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drift.reservoir import IsingReservoir
from drift.lyapunov import edge_radius, lyapunov_sweep, max_lyapunov


def _res(rho: float) -> IsingReservoir:
    return IsingReservoir(n=100, spectral_radius=rho, leak=0.3, seed=0)


def test_ordered_regime_is_contracting():
    # well below the edge: perturbations die, lambda clearly negative (ESP holds)
    assert max_lyapunov(_res(0.5), n_steps=3000) < -0.05


def test_chaotic_regime_is_expanding():
    # well above the edge: perturbations grow, lambda positive
    assert max_lyapunov(_res(3.0), n_steps=3000) > 0.005


def test_lambda_increases_with_radius():
    lo = max_lyapunov(_res(0.5), n_steps=3000)
    hi = max_lyapunov(_res(3.0), n_steps=3000)
    assert hi > lo


def test_edge_sits_above_spectral_proxy():
    # the real dynamical edge (lambda=0) is above rho=1 for a driven tanh reservoir
    radii = np.linspace(0.4, 2.4, 11)
    r, lam = lyapunov_sweep(radii, n=100)
    rc = edge_radius(r, lam)
    assert 1.0 < rc < 2.0


def test_determinism():
    assert max_lyapunov(_res(1.0), n_steps=1500, seed=7) == \
        max_lyapunov(_res(1.0), n_steps=1500, seed=7)
