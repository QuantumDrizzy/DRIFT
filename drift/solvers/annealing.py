"""
drift.solvers.annealing — simulated annealing (Metropolis single-spin flips).

This *is* the physics computing. The system starts hot and disordered, and a cooling
schedule lets it relax toward low energy: at high T it explores freely (accepting
uphill moves), at low T it settles into a minimum. The recorded energy trajectory is
the observable that makes "matter computing" visible — you watch it drift downhill.

It is also, literally, a Boltzmann-machine sampler with a temperature ramp (see
CONCEPTS.md): sampling exp(-E/T) and cooling T → 0.
"""

from __future__ import annotations

import numpy as np

from ..ising import IsingModel


def geometric_schedule(n_sweeps: int, T0: float, T1: float) -> np.ndarray:
    """Geometric cooling from T0 to T1 over n_sweeps (one entry per sweep)."""
    if n_sweeps <= 1:
        return np.array([T0], dtype=np.float64)
    return T0 * (T1 / T0) ** (np.arange(n_sweeps) / (n_sweeps - 1))


def simulated_annealing(
    model: IsingModel,
    *,
    n_sweeps: int = 1000,
    T0: float = 5.0,
    T1: float = 1e-2,
    seed: int = 0,
    s0: np.ndarray | None = None,
):
    """Relax `model` toward its ground state by simulated annealing.

    One *sweep* attempts n single-spin flips (n = number of spins). A flip is accepted
    if it lowers the energy, or, with probability exp(-ΔE/T), if it raises it.

    Returns (best_s, best_E, traj, Ts):
        best_s   lowest-energy configuration seen, shape (n,)
        best_E   its energy
        traj     energy at the end of each sweep, shape (n_sweeps,)
        Ts       temperature schedule, shape (n_sweeps,)
    """
    rng = np.random.default_rng(seed)
    n = model.n

    if s0 is None:
        s = (rng.integers(0, 2, n) * 2 - 1).astype(np.float64)  # random ±1
    else:
        s = np.asarray(s0, dtype=np.float64).copy()

    Ts = geometric_schedule(n_sweeps, T0, T1)
    traj = np.empty(n_sweeps, dtype=np.float64)

    E = model.energy(s)
    best_s, best_E = s.copy(), E

    for t in range(n_sweeps):
        T = Ts[t]
        inv_T = 1.0 / max(T, 1e-12)
        for _ in range(n):
            i = int(rng.integers(n))
            dE = model.delta_energy_flip(s, i)
            if dE <= 0.0 or rng.random() < np.exp(-dE * inv_T):
                s[i] = -s[i]
                E += dE
        traj[t] = E
        if E < best_E:
            best_E = E
            best_s = s.copy()

    return best_s, best_E, traj, Ts
