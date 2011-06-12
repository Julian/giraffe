from giraffe.exceptions import NoSuchEdge
from giraffe.graph_mixin cimport GraphMixin

cdef class Graph(GraphMixin):
    property edges:

        def __get__(self):
            # this is lazy, there's a better way to do this
            seen = set()
            edges = set()

            for u, neighbors in self._adj.iteritems():
                seen.add(u)

                for v in neighbors:
                    if v not in seen:
                        edges.add((u, v))

            return edges

    def add_edge(self, u, v):
        self.add_vertices((u, v))

        if not self.has_edge(u, v):
            self._size += 1

        self._adj[u].add(v)
        self._adj[v].add(u)

    def has_edge(self, u, v):
        return v in self[u]

    def neighbors(self, v):
        return self[v]

    def remove_vertex(self, v):
        for u in self[v]:
            self[u].remove(v)

        del self[v]

    def remove_edge(self, u, v):
        try:
            self[u].remove(v)
            self[v].remove(u)
        except KeyError:
            raise NoSuchEdge((u, v))
        else:
            self._size -= 1
