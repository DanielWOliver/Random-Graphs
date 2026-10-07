"""Reproduce every table and figure in one go: python run_all.py"""
import csv
import time

import numpy as np
from tabulate import tabulate

from random_graph import random_graph, draw_graph
from ramsey import ramsey_simulation, existence_at_bound, exact_p_none, plot_ramsey
from triangles import triangle_threshold, plot_threshold


def save(rows, name):
    with open(f"results/{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"\n{name}\n" + tabulate(rows, headers="keys"))


if __name__ == "__main__":
    t0 = time.time()
    draw_graph(random_graph(40, 0.3, rng=np.random.default_rng(123)),
               "figures/random_graph_G40_0.3.png", title="Random graph G(40, 0.3)")
    ram = ramsey_simulation(k=5, trials=200, seed=123)
    save(ram, "ramsey_k5")
    plot_ramsey(ram, 5, "figures/ramsey_k5.png")
    print("\nSanity check against exact enumeration of every graph:")
    for n in (5, 6):
        print(f"  n = {n}: exact P(none) = {exact_p_none(n, k=5):.4f}")
    save(existence_at_bound(k_values=(8, 9, 10, 11)), "erdos_bound_witnesses")
    tri = triangle_threshold(n=50, trials=200, seed=123)
    save(tri, "triangle_threshold_n50")
    plot_threshold(tri, 50, "figures/triangle_threshold.png")
    print(f"\nDone in {time.time() - t0:.1f}s. Figures in figures/, tables in results/.")
