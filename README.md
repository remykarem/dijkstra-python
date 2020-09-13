# Dijkstra-like algorithm for path finding

```python
>>> from dijsktra import Graph
>>> g = Graph.generate_random()
>>> g.view()
```

![graph](graph.svg)

```python
>>> g.find_shortest_path("g->f")
```

![graph-highlighted](graph-highlight.svg)
