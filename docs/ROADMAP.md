# DRIFT — Roadmap

Each phase has an **understanding goal** (what you'll be able to *see/measure* afterward)
and a **deliverable** (code + at least one figure + a `docs/results/PHASE{N}-results.md`
note). Phases are incremental: every one builds on the shared engine. No phase is about
proving anything — each one makes a piece of the process *observable*.

> Legend: ⬜ not started · 🔄 doing · ✅ done

---

### Phase 0 — Scaffolding ✅
- **Understand:** the shape of the whole thing before any code.
- **Deliverable:** README, ADR-0001, this roadmap, CONCEPTS glossary.

### Phase 1 — The engine + observability ✅  *(see [results](results/PHASE1-results.md))*
- **Understood:** *matter computes.* The relaxation figure shows a spin system exploring
  hot, then freezing into its exact ground state as it cools.
- **Built:** `IsingModel(J, h)`; solvers = **simulated annealing** + **exact** brute force;
  metrics (energy, magnetization, Landauer floor); dark-palette viz.
- **Validated:** 2D ferromagnet `L=4` → exact = annealing = `-32` (`= -2nJ`), SA reaches it.
- **Figures:** `figures/phase1_{relaxation,groundstate,landscape}.png`.

### Phase 2 — Face ①: Optimization (QUBO) ✅  *(see [results](results/PHASE2-results.md))*
- **Understood:** *optimization = ground state.* MaxCut as a purely antiferromagnetic
  Ising; the maximum cut is the lowest-energy spin configuration.
- **Built:** `qubo` builder (`qubo_to_ising`, `maxcut_ising`, `cut_value`, `random_graph`)
  + `plot_graph_cut`.
- **Validated:** `G(n=14, p=0.5)`, 43 edges → exact = annealing = **31-edge cut** (E = -19).
- **Figures:** `figures/phase2_{relaxation,maxcut}.png`.

### Phase 3 — Quantum ground state + χ (the thermometer) ✅  *(see [results](results/PHASE3-results.md))*
- **Understood:** *how much* a state computes. The transverse-field Ising chain's ground
  state, with χ = the bond dimension a tensor network needs. χ stays small in the ordered
  (cat) and disordered (polarized) phases and **peaks at the quantum phase transition**.
- **Built:** `drift/quantum.py` — sparse TFIM, Lanczos ground state, entanglement entropy
  (SVD), Blaze-style `effective_chi`; `plot_chi_sweep`.
- **Validated:** `n=14` chain; χ: 4 (cat) → 6 (critical) → 3 (polarized); peak at Γ≈0.77
  (Γ_c = 1, finite-size shift, stated honestly).
- **Figure:** `figures/phase3_chi.png`.  *The Blaze lesson, applied as a probe.*

### Phase 4 — Face ④: Neural memory (Hopfield) ⬜
- **Understand:** *memory = the self-assembly of an attractor.* The neuroscience face.
- **Build:** `hopfield` builder (patterns → Hebbian `J`); store patterns, recall from noise.
- **Measure:** capacity (~0.138 N), basins of attraction, χ of a stored memory.
- **Figure:** a noisy image relaxing back to a clean stored memory, frame by frame.

### Phase 5 — Face ②: Self-assembly (aTAM / tiles) ⬜
- **Understand:** *constructive nanotech.* A structure assembling itself by minimizing
  affinity energy.
- **Build:** `tiles` builder (tile glues → `J, h`); the abstract Tile Assembly Model.
- **Figure:** a target shape assembling as the system settles.

### Phase 6 — Face ③: Self-replication ⬜
- **Understand:** *grey goo, contained.* Replication as crystallization / periodic ground
  state.
- **Build:** `crystal` builder (periodicity-favoring couplings).
- **Figure:** a pattern replicating across the lattice as it relaxes.

### Phase 7 — The microscope (synthesis) ⬜
- **Understand:** the payoff — compare all four faces under the *same* probes. Does a memory
  compute more than an assembly? Where does each sit against the Landauer / Lloyd limits?
- **Build:** a unified comparison harness + the "cosmic roofline" (real hardware vs. ultimate
  physical limits).
- **Figure:** the four faces on one axis of compute-density (χ) and physical cost.

---

## Out of scope (on purpose)
- Beating quantum-annealing or DMRG SOTA — DRIFT is a microscope, not a competitor.
- Claims about consciousness, real nanotech, or imminent grey goo — see CONCEPTS honesty tags.
- Large-scale GPU solving — deferred to a Rust/CUDA port if and when a phase needs it.
