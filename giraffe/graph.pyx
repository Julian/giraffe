from giraffe.exceptions import EdgeCreatesLoop, NoSuchEdge
from giraffe.graph_mixin cimport GraphMixin

cdef class Graph(GraphMixin):

    # cdef public bint is_directed
    # cdef public bint is_multigraph

    property edges:

        def __get__(self):
            # this is lazy, there's a better way to do this
            seen = set()
            edges = set()

            # TODO: iter_neighbors
            for u, neighbors in self._adj.iteritems():
                seen.add(u)

                for v in neighbors:
                    if v not in seen:
                        edges.add((u, v))

            return edges

    # TODO: edge_added
    def add_edge(self, u, v):
        if u == v:
            raise EdgeCreatesLoop((u, v))

        self.add_vertices((u, v))

        if not self.has_edge(u, v):
            self._size += 1

        self._adj[u].add(v)
        self._adj[v].add(u)

    def degree(self, v):
        return len(self[v])

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

cdef class DiGraph(GraphMixin):

    # cdef public bint is_directed
    # cdef public bint is_multigraph

    property edges:

        def __get__(self):
            return {(u, v) for u in self for v in self[u]}

    def add_edge(self, u, v):
        if u == v:
            raise EdgeCreatesLoop((u, v))

        self.add_vertices((u, v))

        if not self.has_edge(u, v):
            self._size += 1

        self._adj[u].add(v)

    def remove_vertex(self, v):
        del self[v]

        for u in self:
            if v in self[u]:
                self[u].remove(v)

    def remove_edge(self, u, v):
        try:
            self[u].remove(v)
        except KeyError:
            raise NoSuchEdge((u, v))
        else:
            self._size -= 1

    def degree(self, v):
        return self.in_degree(v) + self.out_degree(v)

    def in_degree(self, v):
        return sum(1 for u in self if v in self[u])

    def out_degree(self, v):
        return len(self[v])
