import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import graph
import argparse
import sys

def draw_graph(G: graph.Graph) -> None:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G._graph)

    def update(frame):
        if G._solved:
            return
        G.step()
        ax.clear()
        node_colors = [G._graph.nodes[node].get('color', 'skyblue') for node in G._graph.nodes]
        edge_colors = [G._graph[u][v].get('color', 'black') for u, v in G._graph.edges]
        nx.draw(G._graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)

    anim = animation.FuncAnimation(fig=fig, func=update, frames=range(100), blit=False, repeat=False, interval=500)
    plt.show()

def main(args: argparse.Namespace):
    total = 15
    edges = [(i, i + 1) for i in range(total - 1)]
    edges.extend([(i, i + 2) for i in range(total - 1)])
    edges.extend([(i, i + 3) for i in range(total - 1)])
    # edges.extend([(i, i + 4) for i in range(total - 1)])
    
    if args.BFS:
        G = graph.BFSGraph(nodes=[i for i in range(total)], edges=edges, start=5, goal=13)
        draw_graph(G)
    elif args.DFS:
        print("DFS is not yet implemented.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualisation of Search")
    parser.add_argument("--BFS", action="store_true", help="Test BFS.")
    parser.add_argument("--DFS", action="store_true", help="Test DFS.")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    main(args)