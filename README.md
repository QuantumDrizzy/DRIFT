# DRIFT

> *A microscope for physical computation.*

DRIFT is a sandbox for **understanding how matter computes by minimizing energy**. It is
not built to prove a thesis or beat a benchmark — it is built to let you *see and measure*
one deep idea: that optimization, self-assembly, self-replication, and neural memory are
**the same mathematical object** — ground states of an Ising model — read with tensor
networks.

The name: a system *drifts* toward its energy minimum. The word is honest across all three
domains this project lives in — **physics** (drift to equilibrium / the ground state),
**neuroscience** (the drift-diffusion model of decision-making), and **replication**
(genetic drift).

## The thesis (one object, four faces)

A system of spins relaxing to its lowest-energy state **is a physical computer** solving an
optimization problem. Change only *what the Hamiltonian encodes*, and the same engine
becomes four different things:

| Face | The Hamiltonian encodes… | The ground state **is**… | The science |
|------|--------------------------|--------------------------|-------------|
| **Optimization** | an arbitrary QUBO/Ising problem | the optimal solution | combinatorial optimization, quantum annealing |
| **Self-assembly** | tile affinity rules (aTAM) | the assembled structure | molecular nanotech, DNA origami (Winfree) |
| **Self-replication** | couplings favoring periodicity | the replicated pattern | crystallization, von Neumann replicators |
| **Neural memory** | stored patterns (Hebbian) | a recalled memory (attractor) | Hopfield networks (Nobel Physics 2024) |

The brain, the crystal, the nanobot, the optimizer: **all compute by minimizing energy.**
DRIFT makes that visible and measurable under one roof.

## What DRIFT measures (the instrumentation)

Because the goal is *understanding*, the engine is built around observability. For every
face, the same probes:

- **How much it computes** → the **bond dimension χ** a tensor network needs to represent
  the state. χ is entanglement is information density — our thermometer for "how much
  computation lives in this matter" (the lesson learned in [Blaze](../Blaze)).
- **How it processes** → the **relaxation trajectory**: the path the system takes down the
  energy landscape.
- **What emerges** → the **ground state**: solution / structure / pattern / memory.
- **The physical floor** → the **Landauer cost** of the computation, and where real hardware
  sits relative to the ultimate limits (Margolus-Levitin, Lloyd).

## Honesty contract

The mathematics here — Ising ↔ QUBO ↔ Hopfield ↔ tensor networks ↔ optimization — is
**solid and established**. What is speculative is the leap to *"this is consciousness /
real grey goo / imminent nanobots."* DRIFT lives in the solid part and lets you *touch and
measure* the concepts that science fiction exaggerates, **without swallowing the
exaggeration**. Every claim in `docs/` is tagged as established science or as speculation.
See [`docs/CONCEPTS.md`](docs/CONCEPTS.md).

## Structure

```
DRIFT/
├── README.md
├── docs/
│   ├── ADR-0001-architecture.md   architecture decision (engine + builders, Python-first)
│   ├── ROADMAP.md                 phases, each with an "understanding goal" + deliverable
│   ├── CONCEPTS.md                rigorous glossary, science vs. speculation tagged
│   └── results/                   PHASE{N}-results.md + figures (filled as phases land)
├── drift/                         Python core (engine, solvers, builders, metrics, viz)
├── experiments/                   one script per phase
└── figures/
```

## Status

**Phases P0–P8 landed.** The engine, the four ground-state faces, the synthesis,
and now the *dynamical* face:

- P0 — scaffolding · P1 — engine + observability · P2 — optimization (MaxCut) ·
  P3 — quantum ground state + χ thermometer · P4 — Hopfield memory · P5 — Wang-tile
  self-assembly · P6 — crystallization (self-replication) · P7 — the microscope.
- **P8 — the dynamical (reservoir) face** (`drift/reservoir.py`): the Ising
  substrate driven in time as a physical reservoir, with *measurable* compute
  capacity — Jaeger **memory capacity** and a **separation** metric (MC = 43.5 / N=200,
  peaking at spectral radius ρ ≈ 1.0, the edge of chaos — see
  `figures/phase8_reservoir.png`). It can be built from a real `drift.ising.IsingModel`,
  and its spectral radius is set via the **Spectra** spine, so DRIFT is a Spectra
  consumer. Ships with DRIFT's first automated test suite (`tests/test_reservoir.py`, 5/5).

The two synthesis figures sit in `figures/phase7_four_faces.png` (one engine, four faces)
and `figures/phase7_roofline.png` (real systems vs. the Landauer floor). See
[`docs/ROADMAP.md`](docs/ROADMAP.md) and `docs/results/PHASE{1..7}-results.md`.

## Stack

Python-first (NumPy/SciPy + matplotlib for the engine and visuals — fast to iterate and
*see*), with a Rust port of the hot-path solver planned once systems grow past what exact
methods handle. Same Python-spec → Rust-core pattern as Blaze.
