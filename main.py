import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import graph

def update(frame):
    if frame >= 10:
        return 

def draw_graph(G: nx.graph) -> None:
    fig, ax = plt.subplots()
    nx.draw(G, with_labels=True, font_weight='bold', node_color='skyblue')
    animation.FuncAnimation(fig=fig, func=update)
    plt.show()

def main():
    G = graph.Graph(nodes=[1, 2, 3, 4], edges=[(1, 2), (2, 3)])
    draw_graph(G)

if __name__ == "__main__":
    main()