"""
drift.viz — visualization. Dark 'DRIFT' palette, consistent with the iNFAMØUS look.

Every figure is a window onto the process, not a result to publish: you watch the
energy drift down, watch the spins order, see where the ground state sits in the
spectrum. Saved as PNG (Agg backend) so experiments run headless.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# ── palette ───────────────────────────────────────────────────────────────────
BG, PANEL = "#0a0c12", "#0e121c"
CYAN, MAGENTA, AMBER, LIME = "#00e6c8", "#ff46a0", "#ffb446", "#9dff5a"
TEXT, MUTED, GRID = "#c8d6e0", "#7a8796", "#1b2434"
FOOTER = "DRIFT · a microscope for physical computation"


def _style() -> None:
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "axes.edgecolor": GRID, "axes.labelcolor": TEXT, "text.color": TEXT,
        "xtick.color": MUTED, "ytick.color": MUTED, "grid.color": GRID,
        "axes.grid": True, "grid.alpha": 0.5, "grid.linewidth": 0.7,
        "axes.titlecolor": CYAN, "axes.titlesize": 13, "axes.titleweight": "bold",
        "font.size": 11, "font.family": "DejaVu Sans Mono", "figure.dpi": 140,
        "axes.spines.top": False, "axes.spines.right": False,
    })


def _save(fig, out: str | Path) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.text(0.99, 0.01, FOOTER, ha="right", va="bottom", color=MUTED, fontsize=7.2, style="italic")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_relaxation(traj, *, e_ground=None, Ts=None, title="Relaxation", out="figures/relaxation.png"):
    """Energy vs. sweep — the system drifting downhill. Optional ground-state line and
    a temperature curve on a twin axis."""
    _style()
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    steps = np.arange(len(traj))
    ax.plot(steps, traj, color=CYAN, lw=1.8, label="energy (annealing)")
    if e_ground is not None:
        ax.axhline(e_ground, color=LIME, lw=1.6, ls="--", label=f"exact ground state ({e_ground:.3f})")
    ax.set_xlabel("sweep")
    ax.set_ylabel("energy  E(s)")
    ax.set_title(title)
    if Ts is not None:
        axT = ax.twinx()
        axT.plot(steps, Ts, color=AMBER, lw=1.2, alpha=0.7, label="temperature")
        axT.set_ylabel("temperature  T", color=AMBER)
        axT.tick_params(axis="y", colors=AMBER)
        axT.grid(False)
        axT.set_yscale("log")
    ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=9, loc="upper right")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    return _save(fig, out)


def plot_spins(s, *, grid_shape=None, title="Ground state", out="figures/spins.png"):
    """Show a spin configuration. 1-D → signed bars; 2-D → a colored lattice."""
    _style()
    s = np.asarray(s)
    if grid_shape is not None:
        fig, ax = plt.subplots(figsize=(4.6, 4.6))
        ax.imshow(s.reshape(grid_shape), cmap=plt.matplotlib.colors.ListedColormap([MAGENTA, CYAN]),
                  vmin=-1, vmax=1, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        ax.set_title(title)
    else:
        fig, ax = plt.subplots(figsize=(8.0, 2.4))
        ax.bar(np.arange(len(s)), s, color=[CYAN if v > 0 else MAGENTA for v in s], width=0.9)
        ax.set_ylim(-1.2, 1.2); ax.set_xlabel("spin index"); ax.set_yticks([-1, 0, 1])
        ax.set_title(title)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return _save(fig, out)


def plot_landscape(all_energies, *, e_ground=None, title="Energy landscape", out="figures/landscape.png"):
    """Histogram of the full 2ⁿ energy spectrum — shows how rare the ground state is."""
    _style()
    fig, ax = plt.subplots(figsize=(8.0, 4.2))
    ax.hist(all_energies, bins=80, color=CYAN, alpha=0.8)
    if e_ground is not None:
        ax.axvline(e_ground, color=LIME, lw=1.8, ls="--", label=f"ground state ({e_ground:.3f})")
        ax.legend(facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, fontsize=9)
    ax.set_xlabel("energy  E(s)"); ax.set_ylabel("number of configurations")
    ax.set_title(title)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    return _save(fig, out)


def plot_graph_cut(W, s, *, title="MaxCut partition", out="figures/cut.png"):
    """A weighted graph with its partition: nodes colored by side (±1), cut edges
    highlighted, uncut edges faded. Uses a spring layout if networkx is available."""
    _style()
    W = np.asarray(W)
    s = np.asarray(s)
    n = len(s)

    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if W[i, j] != 0]
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
        pos = {k: np.asarray(v) for k, v in nx.spring_layout(G, seed=7).items()}
    except Exception:
        ang = 2 * np.pi * np.arange(n) / max(n, 1)
        pos = {i: np.array([np.cos(a), np.sin(a)]) for i, a in enumerate(ang)}

    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    for i, j in edges:
        cut = s[i] != s[j]
        ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]],
                color=(LIME if cut else MUTED), lw=(1.9 if cut else 0.6),
                alpha=(0.9 if cut else 0.3), zorder=1)
    for i in range(n):
        ax.scatter(*pos[i], s=200, color=(CYAN if s[i] > 0 else MAGENTA),
                   edgecolor="white", linewidth=0.7, zorder=2)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False); ax.set_aspect("equal")
    ax.set_title(title)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return _save(fig, out)
