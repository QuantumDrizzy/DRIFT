"""The maximal Lyapunov exponent — the *rigorous* edge of chaos.

DRIFT's whole thesis is that computation lives at the edge of chaos. So far the
edge has been located by proxy: the spectral radius rho ≈ 1, where memory
capacity peaks (`compute_cost.py`). But the textbook definition of the edge is
dynamical, not spectral: the **maximal Lyapunov exponent** lambda, the average
exponential rate at which two infinitesimally close states diverge under the
reservoir dynamics.

    lambda < 0  : perturbations die  -> ordered, echo-state property holds
    lambda > 0  : perturbations grow -> chaotic, ESP lost (no fading memory)
    lambda ≈ 0  : the edge of chaos

We measure lambda with the standard two-trajectory Benettin algorithm: run two
copies of the reservoir under the *same* input stream, starting a distance d0
apart, and after each update record how the gap grew before renormalising it
back to d0.

The honest finding (and the reason this is worth measuring rather than assuming):
the spectral proxy rho = 1 and the true dynamical edge do **not** coincide. In a
driven tanh reservoir the input pushes units into the compressive |tanh'| < 1
regime, so the dynamics stay contracting past rho = 1 — measured here, lambda
only crosses zero near rho ≈ 1.35. Memory capacity peaks earlier still, around
rho ≈ 1.1: best computation sits in the *ordered* regime approaching the edge,
not on it. So rho = 1 is a useful lower bound, not the edge itself.

    python -m drift.lyapunov
"""

from __future__ import annotations

import numpy as np

from drift.reservoir import IsingReservoir, memory_capacity


def _step(res: IsingReservoir, state: np.ndarray, ut: float) -> np.ndarray:
    """One reservoir update (mirrors IsingReservoir.run), pure in `state`."""
    pre = res.W @ state + res.W_in * ut
    return (1.0 - res.leak) * state + res.leak * np.tanh(pre)


def max_lyapunov(reservoir: IsingReservoir, n_steps: int = 2000, d0: float = 1e-8,
                 washout: int = 200, seed: int = 0) -> float:
    """Maximal Lyapunov exponent per update step, via two-trajectory Benettin.

    Positive -> chaotic, negative -> contracting (fading memory). Driven by an
    i.i.d. input so it measures the exponent of the *input-driven* dynamics."""
    rng = np.random.default_rng(seed)
    u = rng.uniform(-1.0, 1.0, washout + n_steps)

    # warm up onto the driven attractor
    x = np.zeros(reservoir.n)
    for t in range(washout):
        x = _step(reservoir, x, u[t])

    # second trajectory, started d0 away in a random direction
    v = rng.standard_normal(reservoir.n)
    v /= np.linalg.norm(v)
    y = x + d0 * v

    log_growth = 0.0
    for t in range(washout, washout + n_steps):
        ut = u[t]
        x = _step(reservoir, x, ut)
        y = _step(reservoir, y, ut)
        diff = y - x
        d1 = np.linalg.norm(diff)
        if d1 == 0.0:
            continue
        log_growth += np.log(d1 / d0)
        y = x + (d0 / d1) * diff          # renormalise back to d0
    return float(log_growth / n_steps)


def lyapunov_sweep(radii, n: int = 100, leak: float = 0.3, seed: int = 0):
    """(radii, lambdas) — the exponent across a spectral-radius sweep."""
    radii = np.asarray(radii, dtype=float)
    lams = np.empty(len(radii))
    for i, r in enumerate(radii):
        res = IsingReservoir(n=n, spectral_radius=float(r), leak=leak, seed=seed)
        lams[i] = max_lyapunov(res)
    return radii, lams


def edge_radius(radii, lambdas) -> float:
    """Linear-interpolated spectral radius where lambda crosses zero (the edge)."""
    radii, lambdas = np.asarray(radii), np.asarray(lambdas)
    sign = np.signbit(lambdas)
    cross = np.where(sign[:-1] != sign[1:])[0]
    if len(cross) == 0:
        return float("nan")
    i = cross[0]
    x0, x1, y0, y1 = radii[i], radii[i + 1], lambdas[i], lambdas[i + 1]
    return float(x0 - y0 * (x1 - x0) / (y1 - y0))


def _main() -> None:
    radii = np.linspace(0.4, 1.8, 15)
    r, lam = lyapunov_sweep(radii, n=100)
    print("  rho    lambda")
    for ri, li in zip(r, lam):
        flag = "ordered" if li < -0.005 else ("chaotic" if li > 0.005 else "EDGE")
        print(f"  {ri:4.2f}  {li:+.4f}   {flag}")
    print(f"lambda=0 crossing at rho ~ {edge_radius(r, lam):.3f}  (proxy says rho~1)")

    # does memory capacity peak at the same place?
    best_r, best_mc = max(
        ((ri, memory_capacity(IsingReservoir(n=100, spectral_radius=float(ri), leak=0.3))[0])
         for ri in radii), key=lambda t: t[1])
    print(f"memory capacity peaks at rho ~ {best_r:.3f}  (MC = {best_mc:.1f})")


if __name__ == "__main__":
    _main()
