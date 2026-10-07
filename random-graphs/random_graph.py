"""Binomial random graph G(n, p) and visualisation helpers."""
import numpy as np


def random_graph(n, p=0.5, rng=None):
    """Return the adjacency matrix of a binomial random graph G(n, p).

    Each of the n(n-1)/2 possible edges is included independently with
    probability p. The matrix is symmetric with zeros on the diagonal.
    """
    rng = rng or np.random.default_rng()
    upper = rng.binomial(1, p, size=(n, n))   # random 0/1 entries
    A = np.triu(upper, 1)                     # keep the upper triangle above the diagonal
    return A + A.T                            # make it symmetric


def draw_graph(A, path=None, title=None, node_size=300):
    """Draw a graph from its adjacency matrix with NetworkX."""
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.from_numpy_array(A)
    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw(G, ax=ax, node_color="#2a78d6", edge_color="#9a9a96",
            node_size=node_size, width=0.8, pos=nx.spring_layout(G, seed=1))
    if title:
        ax.set_title(title, fontsize=12)
    if path:
        fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    A = random_graph(40, 0.3, rng=np.random.default_rng(123))
    draw_graph(A, "figures/random_graph_G40_0.3.png",
               title="Random graph G(40, 0.3)")
    print("Saved figures/random_graph_G40_0.3.png")
