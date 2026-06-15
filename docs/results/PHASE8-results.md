# Phase 8 — The dynamical (reservoir) face

**Understood:** *matter computes in time, and you can measure how much.* The first
seven faces read a ground state (static computation). This one drives the Ising
substrate as a physical **reservoir** and quantifies its computation — the
rigorous, measurable core of the computronium idea.

**Built:** `drift/reservoir.py` — `IsingReservoir`, a leaky-integrator reservoir
(`x ← (1−α)x + α·tanh(W·x + W_in·u)`), built either from a random sparse coupling
or from a real `drift.ising.IsingModel` (`IsingReservoir.from_ising`): the same
Ising substrate that solves ground-state problems, now run in time. Metrics:
Jaeger `memory_capacity` (+ forgetting curve) and `separation`. The reservoir's
spectral radius is set via the **Spectra** spine — DRIFT is a Spectra consumer.

**Validated:** `tests/test_reservoir.py` (5/5, DRIFT's first automated tests) —
memory capacity within the N bound and substantial, memory fades with delay,
separation is 0 for identical inputs and positive for distinct ones, the spectral
radius matches the dense reference, and building from a real `IsingModel` works.

**Measured (N=200, leak 0.3):** total **MC = 43.5**, and MC **peaks at spectral
radius ρ ≈ 1.0 — the edge of chaos**, exactly the expected reservoir-computing
signature. Honest note: MC < N because the `tanh` nonlinearity and leak trade
*linear* memory (what MC measures) for nonlinear computation.

**Figure:** `figures/phase8_reservoir.png` — (a) the forgetting curve `MC_k` vs
delay; (b) total memory capacity vs spectral radius, peaking at the edge of chaos.
