# ADR-0002: Hardware Ising readout — physical LED-matrix visualization on the Raspberry Pi

**Status:** Proposed
**Date:** 2026-06-19
**Deciders:** Antonio (QuantumDrizzy)

## Context

DRIFT is sim-only today: optimization, self-assembly and Hopfield memory as ground states of one
Ising Hamiltonian (Python), benchmarked against the Landauer limit. The hardware era + a personal
Raspberry Pi (see `project-groundwatch` / GROUNDWATCH `ADR-0001`) opens a tangible output: **drive a
physical LED matrix from the Pi to show the Ising lattice relaxing to its ground state in real
time** — frustration, domain walls, the anneal as T→0. Matter-as-compute, made physical and
visible. This is the "squeeze the Ising on hardware" idea: a hardware *readout* layer over the
existing DRIFT engine, not new physics.

## Decision

Build a Pi-driven LED-matrix readout of DRIFT's annealing: consume a QUBO/Ising (from DRIFT or
temp0r), run the existing SA on the Pi, and **stream the live spin states to an LED grid** as the
system relaxes. DRIFT's core stays untouched; add a thin edge "readout" adapter.

## What to touch (profiling)
1. A small **edge output module** (separate from DRIFT's core): DRIFT spins → LED pixels via the Pi's
   SPI/GPIO. Hardware options: a WS2812/NeoPixel RGB matrix (e.g. 16×16) or an HUB75 LED panel.
2. Reuse DRIFT's SA + [temp0r] annealing as-is; map each spin → a pixel, color by state / local
   energy, refresh per sweep so the relaxation is visible.
3. (Optional) feed live problems: a webcam/sensor → QUBO → anneal-on-LEDs, tying it to TESSERA's
   vision face on the same Pi.

## Honest framing `[KNOWN_LIMIT]`
- This is **a visualization of classical simulated annealing on the Pi**, displayed on real LEDs —
  **NOT** a quantum annealer and **NOT** a physical Ising machine. The wow is real without
  overclaiming. Frame it exactly so ("watch a simulated Ising relax on real LEDs"). The firewall is
  the same discipline as NIGHTWATCH/SESHAT: say what it is.

## Consequences
- **Easier:** a striking, honest, demoable hardware artifact (a glowing lattice settling to ground
  state) that documents as a build-in-public Twitter thread — and it's the most "quantum-inspired /
  matter-as-compute" piece in the ecosystem, made tangible.
- **Shared substrate:** the same Ising/QUBO thesis as TESSERA (vision), LPLACEXE (`demiurge` CA),
  SESHAT and temp0r. DRIFT is the substrate; this is its physical face.
- **Watch:** DRIFT's heavier reservoir/kernel-rank experiments are CPU/GPU work, not LED work — keep
  the readout adapter thin and separate from the science core.

## Action Items
1. [ ] Pick LED hardware (matrix type + size) and the Pi driver (SPI/GPIO library).
2. [ ] Write the spins→pixels readout adapter (outside DRIFT's core).
3. [ ] Live anneal visualization (refresh per sweep); optional webcam/sensor → QUBO feed.
4. [ ] Record the build-in-public thread.
