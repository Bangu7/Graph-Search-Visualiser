import networkx as nx

class Graph():
    def __init__(
        self,
        nodes: list = None,
        edges: list[tuple] = None,
        start: int = None,
        goal: int = None,
        default_colour: str = 'skyblue'
    ) -> None:
        self._graph = nx.Graph()
        self._graph.add_nodes_from(nodes)
        self._graph.add_edges_from(edges)
        self._start = start
        self._goal = goal
        self._default_colour = default_colour

    def add_node(self, id: int, colour: str = None):
        if colour is None:
            colour = self._default_colour
        self._graph.add_node(id, color=colour)

class BFSGraph(Graph):
    def __init__(self, nodes: list = None, edges: list[tuple] = None, start: int = None, goal: int = None, default_colour: str = 'skyblue') -> None:
        super().__init__(nodes, edges, start, goal, default_colour)