"""Validate that logic gates are the ground states of QUBO penalties (universality)."""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drift.logic import (  # noqa: E402
    NAND_TRUTH,
    TRUTH,
    and_energy,
    ground_states,
    nand_via_composition,
    not_energy,
    or_energy,
)


def test_gates_are_ground_states():
    assert ground_states(and_energy, 3) == TRUTH["AND"]
    assert ground_states(or_energy, 3) == TRUTH["OR"]
    assert ground_states(not_energy, 2) == TRUTH["NOT"]


def test_invalid_rows_are_penalised():
    # every non-truth-table row of AND must have strictly positive energy
    for x, y, z in itertools.product((0, 1), repeat=3):
        e = and_energy(x, y, z)
        if (x, y, z) in TRUTH["AND"]:
            assert e == 0
        else:
            assert e > 0


def test_nand_by_composition_is_universal():
    # NAND = NOT . AND through an internal wire -> functionally complete
    assert nand_via_composition() == NAND_TRUTH
