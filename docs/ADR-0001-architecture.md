# ADR-0001: DRIFT Architecture — one engine, pluggable loads

**Status:** Accepted
**Date:** 2026-06-10
**Deciders:** Antonio

## Context

DRIFT explores a single idea — *matter computes by minimizing energy* — across four
domains: optimization (QUBO), self-assembly (tiles), self-replication (crystals), and
neural memory (Hopfield). The goal is **understanding, not demonstration**: we want to *see
and measure* the process (how much it computes, how it relaxes, what emerges), not to beat a
benchmark or publish a result.

The risk to avoid: building four separate toys that drift apart, or chasing performance/SOTA
when the actual goal is observability and comprehension.

## Decision

**One engine, pluggable loads.** The four faces are NOT separate projects — they are one
Ising/tensor engine fed by different *builders* (Hamiltonian generators). The engine owns
~90% of the code; a builder is a small function that fills `J_ij` and `h_i`.

```
                 ┌─────────────── ENGINE (shared) ───────────────┐
  builders  ──►  │  IsingModel(J, h)                              │
  (QUBO,         │  solvers:  simulated annealing · exact/Lanczos │  ──► observables
   tiles,        │            tensor-network (MPS/DMRG)           │      (χ, energy,
   crystal,      │  metrics:  energy trajectory · χ · entropy ·   │       trajectory,
   Hopfield)     │            Landauer cost · magnetization       │       ground state)
                 │  viz:      landscape · relaxation · emergence  │
                 └───────────────────────────────────────────────┘
```

### Why Ising is the right unifying core

Every face reduces to a ground-state search of `H = -Σ J_ij s_i s_j - Σ h_i s_i`:
- **QUBO → Ising** is a trivial change of variable (`x∈{0,1}` ↔ `s∈{±1}`).
- **Hopfield** *is* an Ising model (synaptic weights = `J`, memories = energy minima).
- **Self-assembly / self-replication** map tile-affinity / periodicity rules onto `J, h`.

This is not a metaphor — it is the same mathematics. The unification is the point.

## Options considered

### Language: Python-first (chosen) vs. Rust-first
| | Python-first | Rust-first |
|---|---|---|
| Iteration / exploration speed | **fast** (notebooks, NumPy, matplotlib) | slow |
| Visualization (the whole point) | **trivial** (matplotlib/plotly) | painful |
| Small-system rigor (exact diag) | fine (SciPy/Lanczos) | fine |
| Scaling to large χ / sizes | slow | **fast** |
| Fits the goal (*understand*) | **yes** | premature |

**Chosen: Python-first.** The goal is comprehension and visuals; exact methods on small
systems (where understanding starts) are perfectly fast in NumPy/SciPy. A **Rust port of the
hot-path solver** is deferred until a phase actually needs scale — the same Python-spec →
Rust-core pattern proven in Blaze. Right tool per domain (Python for exploration/quantum/ML;
Rust/CUDA when it becomes the hot path), not all-one-language.

### Topology: one engine + builders (chosen) vs. four standalone modules
One engine wins because it forces the comparison that *is* the insight: the same probes
(χ, energy, relaxation) across all four faces. Four standalone toys would make
"how much does a memory compute vs. an assembly?" impossible to ask cleanly.

## Consequences

- **Easier:** adding a fifth face is a new builder (~50 lines), not a new project.
- **Easier:** cross-face comparison is native (shared metrics).
- **Harder / deferred:** large-scale systems wait for the Rust port; early phases cap system
  size so exact ground states stay reachable (the honest baseline).
- **Discipline:** observability over performance. The engine is instrumented first,
  optimized later. Every phase ships code + a figure + a `docs/results/` note.

## Honesty contract (inherited project-wide)

Established mathematics (Ising/QUBO/Hopfield/tensor networks) is stated as fact. Anything
touching consciousness, real nanotech, or grey-goo is tagged speculation in
[`CONCEPTS.md`](CONCEPTS.md) and never presented as a result. χ and Landauer numbers are
measured, with the method and system size stated — never a bare figure.
