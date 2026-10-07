"""Simulation of the triangle threshold p = 1/n in G(n, p)."""
import numpy as np

from random_graph import random_graph

DEFAULT_P = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05,
             0.075, 0.1, 0.15, 0.2]


def has_triangle(A):
    """True if the graph has a triangle.

    trace(A^3) counts closed walks of length 3; each triangle is counted
    6 times (3 starting vertices x 2 directions), so trace > 0 iff a
    triangle exists.
    """
    return np.trace(np.linalg.matrix_power(A, 3)) > 0


def triangle_threshold(n=50, trials=200, seed=123, p_values=DEFAULT_P):
    """Estimate P(G(n, p) contains a triangle) for each p."""
    rng = np.random.default_rng(seed)
    rows = []
    for p in p_values:
        found = sum(has_triangle(random_graph(n, p, rng)) for _ in range(trials))
        rows.append({"p": p, "triangles_found": found, "trials": trials,
                     "p_triangle": round(found / trials, 3)})
    return rows


def plot_threshold(rows, n, path):
    """Plot P(triangle) against p with the theoretical threshold 1/n marked."""
    import matplotlib.pyplot as plt

    ps = [r["p"] for r in rows]
    probs = [r["p_triangle"] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(ps, probs, color="#2a78d6", linewidth=2, marker="o", markersize=6)
    ax.axvline(1 / n, color="#52514e", linestyle="--", linewidth=1)
    ax.text(1 / n + 0.003, 0.08, f"threshold p = 1/n = {1/n:.2f}",
            color="#52514e", fontsize=10)
    ax.set_xlabel("Edge probability p", color="#52514e")
    ax.set_ylabel("P(graph contains a triangle)", color="#52514e")
    ax.set_title(f"Triangle threshold in G({n}, p), {rows[0]['trials']} trials per p",
                 fontsize=12, loc="left")
    ax.set_ylim(-0.03, 1.05)
    ax.grid(axis="y", color="#e5e4e0", linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#bdbcb7")
    ax.tick_params(colors="#52514e")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    from tabulate import tabulate
    rows = triangle_threshold()
    print(tabulate(rows, headers="keys"))
    plot_threshold(rows, 50, "figures/triangle_threshold.png")
