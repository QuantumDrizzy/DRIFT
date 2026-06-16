"""Boolean logic from the Ising/QUBO substrate — computational universality.

A logic gate can be written as a QUBO penalty whose **ground states are exactly the
gate's truth table**: the energy is 0 on every valid (input, output) row and > 0 on
every invalid one. So finding the ground state of the penalty *is* evaluating the
gate — the same energy-minimisation DRIFT uses everywhere. Standard penalties
(binary x, y, z ∈ {0,1}):

    AND  z = x ∧ y :  H = xy − 2xz − 2yz + 3z
    OR   z = x ∨ y :  H = xy − 2xz − 2yz + x + y + z
    NOT  z = ¬x    :  H = 2xz − x − z + 1

Gates compose by sharing variables and **adding** their penalties: wire the output
of one into the input of the next and the combined ground states implement the
composed function (demonstrated here: NAND = NOT∘AND via an internal wire). Since
{AND, OR, NOT} (indeed NAND alone) is functionally complete, the Ising substrate is
a **universal Boolean computer** — matter computing logic by relaxing to a minimum.
"""

from __future__ import annotations

import itertools


def and_energy(x, y, z):
    return x * y - 2 * x * z - 2 * y * z + 3 * z


def or_energy(x, y, z):
    return x * y - 2 * x * z - 2 * y * z + x + y + z


def not_energy(x, z):
    return 2 * x * z - x - z + 1


def ground_states(energy_fn, nvars: int) -> frozenset:
    """All bit assignments that minimise the penalty (the computed truth table)."""
    configs = list(itertools.product((0, 1), repeat=nvars))
    energies = [energy_fn(*c) for c in configs]
    emin = min(energies)
    return frozenset(c for c, e in zip(configs, energies) if abs(e - emin) < 1e-9)


# reference truth tables (x, y, z) / (x, z)
TRUTH = {
    "AND": frozenset((x, y, x & y) for x in (0, 1) for y in (0, 1)),
    "OR": frozenset((x, y, x | y) for x in (0, 1) for y in (0, 1)),
    "NOT": frozenset((x, 1 - x) for x in (0, 1)),
}


def nand_via_composition() -> frozenset:
    """Compose NAND = NOT∘AND through an internal wire w: H = H_AND(x,y,w)+H_NOT(w,z).

    Returns the (x, y, z) ground states with the internal w marginalised out.
    """
    energy = lambda x, y, w, z: and_energy(x, y, w) + not_energy(w, z)  # noqa: E731
    gs4 = ground_states(energy, 4)
    return frozenset((x, y, z) for (x, y, w, z) in gs4)


NAND_TRUTH = frozenset((x, y, 1 - (x & y)) for x in (0, 1) for y in (0, 1))
