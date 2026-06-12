"""drift.builders — the loads. Each builder turns a problem into a particular (J, h)
that the engine then minimizes. The engine never changes; only the Hamiltonian does.

Phase 2 ships the optimization face (QUBO / MaxCut). Hopfield, tiles and crystals
follow in later phases.
"""

from .qubo import qubo_to_ising, maxcut_ising, cut_value, random_graph

__all__ = ["qubo_to_ising", "maxcut_ising", "cut_value", "random_graph"]
