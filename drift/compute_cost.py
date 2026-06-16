"""The energy price of computation — the capacity-cost tradeoff at the edge of chaos.

DRIFT's Phase 8 showed the reservoir's *memory capacity* peaks at the edge of chaos
(spectral radius ρ ≈ 1). Computation is never free, though: a substrate that holds
and overwrites information must dissipate. Put both on the same knob ρ and measure:

  - capacity : Jaeger memory capacity MC(ρ) [bits],
  - cost     : the recurrent-drive magnitude ⟨‖W·x‖⟩ the substrate must sustain.

The measured, robust result (and an honest correction of a tempting story):
**capacity peaks at the edge (ρ ≈ 1), but the cost rises monotonically with ρ.**
So peak capability sits on a *rising* cost curve — the edge of chaos maximises
*capacity*, NOT efficiency. Efficiency (MC / cost) actually favours low ρ: cheap
but forgetful. There is a genuine capacity-cost tradeoff, and the most capable
operating point is not the cheapest. (An earlier hope that "efficiency peaks at the
edge" did not survive the data — the state-churn proxy that suggested it was an
artefact of tanh saturation.)

The fundamental floor underneath is Landauer's: each bit processed costs
≥ k_B T ln2 (`landauer_floor_joules`), the same quantity that bounds the Maxwell
demon.
"""

from __future__ import annotations

import numpy as np

from drift.reservoir import IsingReservoir, memory_capacity

K_B = 1.380649e-23
LN2 = float(np.log(2.0))


def dissipation_proxy(reservoir, n_steps: int = 1500, washout: int = 100, seed: int = 3) -> float:
    """Mean recurrent-drive magnitude ⟨‖W·x‖⟩ — the feedback 'effort' the substrate
    must sustain each step (a cost proxy). Chosen over the raw state churn ⟨‖Δx‖⟩
    because that one is confounded by tanh saturation at high ρ (the state pins to
    ±1 and Δx collapses), whereas the recurrent drive grows monotonically with ρ.
    """
    rng = np.random.default_rng(seed)
    u = rng.uniform(-1.0, 1.0, n_steps)
    state = np.zeros(reservoir.n)
    drive = []
    for t, ut in enumerate(u):
        rec = reservoir.W @ state
        state = (1.0 - reservoir.leak) * state + reservoir.leak * np.tanh(rec + reservoir.W_in * ut)
        if t >= washout:
            drive.append(float(np.linalg.norm(rec)))
    return float(np.mean(drive))


def capacity_cost_sweep(radii, n: int = 120, leak: float = 0.3, seed: int = 0):
    """Return (radii, MC, dissipation, efficiency) across the spectral-radius sweep."""
    mc, diss = [], []
    for r in radii:
        res = IsingReservoir(n=n, spectral_radius=float(r), leak=leak, seed=seed)
        mc_total, _ = memory_capacity(res, n_train=1200)
        mc.append(mc_total)
        diss.append(dissipation_proxy(res))
    mc = np.asarray(mc)
    diss = np.asarray(diss)
    eff = mc / np.maximum(diss, 1e-9)
    return np.asarray(radii, dtype=float), mc, diss, eff


def landauer_floor_joules(mc_bits: float, temperature_k: float = 300.0) -> float:
    """Fundamental floor: each bit of capacity costs ≥ k_B T ln2 to process/erase."""
    return mc_bits * K_B * temperature_k * LN2
