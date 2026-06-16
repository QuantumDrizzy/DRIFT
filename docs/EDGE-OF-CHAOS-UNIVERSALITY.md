# The edge of chaos is not special to DRIFT — it is universal

DRIFT's Phase 8 measured a hard fact: the Ising reservoir's **memory capacity
peaks at the edge of chaos** (spectral radius ≈ 1, the order/disorder boundary).
The natural question is whether that boundary is something about *this* substrate
or something general.

A companion experiment in **AETHER** (`research/criticality/universal.py`,
`figures/universal_criticality.png`) answers it: three unrelated systems —

- the **Ising** model (the same computronium substrate as here): magnetisation vs
  temperature,
- **Vicsek active matter**: flocking order vs angular noise,
- **programmable matter**: target-coverage of a self-reconfiguring swarm vs a fixed
  disorder temperature,

each show the *same* order→disorder transition. Normalise every control knob by its
own transition point and the three curves collapse onto one shape that crosses
order = ½ at the critical point. **Criticality is substrate-independent.**

So DRIFT's result is one instance of a general law: a physical substrate computes
best — maximum memory capacity, maximum separation, maximum responsiveness — right
at the critical boundary between order and chaos, whatever the substrate is made
of. That is the through-line of the computronium / daemons line: information,
energy, matter and computation meet at the edge of chaos, and the edge is the same
edge everywhere.

(See also: AETHER `research/daemons` (Maxwell's demon: information → work),
`research/active_matter`, `research/programmable_matter`. The archived HYLE
note `the_triangle` ties the information↔energy↔matter side together.)
