import networkx as nx
import matplotlib.pyplot as plt

def create_graph(nodes: list, edges: list) -> nx.graph:
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def draw_graph(G: nx.graph) -> None:
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def main():
    G = create_graph([1, 2, 3, 4], [(1, 2), (2, 3)])
    draw_graph(G)

if __name__ == "__main__":
    main()