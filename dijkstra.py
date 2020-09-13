import string
import random
import heapq
from graphviz import Graph as DotGraph

INF = float("inf")


class Node:
    """
    >>> node = Node("a")
    Node('a', inf)
    """

    def __init__(self, name, priority=INF):
        self.name = name
        self.priority = priority
        self.before = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, rhs):
        return self.name == rhs.name

    def __repr__(self):
        return f"Node('{self.name}', {self.priority}, {self.before})"

    def __lt__(self, rhs):
        """For heapq"""
        return self.priority < rhs.priority


class Graph:
    """
    Usage
    -----
    >>> graph = Graph.generate_graph(10)
    >>> graph.view()
    >>> graph.find_shortest_path("a->b")
    """

    def __init__(self, _map=None):
        if _map:
            self._map = _map
        else:
            self._map = {}
        # strict=True ensures that graph is rewritten for any changes in node
        self._dot = DotGraph(strict=True)
        self.places = []

    def __getitem__(self, key: Node):
        """Get neighbours and their respective distances"""
        neighbours = {}
        for pair, dist in self._map.items():
            if key in pair:
                neighbours[set(pair - {key}).pop()] = dist
        return neighbours

    def __contains__(self, lhs: frozenset):
        return lhs in self._map

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)

    def view(self):
        """
        Must be called at least once
        """
        for place in self.places:
            self._dot.node(place.name)

        for pair, dist in self._map.items():
            node1, node2 = pair
            self._dot.edge(node1.name, node2.name, label=str(dist))

        return self._dot

    def add(self, key: frozenset, value: int):
        self._map[key] = value

    def heapify(self):
        heapq.heapify(self.places)

    def _run(self):
        explored = set()
        nodes = self.places.copy()

        while nodes:

            ctx = heapq.heappop(nodes)

            for node, dist in self[ctx].items():
                if node in explored:
                    continue

                new_priority = ctx.priority + dist
                if new_priority < node.priority:
                    node.priority = new_priority
                    node.before = ctx

            explored.add(ctx)
            heapq.heapify(nodes)

    def _reset(self):
        for place in self.places:
            place.priority = INF
            place.before = None

    def find_shortest_path(self, srcdst: str):

        dot = self._dot.copy()

        src, dst = srcdst.split("->")

        self._reset()
        src_node = self.places[self.places.index(Node(src))]
        src_node.priority = 0

        self._run()

        path = []
        p = self.places[self.places.index(Node(dst))]
        dot.node(dst, color="red")
        path.append(p.name)
        a = p.name
        while p.before:
            path.append(p.before.name)
            dot.node(p.before.name, color="red")
            dot.edge(a, p.before.name, color="red")

            a = p.before.name

            p = p.before

        path.reverse()

        print("->".join(path))

        return dot

    @classmethod
    def generate_random(cls, num_nodes=None):

        if num_nodes is None:
            num_nodes = random.randint(5, 10)
        world_map = cls()

        for node_name in string.ascii_letters[:num_nodes]:

            existing_nodes_to_connect_to_new_node = random.sample(
                world_map.places, k=random.randint(0, len(world_map.places)))

            node = Node(node_name)
            world_map.add_place(node)

            # Add to map
            to_add = [frozenset({node, existing})
                      for existing in existing_nodes_to_connect_to_new_node]
            for pair in to_add:
                if pair not in world_map:
                    dist = random.randint(1, 10)
                    world_map.add(pair, dist)

        world_map.heapify()

        return world_map

    @classmethod
    def from_string(cls, string):

        world_map = cls()

        for line in string.strip().split("\n"):
            a, b, dist = line.split(",")

            a = Node(a.strip())
            b = Node(b.strip())

            world_map.add_place(a)
            world_map.add_place(b)
            world_map.add(frozenset({a, b}), int(dist))

        world_map.heapify()

        return world_map
