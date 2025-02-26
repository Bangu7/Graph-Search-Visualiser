import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import graph
import argparse
import sys

paused = False
helded = False
x_pos = 0
y_pos = 0

def draw_graph_state(G, ax, pos):
    ax.clear()
    node_colors = [G._graph.nodes[node].get('color', 'skyblue') for node in G._graph.nodes]
    edge_colors = [G._graph[u][v].get('color', 'black') for u, v in G._graph.edges]
    nx.draw(G._graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)

def find_nodes_at_click(event, pos):
    id1 = -1
    id2 = -1
    for node, (x,y) in pos.items():
        distance1 = (event.xdata - x) ** 2 + (event.ydata - y) ** 2
        distance2 = (x_pos - x) ** 2 + (y_pos - y) ** 2
        if distance1 < 0.005:
            id1 = node
        if distance2 < 0.005:
            id2 = node
    return id1, id2

def draw_graph(G: graph.Graph) -> None:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G._graph)

    def update(frame):
        if G.is_impossible():
            print("Nope")
            return
        if G.is_solved() or paused:
            return
        G.step()
        draw_graph_state(G, ax, pos)
        
    def on_click(event):
        global helded, x_pos, y_pos
        helded = True
        x_pos = event.xdata
        y_pos = event.ydata

    def on_release(event):
        global helded
        helded = False
        distance = (event.xdata - x_pos) ** 2 + (event.ydata - y_pos) ** 2
        if distance < 0.005:
            remove_node(event)
        else:
            id1, id2 = find_nodes_at_click(event, pos)
            if G._graph.has_edge(id1, id2):
                G.remove_edge_line(id1, id2)
            else:
                G.add_edge_line(id1, id2) 
            draw_graph_state(G, ax, pos)

    def remove_node(event):
        if event.inaxes != ax or not paused:
            return
        for node, (x,y) in pos.items():
            distance = (event.xdata - x) ** 2 + (event.ydata - y) ** 2
            if distance < 0.005:
                is_cur = G.remove_node(node)
                if is_cur == -1:
                    return
                if is_cur == 1:
                    print("Can't remove current node")
                    return
                print(f"Removed node {node}")
                draw_graph_state(G, ax, pos)
                return
        add_node(event)
    
    def add_node(event):
        id = G._max_node + 1
        G.add_node(id)
        pos[id] = (event.xdata, event.ydata)
        draw_graph_state(G, ax, pos)

    def toggle_pause(event):
        global paused
        paused = not paused

    def reset(event):
        G.reset()
        ax.clear()
        draw_graph_state(G, ax, pos)

    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    cid = fig.canvas.mpl_connect('button_release_event', on_release)

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
    edges.extend([(i, i + 2) for i in range(total - 2)])
    edges.extend([(i, i + 3) for i in range(total - 3)])
    # edges.extend([(i, i + 4) for i in range(total - 4)])
    
    if args.BFS:
        G = graph.BFSGraph(nodes=[i for i in range(total)], edges=edges, start=5, goal=13)
        draw_graph(G)
    elif args.DFS:
        print("DFS is not yet implemented.")
    elif args.TEST:
        G = graph.BFSGraph(nodes=[i for i in range(total)], edges=[(1,2)], start=5, goal=13)
        draw_graph(G)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualisation of Search")
    parser.add_argument("--BFS", action="store_true", help="Test BFS.")
    parser.add_argument("--DFS", action="store_true", help="Test DFS.")
    parser.add_argument("--TEST", action="store_true", help="Test")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    main(args)