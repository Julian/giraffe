from giraffe.exceptions import NoSuchEdge
from giraffe.graph_mixin cimport GraphMixin

cdef class Graph(GraphMixin):
    def add_edge(self, u, v):
        # if necessary we can sorted(key=id) to know where to put the edge
        self.add_vertices((u, v))

        if not self.has_edge(u, v):
            self._size += 1

        self._adj[u].add(v)

    def has_edge(self, u, v):
        u_adj, v_adj = self._adj.get(u, {}), self._adj.get(v, {})
        return v in u_adj or u in v_adj

    def neighbors(self, v):
        return self[v] | {u for u in self if v in self[u]}

    def remove_vertex(self, v):
        del self[v]

        for u, e in self._adj.iteritems():
            if v in e:
                e.remove(v)

    def remove_edge(self, u, v):
        try:
            self[u].remove(v)
        except KeyError:
            raise NoSuchEdge((u, v))
        else:
            self._size -= 1
