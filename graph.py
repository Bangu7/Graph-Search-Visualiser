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
        self._temp_adj = []
        self._cur_node = None
        self._skip_step = skip_step
    
    def get_frontier(self):
        return self._frontier
    
    def get_visited(self):
        return self._visited
    
    def is_solved(self):
        return self._solved

    def step(self) -> None:
        # print(self._frontier)
        if not len(self._frontier) or self._solved:
            return
        
        if not len(self._visited):
            self._visited.add(self._start)
            self._graph.nodes[self._start]['color'] = 'red'
            return
        
        if not self._temp_adj:
            if self._cur_node:
                self._graph.nodes[self._cur_node]['color'] = 'red'
            self._cur_node = self._frontier.pop(0)
            self._graph.nodes[self._cur_node]['color'] = 'purple'
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
        if self._cur_node == id:
            return True
        self._graph.remove_node(id)
        if id in self._frontier:
            self._frontier.remove(id)
        if id in self._visited:
            self._visited.remove(id)
        if id in self._temp_adj:
            self._temp_adj.remove(id)
        return False