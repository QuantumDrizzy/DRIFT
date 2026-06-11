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

### Phase 2 — Face ①: Optimization (QUBO) ⬜
- **Understand:** *optimization = ground state.* A combinatorial problem solved by physics.
- **Build:** `qubo` builder (`Q → J, h`); canonical example **MaxCut** (or number
  partitioning).
- **Measure:** does annealing reach the exact optimum? how far, how often?
- **Figure:** the graph + the partition emerging as the system cools.

### Phase 3 — Tensor-network solver + χ (the thermometer) ⬜
- **Understand:** *how much* a problem computes. Add a tensor-network ground-state solver
  and read the **bond dimension χ** it needs — easy problems stay low-χ, hard ones explode.
- **Build:** MPS/DMRG (or exact contraction) ground state + χ measurement + entanglement
  entropy.
- **Measure:** χ across easy vs. hard instances → χ as compute-density.
- **Figure:** χ (and entropy) vs. problem difficulty. *This is the Blaze lesson, applied.*

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
