"""Simulations for Ramsey's theorem and Erdős's lower bound R(k) >= 2^(k/2 - 1)."""
from itertools import combinations
from math import ceil, comb

import numpy as np

from random_graph import random_graph


def has_clique_or_independent_set(A, k):
    """True if the graph contains a clique or an independent set of size k.

    Checks every k-subset S of vertices: S is a clique if all comb(k, 2) edges
    are present, and an independent set if none are.
    """
    n = A.shape[0]
    max_edges = comb(k, 2)
    for S in combinations(range(n), k):
        sub = A[np.ix_(S, S)]           # induced subgraph on S
        e = np.triu(sub, 1).sum()       # number of edges, no double counting
        if e == max_edges or e == 0:
            return True
    return False


def ramsey_simulation(k=5, trials=200, seed=123):
    """Estimate P(no clique or independent set of size k) in G(n, 1/2) as n grows.

    Stops once every sampled graph contains one, illustrating Ramsey's theorem.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for n in range(max(k, 5), min(4 * k, 50)):
        hits = sum(has_clique_or_independent_set(random_graph(n, 0.5, rng), k)
                   for _ in range(trials))
        p_none = 1 - hits / trials
        rows.append({"n": n, "has_clique_or_indep": hits, "trials": trials,
                     "p_none": round(p_none, 3)})
        if p_none == 0:
            break
    return rows


def existence_at_bound(k_values=(8, 9, 10, 11), max_tries=1000, seed=123):
    """At n = ceil(2^(k/2 - 1)), search for a 'witness' graph with no clique and
    no independent set of size k, as Erdős's bound guarantees one exists."""
    rows = []
    for k in k_values:
        rng = np.random.default_rng(seed + k)
        n = ceil(2 ** (k / 2 - 1))
        tries = None
        for t in range(1, max_tries + 1):
            if not has_clique_or_independent_set(random_graph(n, 0.5, rng), k):
                tries = t
                break
        rows.append({"k": k, "n": n, "witness_found": tries is not None,
                     "trials_needed": tries if tries else f">{max_tries}"})
    return rows


if __name__ == "__main__":
    from tabulate import tabulate
    print("Ramsey's theorem, k = 5")
    print(tabulate(ramsey_simulation(), headers="keys"))
    print("\nWitnesses at Erdős's lower bound")
    print(tabulate(existence_at_bound(), headers="keys"))


def exact_p_none(n, k=5):
    """Exact P(no clique and no independent set of size k) in G(n, 1/2),
    by checking all 2^(n choose 2) graphs. Only feasible for small n (<= 6)."""
    from itertools import product
    pairs = list(combinations(range(n), 2))
    count = 0
    for bits in product([0, 1], repeat=len(pairs)):
        A = np.zeros((n, n), dtype=int)
        for b, (i, j) in zip(bits, pairs):
            if b:
                A[i, j] = A[j, i] = 1
        count += not has_clique_or_independent_set(A, k)
    return count / 2 ** len(pairs)


def plot_ramsey(rows, k, path):
    """Plot the estimated P(no clique or independent set of size k) against n."""
    import matplotlib.pyplot as plt

    ns = [r["n"] for r in rows]
    ps = [r["p_none"] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(ns, ps, color="#2a78d6", linewidth=2, marker="o", markersize=6)
    ax.set_xlabel("Number of vertices n", color="#52514e")
    ax.set_ylabel(f"P(no {k}-clique and no {k}-independent set)", color="#52514e")
    ax.set_title(f"Ramsey's theorem in G(n, 1/2), k = {k}, {rows[0]['trials']} trials per n",
                 fontsize=12, loc="left")
    ax.set_ylim(-0.03, 1.05)
    ax.set_xticks(ns)
    ax.grid(axis="y", color="#e5e4e0", linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#bdbcb7")
    ax.tick_params(colors="#52514e")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
