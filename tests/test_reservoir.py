"""Validation of Phase 8 — the reservoir face (DRIFT's first automated tests).

Checks the measurable-computronium claims: memory capacity obeys its bound and
fades with delay, the substrate separates distinct inputs, and the spectral
radius (set via the Spectra spine) matches the dense reference.

Run standalone:  python tests/test_reservoir.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drift.reservoir import IsingReservoir, memory_capacity, separation  # noqa: E402


def test_spectral_radius_is_set_via_spectra():
    sr = 0.9
    res = IsingReservoir(n=120, spectral_radius=sr, seed=3)
    exact = float(np.max(np.abs(np.linalg.eigvals(res.W))))
    # Spectra's power-iteration sets it; agreement with the exact dense radius is
    # within power-iteration precision for a sparse random (non-symmetric) W.
    assert abs(exact - sr) < 0.05, f"radius {exact} vs {sr}"


def test_memory_capacity_within_bound_and_substantial():
    res = IsingReservoir(n=150, spectral_radius=0.95, leak=0.4, seed=0)
    mc, curve = memory_capacity(res, max_delay=200, n_train=1500)
    assert mc <= res.n * 1.05, f"MC {mc} exceeds the bound N={res.n}"
    assert mc > 0.2 * res.n, f"MC {mc} too low for a working reservoir (N={res.n})"
    assert curve.shape == (200,)


def test_memory_fades_with_delay():
    res = IsingReservoir(n=150, spectral_radius=0.95, leak=0.4, seed=0)
    _, curve = memory_capacity(res, max_delay=200, n_train=1500)
    # Recent delays are reconstructed better than distant ones (forgetting curve).
    assert curve[:5].mean() > curve[-20:].mean() + 0.1


def test_separation_zero_for_identical_positive_for_distinct():
    res = IsingReservoir(n=120, spectral_radius=0.95, seed=1)
    assert separation(res, eps=0.0) < 1e-9
    assert separation(res, eps=1e-2) > 1e-6


def _run_standalone() -> int:
    tests = [
        test_spectral_radius_is_set_via_spectra,
        test_memory_capacity_within_bound_and_substantial,
        test_memory_fades_with_delay,
        test_separation_zero_for_identical_positive_for_distinct,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL  {t.__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return failures


if __name__ == "__main__":
    sys.exit(1 if _run_standalone() else 0)
