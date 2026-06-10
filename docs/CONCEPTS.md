# DRIFT — Concepts (glossary, with honesty tags)

Every entry is tagged: **[ESTABLISHED]** = solid, textbook science · **[ACTIVE]** = real
research, debated details · **[SPECULATIVE]** = interesting math, not established truth.
DRIFT builds only on [ESTABLISHED] and [ACTIVE]; [SPECULATIVE] entries are here because
they motivate the questions, not because we treat them as answers.

---

## The core object

### Ising model **[ESTABLISHED]**
`H = -Σ J_ij s_i s_j - Σ h_i s_i`, with spins `s_i ∈ {±1}`. Coupling `J_ij` sets how strongly
two spins want to align; field `h_i` biases individual spins. The system's **ground state**
is the spin configuration of lowest energy. Originally a model of magnetism (1920s); now the
universal language of "many coupled binary variables minimizing a cost."

### QUBO ≡ Ising **[ESTABLISHED]**
Quadratic Unconstrained Binary Optimization: minimize `x^T Q x` over `x ∈ {0,1}^n`. The map
`x = (s+1)/2` turns any QUBO into an Ising Hamiltonian and back. So **every combinatorial
optimization problem expressible as QUBO is a ground-state search.** (MaxCut, number
partitioning, graph coloring, TSP, ... all reduce to this.)

### Ground state as computation **[ESTABLISHED]**
A physical system relaxing to its lowest energy is literally minimizing a cost function. If
you encode a problem in `J, h`, the physics *solves* it. This is the principle behind
**quantum annealing** (D-Wave) and **Ising machines** (coherent / oscillator-based hardware
that minimizes a Hamiltonian physically, without a von Neumann CPU).

---

## Measuring "how much it computes"

### Bond dimension χ / entanglement **[ESTABLISHED]**
A tensor network (MPS) represents a quantum state with cores linked by bonds of dimension χ.
χ bounds how much **entanglement** — and so how much **information** — the state holds. Low-χ
states are cheap to represent (little "computation"); states needing large χ are
information-dense. In DRIFT, **χ is the thermometer**: the χ a ground state needs measures
how much computation lives in it. (This is the lesson from Blaze: χ-truncation *is*
information-budget management.)

### Landauer limit **[ESTABLISHED]**
Erasing one bit irreversibly costs at least `kT·ln2` of energy (≈ 2.9 zJ at 300 K, Landauer
1961). A hard floor on irreversible computation. **Reversible** computation can in principle
approach zero cost — which is why reversible and quantum logic matter.

### Margolus-Levitin / Bremermann / Lloyd limits **[ESTABLISHED]**
Ultimate physical limits on computation: a system of energy `E` does at most `2E/πℏ`
operations per second (Margolus-Levitin); ~`1.36×10⁵⁰` bits/s per kg (Bremermann); Lloyd's
"ultimate laptop" (1 kg, 1 L) tops out at ~`5×10⁵⁰` ops/s and ~`10³¹` bits (Nature, 2000).
The maximal-density computer is, formally, a black hole (Bekenstein bound). DRIFT's "cosmic
roofline" compares real hardware to these.

---

## The four faces

### Neural memory — Hopfield network **[ESTABLISHED]**
A Hopfield network *is* an Ising model: neurons = spins, synaptic weights = `J_ij`, stored
**memories = energy minima (attractors)**. Recalling a memory from a noisy cue is relaxing to
the nearest ground state. Capacity ≈ `0.138 N` patterns for `N` neurons. Hopfield shared the
**2024 Nobel Prize in Physics** (with Hinton) for this line of work.

### Boltzmann machine **[ESTABLISHED]**
A stochastic Ising model at finite temperature (Hinton & Sejnowski, 1985) — a generative
neural network. DRIFT's annealing solver *is* a Boltzmann machine sampler in disguise.

### Self-assembly — abstract Tile Assembly Model (aTAM) **[ESTABLISHED / ACTIVE]**
Winfree's model of molecular self-assembly: tiles bind by matching "glues" of given
strength; structures grow by minimizing binding energy. aTAM is **Turing-complete**, and is
the theoretical basis of real DNA-origami nanotechnology. The *constructive* counterpart to
grey goo — assembly, not consumption.

### Self-replication — von Neumann replicators **[ESTABLISHED (theory)]**
Von Neumann proved self-reproducing automata are possible (universal constructor, 1940s-50s)
before DNA was understood. Replication as a periodic/crystalline ground state is a contained,
measurable instance of the idea.

---

## The sci-fi vocabulary (what motivated this, honestly tagged)

### Computronium **[SPECULATIVE]**
Hypothetical matter arranged for maximal computation. The *fabrication* is fiction; the
**limits** it gestures at (above) are rigorous. We use the concept to ask "how close is real
matter to the physical limit of computation?" — a measurable question.

### Grey goo **[SPECULATIVE / mostly myth]**
Drexler's runaway self-replicating nanobots (1986). Drexler himself walked it back (2004):
self-replication is thermodynamically expensive (energy, heat dissipation, specific
feedstock). Life is the regulated proof. DRIFT studies the *real* core (self-assembly /
replication as energy minimization), not the apocalypse.

### Drift-diffusion model (DDM) **[ESTABLISHED]**
The canonical model of decision-making in computational neuroscience: evidence accumulates
("drifts") until it crosses a threshold. One of the three meanings behind the project's name,
and a future face worth exploring (decision as a first-passage process).

### Criticality / "edge of chaos" **[ACTIVE]**
The brain appears to operate near a phase transition (neuronal avalanches, power laws) — an
Ising near `T_c`. Real, measurable, and debated. Connects directly to phase-transition work
(see EIGEN).

### Free Energy Principle **[ACTIVE / debated]**
Friston: the brain minimizes variational "free energy" (surprise) ≈ Bayesian inference ≈
energy minimization again. Mathematically serious, empirically contested.

### Integrated Information Theory (Φ) **[SPECULATIVE]**
Tononi: Φ measures "integrated information," proposed as a correlate of consciousness. A real
measure of *how much a system integrates/computes* — conceptually a cousin of χ — but its
identification with consciousness is unproven and heavily debated. We borrow the *math of
integration*, not the metaphysics.

---

## References (starting points)
- R. Landauer, *Irreversibility and heat generation in the computing process* (1961).
- S. Lloyd, *Ultimate physical limits to computation*, Nature 406 (2000); *Programming the
  Universe* (2006).
- J. Hopfield, *Neural networks and physical systems with emergent collective computational
  abilities*, PNAS (1982).
- E. Winfree, *Algorithmic Self-Assembly of DNA* (PhD thesis, 1998).
- K. E. Drexler, *Engines of Creation* (1986); Phoenix & Drexler, *Safe exponential
  manufacturing* (2004).
