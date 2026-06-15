"""Phase 8 — the dynamical (reservoir) face: matter that computes *in time*.

The first seven faces are ground-state computation (static). This one uses the
**dynamics** of an Ising-style coupled network as a physical reservoir: drive it
with an input stream, read its state with a linear readout, and *measure how much
it computes* — Jaeger **memory capacity** and a **separation** metric. That makes
the computronium idea quantitative rather than rhetorical.

The reservoir's spectral radius (its edge-of-chaos scaling) is set via the
**Spectra** spine — this module is a Spectra consumer.
"""

from __future__ import annotations

import numpy as np

try:
    from spectra import LinearOperator
    from spectra import spectral_radius as _spectra_radius

    _HAVE_SPECTRA = True
except ImportError:  # graceful fallback to NumPy
    _HAVE_SPECTRA = False


def _radius(w: np.ndarray) -> float:
    """Spectral radius of the (generally non-symmetric) coupling matrix.

    Uses the Spectra spine when available; falls back to dense NumPy otherwise."""
    if _HAVE_SPECTRA:
        return _spectra_radius(LinearOperator.from_dense(w))
    return float(np.max(np.abs(np.linalg.eigvals(w))))


class IsingReservoir:
    """A coupled-spin network run as a leaky-integrator reservoir.

    State update:  x ← (1−α)·x + α·tanh(W·x + W_in·u).  W is a sparse random
    Ising-style coupling rescaled to a target spectral radius.
    """

    def __init__(
        self,
        n: int = 200,
        spectral_radius: float = 0.95,
        leak: float = 0.3,
        input_scale: float = 0.5,
        density: float = 0.1,
        seed: int = 0,
    ) -> None:
        rng = np.random.default_rng(seed)
        w = rng.standard_normal((n, n)) * (rng.random((n, n)) < density)
        rho = _radius(w)
        self.W = w * (spectral_radius / rho) if rho > 0 else w
        self.W_in = rng.uniform(-1.0, 1.0, n) * input_scale
        self.leak = leak
        self.n = n
        self.state = np.zeros(n)

    def run(self, u: np.ndarray, washout: int = 0) -> np.ndarray:
        """Drive with a scalar input series `u`; return states (len(u)−washout, n)."""
        self.state = np.zeros(self.n)
        states = np.empty((len(u), self.n))
        for t, ut in enumerate(u):
            pre = self.W @ self.state + self.W_in * ut
            self.state = (1.0 - self.leak) * self.state + self.leak * np.tanh(pre)
            states[t] = self.state
        return states[washout:]


def memory_capacity(
    reservoir: IsingReservoir,
    max_delay: int | None = None,
    n_train: int = 1700,
    washout: int | None = None,
    ridge: float = 1e-6,
    seed: int = 1,
):
    """Jaeger memory capacity: MC = Σ_k corr²(u(t−k), linear readout of the state).

    Returns (mc_total, curve) where curve[k−1] = MC_k (the forgetting curve).
    Theoretical bound: MC ≤ N (reservoir size).
    """
    n = reservoir.n
    max_delay = max_delay or int(1.5 * n)
    washout = washout if washout is not None else max_delay + 50
    rng = np.random.default_rng(seed)
    u = rng.uniform(-1.0, 1.0, washout + n_train)

    x = reservoir.run(u, washout=washout)  # (n_train, n)
    xb = np.hstack([x, np.ones((x.shape[0], 1))])
    a = xb.T @ xb + ridge * np.eye(xb.shape[1])

    curve = []
    for k in range(1, max_delay + 1):
        target = u[washout - k : washout - k + n_train]
        w = np.linalg.solve(a, xb.T @ target)
        pred = xb @ w
        if np.std(pred) < 1e-12 or np.std(target) < 1e-12:
            mc_k = 0.0
        else:
            mc_k = float(np.corrcoef(pred, target)[0, 1] ** 2)
        curve.append(mc_k)
    return float(np.sum(curve)), np.asarray(curve)


def separation(reservoir: IsingReservoir, eps: float, length: int = 500, washout: int = 100, seed: int = 2) -> float:
    """Mean state distance between two input streams that differ (in their second
    half) by ~eps. eps=0 → 0 (determinism); eps>0 → >0 (distinct inputs separate)."""
    rng = np.random.default_rng(seed)
    u1 = rng.uniform(-1.0, 1.0, length)
    u2 = u1.copy()
    half = length // 2
    u2[half:] = u2[half:] + eps * rng.standard_normal(length - half)
    x1 = reservoir.run(u1, washout=washout)
    x2 = reservoir.run(u2, washout=washout)
    return float(np.mean(np.linalg.norm(x1 - x2, axis=1)))
