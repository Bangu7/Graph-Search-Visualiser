import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import graph
import argparse
import sys

paused = False

def draw_graph(G: graph.Graph) -> None:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G._graph)

    def update(frame):
        if G._solved or paused:
            return
        G.step()
        ax.clear()
        node_colors = [G._graph.nodes[node].get('color', 'skyblue') for node in G._graph.nodes]
        edge_colors = [G._graph[u][v].get('color', 'black') for u, v in G._graph.edges]
        nx.draw(G._graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)

    def on_click(event):
        if event.inaxes != ax or not paused:
            return
        for node, (x,y) in pos.items():
            distance = (event.xdata - x) ** 2 + (event.ydata - y) ** 2
            if distance < 0.005:
                is_cur = G.remove_node(node)
                if is_cur:
                    print("Can't remove current node")
                    return
                print(f"Removed node {node}")
                ax.clear()
                node_colors = [G._graph.nodes[node].get('color', 'skyblue') for node in G._graph.nodes]
                edge_colors = [G._graph[u][v].get('color', 'black') for u, v in G._graph.edges]
                nx.draw(G._graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)
                break
    
    def toggle_pause(event):
        global paused
        paused = not paused

    def reset(event):
        G.reset()
        ax.clear()
        # pos = nx.spring_layout(G._graph)
        node_colors = [G._graph.nodes[node].get('color', 'skyblue') for node in G._graph.nodes]
        edge_colors = [G._graph[u][v].get('color', 'black') for u, v in G._graph.edges]
        nx.draw(G._graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)

    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    ax_button = plt.axes([0.85, 0.01, 0.125, 0.075])
    button = Button(ax_button, 'Pause/Play')
    button.on_clicked(toggle_pause)

    ax_button2 = plt.axes([0.1, 0.01, 0.125, 0.075])
    button2 = Button(ax_button2, 'Reset')
    button2.on_clicked(reset)

    anim = animation.FuncAnimation(fig=fig, func=update, frames=range(100), blit=False, repeat=True, interval=500)
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