import networkx as nx

"""
A base structure for a graph utilising networkx.

Params:
    nodes: a list of graph node ids
    edges: a list with edges to connect chosen node ids (Doesn't require node to exist)
    start: the node id of the starting node (Practical for algorithms)
    goal: node id of end point/goal
    default_colour: the default colour for each node

"""
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

    def remove_node(self, id):
        self._graph.remove_node(id)
    
    def add_edge_line(self, id1, id2):
        pass

    def reset(self):
        pass

"""
An extension of the Graph class into a BFS search algorithm. 
Each step of the algorithm can be done one at a time.
"""
class BFSGraph(Graph):
    def __init__(self, nodes: list, edges: list[tuple], start: int, goal: int, default_colour: str = 'skyblue', skip_step: bool = True) -> None:
        super().__init__(nodes, edges, start, goal, default_colour)
        self._frontier = [self._start]
        self._visited = set()
        self._solved = False
        self._impossible = False
        self._temp_adj = []
        self._cur_node = None
        self._skip_step = skip_step
        self._max_node = nodes[-1]
    
    def get_frontier(self):
        return self._frontier
    
    def get_visited(self):
        return self._visited
    
    def is_solved(self):
        return self._solved
    
    def is_impossible(self):
        return self._impossible

    def step(self) -> None:
        if self._solved:
            return
        elif not (len(self._frontier) or self._temp_adj):
            self._impossible = True
            return
        
        if not len(self._visited):
            self._visited.add(self._start)
            self._graph.nodes[self._start]['color'] = 'purple'
            return
        
        if not self._temp_adj:
            if self._cur_node is not None:
                self._graph.nodes[self._cur_node]['color'] = 'red'
            self._cur_node = self._frontier.pop(0)
            self._graph.nodes[self._cur_node]['color'] = 'purple'
            if not self._graph.adj[self._cur_node]:
                return
            for vertex in self._graph.adj[self._cur_node]:
                self._temp_adj.append(vertex)

        cur_adj = self._temp_adj.pop(0)
        if cur_adj == self._goal:
            self._graph.nodes[cur_adj]['color'] = 'green'
            self._graph[cur_adj][self._cur_node]['color'] = 'green'
            self._solved = True
            return
        if cur_adj not in self._visited:
            self._frontier.append(cur_adj)
            self._visited.add(cur_adj)
            self._graph.nodes[cur_adj]['color'] = 'red'
            self._graph[cur_adj][self._cur_node]['color'] = 'red'
        elif self._skip_step:
            self.step()

    def remove_node(self, id):
        if not self._graph.has_node(id):
            return -1

        if self._cur_node == id or self._start == id or self._goal == id:
            return 1

        self._graph.remove_node(id)
        if id in self._frontier:
            self._frontier.remove(id)
        if id in self._visited:
            self._visited.remove(id)
        if id in self._temp_adj:
            self._temp_adj.remove(id)
        return 0
    
    def add_edge_line(self, id1, id2):
        if not self._graph.has_node(id1) or not self._graph.has_node(id2):
            return -1
        if id1 == id2:
            return 1
        self._graph.add_edge(id1, id2)
        return 0
    
    def remove_edge_line(self, id1, id2):
        if not self._graph.has_node(id1) or not self._graph.has_node(id2):
            return -1
        if id1 == id2:
            return 1
        self._graph.remove_edge(id1, id2)
        return 0

    def reset(self):
        self._frontier = [self._start]
        self._visited = set()
        self._solved = False
        self._impossible = False
        self._temp_adj = []
        self._cur_node = None

        for node in self._graph.nodes():
            self._graph.nodes[node]['color'] = self._default_colour
            for other in self._graph.adj[node]:
                self._graph[node][other]['color'] = 'black'
        # nx.set_node_attributes(self._graph, 'color', self._default_colour)
        # nx.set_edge_attributes(self._graph, 'color', 'black')
    
    def add_node(self, id, colour = None):
        self._max_node = id
        return super().add_node(id, colour)