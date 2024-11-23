import networkx as nx

class Graph():
    def __init__(
        self,
        nodes: list,
        edges: list[tuple],
        start: int,
        goal: int,
        default_colour: str = 'skyblue'
    ) -> None:
        self._graph = nx.Graph()
        self._graph.add_nodes_from(nodes)
        self._graph.add_edges_from(edges)
        self._start = start
        self._goal = goal
        self._default_colour = default_colour

    def get_graph_nx(self) -> nx.Graph:
        return self._graph

    def add_node(self, id: int, colour: str = None) -> None:
        if colour is None:
            colour = self._default_colour
        self._graph.add_node(id, color=colour)

    def add_edge(self, vertex1: int, vertex2: int) -> None:
        self._graph.add_edge(vertex1, vertex2)

    def set_start(self, start: int) -> None:
        self._start = start

    def set_goal(self, goal: int) -> None:
        self._goal = goal


class BFSGraph(Graph):
    def __init__(self, nodes: list, edges: list[tuple], start: int, goal: int, default_colour: str = 'skyblue') -> None:
        super().__init__(nodes, edges, start, goal, default_colour)
        self._frontier = [self._start]
        self._visited = set()
        self._solved = False        
    
    def step(self) -> None:
        if not len(self._frontier) or self._solved:
            return
        
        if not len(self._visited):
            self._visited.add(self._start)
            self._graph.nodes[self._start]['color'] = 'red'
            return
        
        cur = self._frontier.pop(0)
        for vertex in self._graph.adj[cur]:
            if vertex == self._goal:
                self._graph.nodes[vertex]['color'] = 'green'
                self._solved = True
                return
            if vertex not in self._visited:
                self._frontier.append(vertex)
                self._visited.add(vertex)
                self._graph.nodes[vertex]['color'] = 'red'