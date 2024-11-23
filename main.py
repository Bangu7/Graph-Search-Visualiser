import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import graph

def draw_graph(G: graph.Graph) -> None:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G._graph)

    def update(frame):
        if G._solved:
            return
        G.step()
        ax.clear()
        node_colors = [G._graph.nodes[node].get('color', 'skyblue') for node in G._graph.nodes]
        nx.draw(G._graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors)

    anim = animation.FuncAnimation(fig=fig, func=update, frames=range(100), blit=False, repeat=False, interval=500)
    plt.show()

def main():
    G = graph.BFSGraph(nodes=[i for i in range(100)], edges=[(i, i + 1) for i in range(99)], start=5, goal=7)
    draw_graph(G)

if __name__ == "__main__":
    main()