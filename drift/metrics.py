"""
drift.metrics — observables. The instrumentation that turns "it computed" into
numbers you can read and compare across the four faces.

Phase 1 ships the cheap classical observables. The headline probe — the bond
dimension χ as a measure of *how much* a state computes — arrives in Phase 3 with the
tensor-network solver.
"""

from __future__ import annotations

import numpy as np

from .ising import IsingModel

# Boltzmann constant (J/K)
_K_B = 1.380649e-23


def magnetization(s: np.ndarray) -> float:
    """Mean spin ⟨s⟩ ∈ [-1, 1]. Order parameter: ±1 = fully ordered, 0 = disordered."""
    return float(np.mean(s))


def energy_per_spin(model: IsingModel, s: np.ndarray) -> float:
    """E(s) / n — lets you compare systems of different size."""
    return model.energy(s) / model.n


def landauer_energy_j(n_bits: float, temperature_k: float = 300.0) -> float:
    """Landauer floor: minimum energy to irreversibly erase `n_bits` bits, in Joules.

    E_min = n_bits · k_B · T · ln 2.  At T = 300 K this is ≈ 2.87e-21 J per bit.
    Used by the 'cosmic roofline' (Phase 7) to place real computation against the
    thermodynamic limit.
    """
    return float(n_bits * _K_B * temperature_k * np.log(2.0))


def success(found_energy: float, exact_energy: float, tol: float = 1e-9) -> bool:
    """Did the solver reach the exact ground-state energy (within tol)?"""
    return abs(found_energy - exact_energy) <= tol * (1.0 + abs(exact_energy))
