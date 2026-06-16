"""Validate the capacity-vs-cost analysis across the edge of chaos."""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drift.compute_cost import (  # noqa: E402
    capacity_cost_sweep,
    landauer_floor_joules,
)

RADII = np.linspace(0.4, 1.3, 10)


def test_capacity_peaks_at_edge_of_chaos():
    r, mc, diss, eff = capacity_cost_sweep(RADII, n=100)
    assert 0.85 <= r[int(np.argmax(mc))] <= 1.2


def test_dissipation_increases_with_radius():
    r, mc, diss, eff = capacity_cost_sweep(RADII, n=100)
    assert diss[-1] > diss[0]            # more chaotic -> more churn


def test_capacity_cost_tradeoff():
    # honest finding: peak capacity (at the edge) costs MORE than operating at low ρ,
    # and efficiency (MC/cost) is higher at low ρ -> the edge maximises capability,
    # not efficiency.
    r, mc, diss, eff = capacity_cost_sweep(RADII, n=100)
    i_peak = int(np.argmax(mc))
    assert diss[i_peak] > diss[0]        # you pay more for peak capacity
    assert eff[0] > eff[i_peak]          # low ρ is cheaper-per-bit (but forgetful)


def test_landauer_floor_scales_with_bits():
    assert landauer_floor_joules(0.0) == 0.0
    assert abs(landauer_floor_joules(10.0) - 10.0 * landauer_floor_joules(1.0)) < 1e-30
    assert landauer_floor_joules(1.0, 300.0) > 0.0
